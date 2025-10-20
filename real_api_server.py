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
from google.cloud import storage
import base64
import io


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

# GCS Setup
GCS_BUCKET_NAME = "gcs-vodacast-bucket"  # replace with your bucket name
# GCS_CREDENTIALS_FILE_FOR_VIDEO_UPLOADING = "gcs_credentials.json"  # path to your service account JSON
GCS_CREDENTIALS_FILE_FOR_VIDEO_UPLOADING = os.path.join(os.getcwd(), "gcs_credentials.json")

def upload_to_gcs(local_file, bucket_name, destination_blob):
    client = storage.Client.from_service_account_json(GCS_CREDENTIALS_FILE_FOR_VIDEO_UPLOADING)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(local_file)
    
    # Make the file public
    blob.make_public()
    
    return blob.public_url


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_sadtalker_inference(job_id, image_path, audio_path, preprocess='crop', still_mode='false', 
                           use_enhancer='false', batch_size='1', size='256', pose_style='0', 
                           upload_to_youtube_flag='false', youtube_title='', youtube_description='', 
                           youtube_tags='', youtube_privacy='private'):
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

                print(f"Uploading to GCS: {output_path}")

                # Upload to GCS
                # gcs_filename = f"{job_id}/output.mp4"
                public_url = upload_to_gcs(
                    local_file=output_path,
                    bucket_name=GCS_BUCKET_NAME,
                    destination_blob=f"{job_id}/output.mp4"
                )


                print(f"Uploaded to GCS: {public_url}")
                print("reached")

                # YouTube upload if requested
                youtube_result = None
                if upload_to_youtube_flag.lower() == 'true':
                    print(f"Starting YouTube upload for job {job_id}")
                    jobs[job_id]['youtube_status'] = 'uploading'
                    
                    # Prepare YouTube metadata
                    title = youtube_title or f"SadTalker Generated Video - {job_id[:8]}"
                    description = youtube_description or f"AI-generated talking face video created with SadTalker. Job ID: {job_id}"
                    tags = [tag.strip() for tag in youtube_tags.split(',') if tag.strip()] if youtube_tags else ['SadTalker', 'AI', 'Talking Face']
                    
                    youtube_result = upload_to_youtube(
                        video_path=output_path,
                        title=title,
                        description=description,
                        tags=tags,
                        privacy_status=youtube_privacy
                    )
                    
                    if youtube_result['success']:
                        jobs[job_id]['youtube_status'] = 'completed'
                        jobs[job_id]['youtube_url'] = youtube_result['video_url']
                        jobs[job_id]['youtube_video_id'] = youtube_result['video_id']
                        print(f"YouTube upload successful: {youtube_result['video_url']}")
                    else:
                        jobs[job_id]['youtube_status'] = 'failed'
                        jobs[job_id]['youtube_error'] = youtube_result['error']
                        print(f"YouTube upload failed: {youtube_result['error']}")

                jobs[job_id]['status'] = 'completed'
                jobs[job_id]['progress'] = 100
                jobs[job_id]['result_path'] = output_path
                # jobs[job_id]['s3_url'] = f'http://localhost:7860/api/results/{job_id}/output.mp4'
                jobs[job_id]['s3_url']= public_url
            else:
                jobs[job_id]['status'] = 'failed'
                jobs[job_id]['error'] = 'No output video generated'
        else:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['error'] = result.stderr or 'Inference failed'
            
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)

@app.route('/api/youtube/auth', methods=['GET'])
def youtube_auth():
    """Initialize YouTube OAuth flow"""
    try:
        if not os.path.exists(YOUTUBE_CLIENT_SECRETS_FILE):
            return jsonify({
                'error': f'YouTube client secrets file not found: {YOUTUBE_CLIENT_SECRETS_FILE}',
                'setup_required': True
            }), 400
        
        flow = Flow.from_client_secrets_file(YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
        flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
        
        auth_url, _ = flow.authorization_url(prompt='consent')
        
        return jsonify({
            'auth_url': auth_url,
            'message': 'Visit the URL to authorize YouTube access',
            'setup_required': False
        })
        
    except Exception as e:
        return jsonify({
            'error': f'YouTube auth setup failed: {str(e)}',
            'setup_required': True
        }), 500

@app.route('/api/youtube/auth/callback', methods=['POST'])
def youtube_auth_callback():
    """Complete YouTube OAuth flow with authorization code"""
    try:
        data = request.get_json()
        auth_code = data.get('auth_code', '').strip()
        
        if not auth_code:
            return jsonify({'error': 'Authorization code is required'}), 400
        
        flow = Flow.from_client_secrets_file(YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
        flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
        
        flow.fetch_token(code=auth_code)
        creds = flow.credentials
        
        # Save credentials
        with open(YOUTUBE_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        
        return jsonify({
            'success': True,
            'message': 'YouTube authorization completed successfully'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'YouTube auth callback failed: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'SadTalker API is running',
        'timestamp': time.time(),
        'active_jobs': len([job for job in jobs.values() if job['status'] == 'processing'])
    })

import requests
from google.oauth2 import service_account
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import pickle

GCS_CREDENTIALS_FILE = os.path.join(os.getcwd(), "revoiz-ai-dd6bb5e7b3ee.json")

# YouTube API Configuration
YOUTUBE_CLIENT_SECRETS_FILE = os.path.join(os.getcwd(), "youtube_client_secrets.json")
YOUTUBE_TOKEN_FILE = os.path.join(os.getcwd(), "youtube_token.pickle")
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_youtube_service():
    """Get authenticated YouTube service"""
    creds = None
    
    # Load existing token
    if os.path.exists(YOUTUBE_TOKEN_FILE):
        with open(YOUTUBE_TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(YOUTUBE_CLIENT_SECRETS_FILE):
                raise FileNotFoundError(f"YouTube client secrets file not found: {YOUTUBE_CLIENT_SECRETS_FILE}")
            
            flow = Flow.from_client_secrets_file(YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"Please visit this URL to authorize the application: {auth_url}")
            auth_code = input('Enter the authorization code: ')
            flow.fetch_token(code=auth_code)
            creds = flow.credentials
        
        # Save credentials for next run
        with open(YOUTUBE_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

def upload_to_youtube(video_path, title, description="", tags=None, privacy_status="private"):
    """Upload video to YouTube"""
    try:
        youtube = get_youtube_service()
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': '22'  # People & Blogs category
            },
            'status': {
                'privacyStatus': privacy_status  # private, public, unlisted
            }
        }
        
        # Create media upload object
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        
        # Insert video
        insert_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        # Execute upload
        response = None
        while response is None:
            status, response = insert_request.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")
        
        if 'id' in response:
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return {
                'success': True,
                'video_id': video_id,
                'video_url': video_url,
                'title': title
            }
        else:
            return {
                'success': False,
                'error': 'Upload failed - no video ID returned'
            }
            
    except HttpError as e:
        return {
            'success': False,
            'error': f'YouTube API error: {e}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Upload error: {str(e)}'
        }

def get_google_access_token():
    """Fetch OAuth2 access token using service account"""
    credentials = service_account.Credentials.from_service_account_file(
        GCS_CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    return credentials.token


@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech using Google Cloud Text-to-Speech REST API with language support"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        language_code = data.get('language_code', 'en-US')  # Default to English
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Validate language code
        valid_languages = {
            'en-US': 'English (US)',
            'ur-IN': 'Urdu (India)', 
            'hi-IN': 'Hindi (India)'
        }
        
        if language_code not in valid_languages:
            return jsonify({
                'error': f'Invalid language code. Supported languages: {list(valid_languages.keys())}'
            }), 400
        
        print(f"Generating speech for language: {language_code} ({valid_languages[language_code]})")
        
        # Get access token
        access_token = get_google_access_token()
        print(f"Access token---->: {access_token}")
        
        # Configure voice parameters based on language
        voice_config = {
            'en-US': {
                'languageCode': 'en-US',
                'name': 'en-US-Standard-A',  # Female voice
                'ssmlGender': 'FEMALE'
            },
            'ur-IN': {
                'languageCode': 'ur-IN',
                'name': 'ur-IN-Standard-A',  # Standard voice for Urdu
                'ssmlGender': 'FEMALE'
            },
            'hi-IN': {
                'languageCode': 'hi-IN',
                'name': 'hi-IN-Standard-A',  # Female voice for Hindi
                'ssmlGender': 'FEMALE'
            }
        }
        
        # Prepare the request payload
        payload = {
            "input": {
                "text": text
            },
            "voice": voice_config[language_code],
            "audioConfig": {
                "audioEncoding": "MP3"
            }
        }
        
        # Make the API request to Google Cloud Text-to-Speech
        api_url = "https://texttospeech.googleapis.com/v1/text:synthesize"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "x-goog-user-project": "revoiz-ai",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        print(f"Making request to Google Cloud TTS API...")
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        print(f"Response: {response}")
        
        if response.status_code == 200:
            response_data = response.json()
            
            # Get the base64 audio content
            audio_content_b64 = response_data.get('audioContent', '')

            print(f"Audio content: {audio_content_b64}")
            if not audio_content_b64:
                return jsonify({'error': 'No audio content received from Google Cloud TTS'}), 500
            
            # Decode the base64 audio content
            audio_content = base64.b64decode(audio_content_b64)


            print(f"audio_content: {audio_content}")
            # Generate filename with timestamp
            filename = f'generated_speech_{language_code}_{int(time.time())}.mp3'

            print(f"filename: {filename}")
            
            return jsonify({
                'status': 'success',
                'message': f'Text converted to speech successfully in {valid_languages[language_code]}',
                'audio_data': audio_content_b64,  # Return the base64 string directly
                'filename': filename,
                'language_code': language_code,
                'language_name': valid_languages[language_code],
                'file_size': len(audio_content),
                'audio_format': 'mp3'
            })
        else:
            error_msg = f"Google Cloud TTS API error: {response.status_code}"
            try:
                error_data = response.json()
                error_msg += f" - {error_data.get('error', {}).get('message', 'Unknown error')}"
            except:
                error_msg += f" - {response.text}"
            
            print(f"TTS API Error: {error_msg}")
            return jsonify({'error': error_msg}), 500
        
    except Exception as e:
        print(f"Google Cloud Text-to-speech error: {str(e)}")
        return jsonify({'error': f'Text-to-speech failed: {str(e)}'}), 500




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
    
    # YouTube upload parameters
    upload_to_youtube_flag = request.form.get('upload_to_youtube', 'false')
    youtube_title = request.form.get('youtube_title', '')
    youtube_description = request.form.get('youtube_description', '')
    youtube_tags = request.form.get('youtube_tags', '')
    youtube_privacy = request.form.get('youtube_privacy', 'private')
    
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
        'upload_to_youtube': upload_to_youtube_flag,
        'youtube_title': youtube_title,
        'youtube_description': youtube_description,
        'youtube_tags': youtube_tags,
        'youtube_privacy': youtube_privacy
    }
    
    # Start background processing
    thread = threading.Thread(target=run_sadtalker_inference, args=(
        job_id, image_path, audio_path, preprocess, still_mode, 
        use_enhancer, batch_size, size, pose_style, upload_to_youtube_flag,
        youtube_title, youtube_description, youtube_tags, youtube_privacy
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
    print("   POST /api/text-to-speech - Convert text to speech")
    print("   POST /api/jobs - Create a new job")
    print("   GET  /api/jobs - List all jobs")
    print("   GET  /api/jobs/<job_id> - Get job status")
    print("   GET  /api/results/<job_id>/<filename> - Download result files")
    print("   GET  /api/youtube/auth - Initialize YouTube OAuth")
    print("   POST /api/youtube/auth/callback - Complete YouTube OAuth")
    print("\n🎥 YouTube Integration:")
    print("   - Set upload_to_youtube=true in job creation")
    print("   - Provide youtube_title, youtube_description, youtube_tags, youtube_privacy")
    print("   - Videos will be uploaded to your YouTube channel after generation")
    print("\n🧪 You can now test with Postman or run test_api.py")
    
    app.run(host='0.0.0.0', port=7860, debug=True)
