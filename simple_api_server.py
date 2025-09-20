#!/usr/bin/env python3
"""
Simple SadTalker API server for testing with real files
"""
import os
import sys
import uuid
import json
import time
import threading
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
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

def simulate_processing(job_id):
    """Simulate processing with real file handling"""
    try:
        job = jobs[job_id]
        
        # Update progress
        for i in range(10, 101, 10):
            jobs[job_id]['progress'] = i
            jobs[job_id]['status'] = 'processing'
            time.sleep(1)
        
        # Create a mock result file
        result_dir = os.path.join(RESULTS_FOLDER, job_id)
        os.makedirs(result_dir, exist_ok=True)
        
        # Copy the input files to results for demonstration
        if os.path.exists(job['image_path']):
            shutil.copy2(job['image_path'], os.path.join(result_dir, 'input_image.png'))
        
        if os.path.exists(job['audio_path']):
            shutil.copy2(job['audio_path'], os.path.join(result_dir, 'input_audio.wav'))
        
        # Create a mock output video (just copy a sample file if available)
        sample_video = None
        for ext in ['mp4', 'avi', 'mov']:
            sample_files = list(Path('.').glob(f'**/*.{ext}'))
            if sample_files:
                sample_video = sample_files[0]
                break
        
        if sample_video:
            shutil.copy2(sample_video, os.path.join(result_dir, 'output.mp4'))
        else:
            # Create a dummy file
            with open(os.path.join(result_dir, 'output.mp4'), 'w') as f:
                f.write('Mock video file - replace with actual SadTalker output')
        
        # Update job status
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['result_path'] = os.path.join(result_dir, 'output.mp4')
        jobs[job_id]['s3_url'] = f'http://localhost:7860/api/results/{job_id}/output.mp4'
        
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
    """Create a new job with real file uploads"""
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
        'audio_path': audio_path,
        'image_filename': image_file.filename,
        'audio_filename': audio_file.filename
    }
    
    # Start background processing
    thread = threading.Thread(target=simulate_processing, args=(job_id,))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'status': 'created',
        'message': 'Job created successfully',
        'preprocess': preprocess,
        'still_mode': still_mode,
        'use_enhancer': use_enhancer,
        'batch_size': batch_size,
        'size': size,
        'pose_style': pose_style,
        'image_filename': image_file.filename,
        'audio_filename': audio_file.filename
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

@app.route('/api/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    # Clean up files
    job = jobs[job_id]
    if os.path.exists(job['image_path']):
        os.remove(job['image_path'])
    if os.path.exists(job['audio_path']):
        os.remove(job['audio_path'])
    
    result_dir = os.path.join(RESULTS_FOLDER, job_id)
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    
    del jobs[job_id]
    return jsonify({
        'message': f'Job {job_id} deleted successfully'
    })

@app.route('/api/results/<job_id>/<filename>')
def get_result_file(job_id, filename):
    """Serve result files"""
    result_dir = os.path.join(RESULTS_FOLDER, job_id)
    file_path = os.path.join(result_dir, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    print("🚀 Starting Simple SadTalker API server on http://localhost:7860")
    print("📝 Available endpoints:")
    print("   GET  /api/health - Health check")
    print("   POST /api/jobs - Create a new job")
    print("   GET  /api/jobs - List all jobs")
    print("   GET  /api/jobs/<job_id> - Get job status")
    print("   DELETE /api/jobs/<job_id> - Delete a job")
    print("   GET  /api/results/<job_id>/<filename> - Download result files")
    print("\n🧪 You can now test with Postman or run test_api.py")
    print("📁 Uploaded files will be saved to 'uploads/' directory")
    print("📁 Results will be saved to 'results/' directory")
    
    app.run(host='0.0.0.0', port=7860, debug=True)
