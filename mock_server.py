#!/usr/bin/env python3
"""
Mock server for testing SadTalker API endpoints
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import time
import threading
import json
from werkzeug.serving import make_server

app = Flask(__name__)
CORS(app)

# Store jobs in memory
jobs = {}

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
    has_image = 'source_image' in request.files
    has_audio = 'driven_audio' in request.files
    
    # Simulate processing time
    jobs[job_id] = {
        'job_id': job_id,
        'status': 'processing',
        'progress': 0,
        'created_at': time.time(),
        'preprocess': preprocess,
        'still_mode': still_mode,
        'use_enhancer': use_enhancer,
        'batch_size': batch_size,
        'size': size,
        'pose_style': pose_style,
        'has_image': has_image,
        'has_audio': has_audio
    }
    
    # Start background processing simulation
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
        'has_image': has_image,
        'has_audio': has_audio
    })

@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get job status"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    
    # Simulate progress
    if job['status'] == 'processing':
        elapsed = time.time() - job['created_at']
        progress = min(int(elapsed * 10), 100)
        job['progress'] = progress
        
        if progress >= 100:
            job['status'] = 'completed'
            job['result_path'] = f'/results/{job_id}/output.mp4'
            job['s3_url'] = f'https://s3.example.com/results/{job_id}/output.mp4'
    
    return jsonify(job)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'SadTalker API is running',
        'timestamp': time.time(),
        'active_jobs': len([job for job in jobs.values() if job['status'] == 'processing'])
    })

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
    
    del jobs[job_id]
    return jsonify({
        'message': f'Job {job_id} deleted successfully'
    })

def simulate_processing(job_id):
    """Simulate job processing"""
    time.sleep(2)  # Simulate processing time
    if job_id in jobs:
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['result_path'] = f'/results/{job_id}/output.mp4'
        jobs[job_id]['s3_url'] = f'https://s3.example.com/results/{job_id}/output.mp4'

if __name__ == '__main__':
    print("🚀 Starting mock SadTalker API server on http://localhost:7860")
    print("📝 Available endpoints:")
    print("   GET  /api/health - Health check")
    print("   POST /api/jobs - Create a new job")
    print("   GET  /api/jobs - List all jobs")
    print("   GET  /api/jobs/<job_id> - Get job status")
    print("   DELETE /api/jobs/<job_id> - Delete a job")
    print("\n🧪 You can now test with Postman or run test_api.py")
    print("📋 Postman Collection: Import the API endpoints above")
    
    server = make_server('localhost', 7860, app)
    server.serve_forever()
