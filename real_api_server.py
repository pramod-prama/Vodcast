#!/usr/bin/env python3
"""
Real SadTalker API server using inference.py
"""
import os
import sys
import uuid
import json
import time
import threading
import subprocess
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import tempfile
import shutil

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'wav', 'mp3', 'mp4'}

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Store jobs in memory
jobs = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_sadtalker_inference(job_id, image_path, audio_path, preprocess='crop', still_mode='false', 
                           use_enhancer='false', batch_size='1', size='256', pose_style='0'):
    """Run SadTalker inference using the inference.py script"""
    try:
        # Create result directory for this job
        result_dir = os.path.join(RESULTS_FOLDER, job_id)
        os.makedirs(result_dir, exist_ok=True)
        
        # Note: SadTalker will create its own timestamped subdirectory
        # We don't need to create it here as it will cause timestamp mismatches
        
        # Update job status
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['progress'] = 10
        
        # Prepare command for inference.py
        cmd = [
            sys.executable, 'inference.py',
            '--driven_audio', audio_path,
            '--source_image', image_path,
            '--result_dir', result_dir,
            '--preprocess', preprocess,
            '--batch_size', batch_size,
            '--size', size,
            '--pose_style', pose_style,
            '--cpu'  # Use CPU for compatibility
        ]
        
        # Add boolean flags only if they are True
        if still_mode.lower() == 'true':
            cmd.append('--still')
        
        # Add enhancer if specified (it expects a value, not a boolean)
        if use_enhancer.lower() == 'true':
            cmd.extend(['--enhancer', 'gfpgan'])  # Use gfpgan as default enhancer
        
        jobs[job_id]['progress'] = 30
        
        # Debug: Print the command being run
        print(f"Running command: {' '.join(cmd)}")
        
        # Run the inference
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        # Debug: Print the result
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT: {result.stdout}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        
        jobs[job_id]['progress'] = 80
        
        if result.returncode == 0:
            # Look for output video file - SadTalker creates a timestamped subdirectory
            output_files = []
            
            # First, look for .mp4 files in the result directory (SadTalker moves the final video there)
            output_files = list(Path(result_dir).glob('*.mp4'))
            
            # If not found, look in timestamped subdirectories
            if not output_files:
                for subdir in Path(result_dir).iterdir():
                    if subdir.is_dir() and '_' in subdir.name:  # timestamped directory
                        output_files = list(subdir.glob('*.mp4'))
                        if output_files:
                            break
            
            if output_files:
                output_path = str(output_files[0])
                jobs[job_id]['status'] = 'completed'
                jobs[job_id]['progress'] = 100
                jobs[job_id]['result_path'] = output_path
                jobs[job_id]['s3_url'] = f'http://localhost:7860/api/results/{job_id}/output.mp4'
            else:
                jobs[job_id]['status'] = 'failed'
                jobs[job_id]['error'] = 'No output video generated'
        else:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['error'] = result.stderr or 'Inference failed'
            
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'SadTalker API is running',
        'timestamp': time.time(),
        'active_jobs': len([job for job in jobs.values() if job['status'] == 'processing'])
    })

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job"""
    job_id = str(uuid.uuid4())
    
    # Get form data
    preprocess = request.form.get('preprocess', 'crop')
    still_mode = request.form.get('still_mode', 'false')
    use_enhancer = request.form.get('use_enhancer', 'false')
    batch_size = request.form.get('batch_size', '1')
    size = request.form.get('size', '256')
    pose_style = request.form.get('pose_style', '0')
    
    # Check if files were uploaded
    if 'source_image' not in request.files or 'driven_audio' not in request.files:
        return jsonify({'error': 'Both source_image and driven_audio files are required'}), 400
    
    image_file = request.files['source_image']
    audio_file = request.files['driven_audio']
    
    if image_file.filename == '' or audio_file.filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    if not (allowed_file(image_file.filename) and allowed_file(audio_file.filename)):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Save uploaded files
    image_filename = secure_filename(f"{job_id}_image_{image_file.filename}")
    audio_filename = secure_filename(f"{job_id}_audio_{audio_file.filename}")
    
    image_path = os.path.join(UPLOAD_FOLDER, image_filename)
    audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
    
    image_file.save(image_path)
    audio_file.save(audio_path)
    
    # Initialize job
    jobs[job_id] = {
        'job_id': job_id,
        'status': 'created',
        'progress': 0,
        'created_at': time.time(),
        'preprocess': preprocess,
        'still_mode': still_mode,
        'use_enhancer': use_enhancer,
        'batch_size': batch_size,
        'size': size,
        'pose_style': pose_style,
        'image_path': image_path,
        'audio_path': audio_path
    }
    
    # Start background processing
    thread = threading.Thread(target=run_sadtalker_inference, args=(
        job_id, image_path, audio_path, preprocess, still_mode, 
        use_enhancer, batch_size, size, pose_style
    ))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'status': 'created',
        'message': 'Job created successfully'
    })

@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get job status"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(jobs[job_id])

@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """List all jobs"""
    return jsonify({
        'jobs': list(jobs.values()),
        'total': len(jobs)
    })

@app.route('/api/results/<job_id>/<filename>')
def get_result_file(job_id, filename):
    """Serve result files"""
    result_dir = os.path.join(RESULTS_FOLDER, job_id)
    
    # First try the main result directory (where SadTalker moves the final video)
    file_path = os.path.join(result_dir, filename)
    
    # If not found, look in timestamped subdirectories
    if not os.path.exists(file_path):
        for subdir in os.listdir(result_dir):
            subdir_path = os.path.join(result_dir, subdir)
            if os.path.isdir(subdir_path) and '_' in subdir:  # timestamped directory
                potential_file = os.path.join(subdir_path, filename)
                if os.path.exists(potential_file):
                    file_path = potential_file
                    break
    
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    print("🚀 Starting Real SadTalker API server on http://localhost:7860")
    print("📝 Available endpoints:")
    print("   GET  /api/health - Health check")
    print("   POST /api/jobs - Create a new job")
    print("   GET  /api/jobs - List all jobs")
    print("   GET  /api/jobs/<job_id> - Get job status")
    print("   GET  /api/results/<job_id>/<filename> - Download result files")
    print("\n🧪 You can now test with Postman or run test_api.py")
    
    app.run(host='0.0.0.0', port=7860, debug=True)
