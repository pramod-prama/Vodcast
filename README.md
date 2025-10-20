# Vodcast - SadTalker API Integration with Multi-Language TTS

This repository includes a comprehensive SadTalker API system with multi-language Text-to-Speech support. It features a production-ready API for React integration, background job processing, real-time progress updates, Google Cloud Storage integration, and advanced TTS capabilities supporting English, Urdu, and Hindi languages.

## 🎯 Key Features

- **🎭 SadTalker Integration**: Generate talking face videos from images and audio
- **🌍 Multi-Language TTS**: Google Cloud TTS supporting English, Urdu, and Hindi
- **📺 YouTube Upload**: Automatic video upload to YouTube channel after generation
- **⚡ Async Processing**: Background job processing with real-time progress updates
- **☁️ Cloud Storage**: Google Cloud Storage integration for scalable file management
- **🎨 Modern Frontend**: React-based web interface with real-time updates
- **🔧 Production Ready**: Comprehensive error handling and monitoring

## 📡 API Endpoints

### Video Generation
- **POST** `/api/jobs`
  - Form (multipart/form-data):
    - `source_image` (file)
    - `driven_audio` (file)
    - Optional fields: `preprocess`, `still_mode`, `use_enhancer`, `batch_size`, `size`, `pose_style`
    - YouTube fields: `upload_to_youtube`, `youtube_title`, `youtube_description`, `youtube_tags`, `youtube_privacy`
  - Response: `{ "status": "ok", "job_id": "<uuid>" }`

- **GET** `/api/jobs/{job_id}`
  - Response: `{ status, progress, result_path?, s3_url?, error?, last_event? }`

### Text-to-Speech
- **POST** `/api/text-to-speech`
  - JSON body: `{ "text": "Your text", "language_code": "en-US" }`
  - Response: `{ "status": "success", "audio_data": "base64_encoded_mp3", "filename": "..." }`

### YouTube Integration
- **GET** `/api/youtube/auth`
  - Initialize YouTube OAuth flow
  - Response: `{ "auth_url": "...", "message": "..." }`

- **POST** `/api/youtube/auth/callback`
  - Complete YouTube OAuth with authorization code
  - Body: `{ "auth_code": "..." }`
  - Response: `{ "success": true, "message": "..." }`

### System Health
- **GET** `/api/health`
  - Response: `{ "status": "healthy", "message": "API is running", "active_jobs": 0 }`

## 🌍 Supported Languages

### Text-to-Speech Languages
- **🇺🇸 English (US)**: `en-US` - High-quality American English voices
- **🇵🇰 Urdu (Pakistan)**: `ur-PK` - Natural Urdu speech synthesis  
- **🇮🇳 Hindi (India)**: `hi-IN` - Clear Hindi voice generation

### Voice Options
Each language includes multiple voice options:
- **English**: 18 voices (US, UK, Australian accents, Male/Female)
- **Urdu**: 4 voices (Pakistani Urdu, Male/Female)
- **Hindi**: 4 voices (Indian Hindi, Male/Female)

## 📺 YouTube Integration Setup

### Prerequisites
1. Google Cloud Console account
2. YouTube channel
3. YouTube Data API v3 enabled

### Quick Setup
1. **Create OAuth Credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing
   - Enable YouTube Data API v3
   - Create OAuth 2.0 credentials (Desktop application)
   - Download JSON file as `youtube_client_secrets.json`

2. **Configure OAuth Consent Screen**:
   - Add your email as test user
   - Add YouTube Data API v3 scope

3. **First Time Authorization**:
   ```bash
   python real_api_server.py
   # Open http://localhost:7860
   # Go to Create Job tab
   # Check "Upload to YouTube after generation"
   # Click "Setup YouTube Authorization"
   # Complete OAuth flow
   ```

### Usage
```bash
# Create job with YouTube upload
curl -X POST http://localhost:7860/api/jobs \
  -F "source_image=@image.jpg" \
  -F "driven_audio=@audio.wav" \
  -F "upload_to_youtube=true" \
  -F "youtube_title=My Video" \
  -F "youtube_description=Video description" \
  -F "youtube_tags=AI,SadTalker" \
  -F "youtube_privacy=private"
```

**Detailed setup guide**: See [YOUTUBE_SETUP_GUIDE.md](YOUTUBE_SETUP_GUIDE.md)

## 🔧 Configuration

### Google Cloud Setup
- **Service Account**: `revoiz-ai-dd6bb5e7b3ee.json` (Text-to-Speech API enabled)
- **Storage Bucket**: `gcs-vodacast-bucket` for video file storage
- **Authentication**: Automatic OAuth2 token generation

### Environment Variables
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account JSON
- `GCS_BUCKET_NAME`: Google Cloud Storage bucket name

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Google Cloud Credentials
```bash
# Ensure your service account JSON is in place
cp revoiz-ai-dd6bb5e7b3ee.json gcs_credentials.json
```

### 3. Start the API Server
```bash
# Development
python real_api_server.py

# Production
uvicorn real_api_server:app --host 0.0.0.0 --port 7860
```

### 4. Access the Frontend
```bash
# Open in browser
open sadtalker-frontend-demo/demo.html
```

## 🧪 Testing the System

For comprehensive testing instructions, see the [**TESTING_GUIDE.md**](TESTING_GUIDE.md) file.

### Quick Test Commands:
```bash
# Test all APIs automatically
python test_apis.py

# Or test manually with the frontend
# 1. Start server: python real_api_server.py
# 2. Open: sadtalker-frontend-demo/demo.html
```

## 🧪 Testing the APIs

### Method 1: Using the Frontend Demo (Recommended)

#### Step 1: Start the API Server
```bash
# In terminal/command prompt
cd C:\Users\alira\OneDrive\Desktop\Internship Projects\Vodcast
python real_api_server.py
```

You should see:
```
🚀 Starting Real SadTalker API server on http://localhost:7860
📝 Available endpoints:
   GET  /api/health - Health check
   POST /api/text-to-speech - Convert text to speech
   POST /api/jobs - Create a new job
   GET  /api/jobs - List all jobs
   GET  /api/jobs/<job_id> - Get job status
   GET  /api/results/<job_id>/<filename> - Download result files

🧪 You can now test with Postman or run test_api.py
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:7860
 * Running on http://[your-ip]:7860
```

#### Step 2: Open the Frontend Demo
```bash
# Open the demo.html file in your browser
# Path: sadtalker-frontend-demo/demo.html
```

Or double-click on `sadtalker-frontend-demo/demo.html` in your file explorer.

#### Step 3: Test the Features

**🌍 Text-to-Speech Testing:**
1. Go to the "Text-to-Speech" tab in the demo
2. Select a language (English, Urdu, Hindi)
3. Enter text in the text area
4. Click "Generate Speech"
5. The generated audio will be automatically loaded into the audio file input

**🎭 Video Generation Testing:**
1. Go to the "Create Job" tab
2. Upload a source image (PNG, JPG, JPEG)
3. Upload or generate audio using TTS
4. Configure parameters (optional)
5. Click "Create Job"
6. Monitor progress in "Job Status" tab
7. Download the generated video when complete

### Method 2: Using API Testing Tools

#### Using cURL Commands

**Health Check:**
```bash
curl -X GET http://localhost:7860/api/health
```

**Text-to-Speech (English):**
```bash
curl -X POST http://localhost:7860/api/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test of the API",
    "language_code": "en-US"
  }'
```

**Text-to-Speech (Urdu):**
```bash
curl -X POST http://localhost:7860/api/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "السلام علیکم، یہ API کا ٹیسٹ ہے",
    "language_code": "ur-PK"
  }'
```

**Text-to-Speech (Hindi):**
```bash
curl -X POST http://localhost:7860/api/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्ते, यह API का परीक्षण है",
    "language_code": "hi-IN"
  }'
```

**Create Video Job:**
```bash
curl -X POST http://localhost:7860/api/jobs \
  -F "source_image=@examples/source_image/people_0.png" \
  -F "driven_audio=@examples/driven_audio/imagine.wav" \
  -F "preprocess=crop" \
  -F "still_mode=false" \
  -F "use_enhancer=false"
```

**Check Job Status:**
```bash
curl -X GET http://localhost:7860/api/jobs/{job_id}
```

#### Using Postman

1. **Import Collection**: Import the API collection if available
2. **Set Base URL**: `http://localhost:7860`
3. **Test Endpoints**:
   - `GET /api/health`
   - `POST /api/text-to-speech`
   - `POST /api/jobs`
   - `GET /api/jobs/{job_id}`

### Method 3: Using Python Scripts

Create a test script `test_apis.py`:

```python
import requests
import json
import time

# Base URL
BASE_URL = "http://localhost:7860"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/api/health")
    print("Health Check:", response.json())
    return response.status_code == 200

def test_text_to_speech():
    """Test TTS endpoint"""
    data = {
        "text": "Hello, this is a test",
        "language_code": "en-US"
    }
    response = requests.post(f"{BASE_URL}/api/text-to-speech", json=data)
    print("TTS Response:", response.json())
    return response.status_code == 200

def test_create_job():
    """Test job creation"""
    files = {
        'source_image': open('examples/source_image/people_0.png', 'rb'),
        'driven_audio': open('examples/driven_audio/imagine.wav', 'rb')
    }
    data = {
        'preprocess': 'crop',
        'still_mode': 'false',
        'use_enhancer': 'false'
    }
    
    response = requests.post(f"{BASE_URL}/api/jobs", files=files, data=data)
    result = response.json()
    print("Job Created:", result)
    
    # Close files
    files['source_image'].close()
    files['driven_audio'].close()
    
    return result.get('job_id')

def test_job_status(job_id):
    """Test job status checking"""
    response = requests.get(f"{BASE_URL}/api/jobs/{job_id}")
    print("Job Status:", response.json())
    return response.json()

if __name__ == "__main__":
    print("🧪 Testing SadTalker APIs...")
    
    # Test health
    if test_health():
        print("✅ Health check passed")
    else:
        print("❌ Health check failed")
        exit(1)
    
    # Test TTS
    if test_text_to_speech():
        print("✅ TTS test passed")
    else:
        print("❌ TTS test failed")
    
    # Test job creation
    job_id = test_create_job()
    if job_id:
        print(f"✅ Job created: {job_id}")
        
        # Monitor job status
        for i in range(10):  # Check for 10 iterations
            status = test_job_status(job_id)
            if status.get('status') == 'completed':
                print("✅ Job completed successfully!")
                break
            elif status.get('status') == 'failed':
                print("❌ Job failed")
                break
            time.sleep(5)  # Wait 5 seconds
    else:
        print("❌ Job creation failed")
```

Run the test script:
```bash
python test_apis.py
```

## 🔧 Troubleshooting

### Common Issues

#### 1. **Server Won't Start**
```bash
# Check if port 7860 is available
netstat -an | findstr 7860

# Try a different port
python real_api_server.py --port 8000
```

#### 2. **Google Cloud Authentication Error**
```bash
# Verify credentials file exists
ls -la revoiz-ai-dd6bb5e7b3ee.json

# Check environment variable
echo $GOOGLE_APPLICATION_CREDENTIALS
```

#### 3. **Frontend Can't Connect to API**
- Ensure API server is running on `http://localhost:7860`
- Check browser console for CORS errors
- Verify the API_BASE_URL in demo.html

#### 4. **File Upload Issues**
- Check file size limits
- Verify file formats (PNG, JPG, JPEG for images; WAV, MP3, MP4 for audio)
- Ensure uploads directory exists and is writable

#### 5. **Job Processing Stuck**
- Check SadTalker model files in `checkpoints/`
- Verify `inference.py` is working
- Check system resources (CPU/Memory)

### Debug Mode
```bash
# Run with debug logging
python real_api_server.py --debug

# Check logs
tail -f logs/api.log
```

## 🎮 Usage Examples

### Text-to-Speech API
```javascript
// Generate English speech
const response = await fetch('/api/text-to-speech', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "Hello, this is a test",
    language_code: "en-US"
  })
});

// Generate Urdu speech
const urduResponse = await fetch('/api/text-to-speech', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "السلام علیکم، یہ ٹیسٹ ہے",
    language_code: "ur-PK"
  })
});
```

### Video Generation
```javascript
// Create talking face video
const formData = new FormData();
formData.append('source_image', imageFile);
formData.append('driven_audio', audioFile);

const job = await fetch('/api/jobs', {
  method: 'POST',
  body: formData
});
```

## Minimal React usage

```tsx
// api.ts
export async function startJob(baseUrl: string, data: FormData) {
  const res = await fetch(`${baseUrl}/api/jobs`, { method: 'POST', body: data });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ status: string; job_id: string }>; 
}

export function subscribeProgress(wsBaseUrl: string, jobId: string, onMessage: (evt: any) => void) {
  const ws = new WebSocket(`${wsBaseUrl.replace(/^http/, 'ws')}/ws/jobs/${jobId}`);
  ws.onmessage = (e) => onMessage(JSON.parse(e.data));
  return () => ws.close();
}
```

```tsx
// useGenerateVideo.tsx
import { useCallback, useEffect, useRef, useState } from 'react';
import { startJob, subscribeProgress } from './api';

export function useGenerateVideo(apiBase = 'http://localhost:7860') {
  const [jobId, setJobId] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const [status, setStatus] = useState<'idle' | 'running' | 'done' | 'error'>('idle');
  const [s3Url, setS3Url] = useState<string | null>(null);
  const unsub = useRef<() => void>();

  const generate = useCallback(async (sourceFile: File, audioFile: File, options?: Partial<{ preprocess: string; still_mode: boolean; use_enhancer: boolean; batch_size: number; size: number; pose_style: number }>) => {
    const form = new FormData();
    form.append('source_image', sourceFile);
    form.append('driven_audio', audioFile);
    if (options?.preprocess) form.append('preprocess', String(options.preprocess));
    if (options?.still_mode != null) form.append('still_mode', String(options.still_mode));
    if (options?.use_enhancer != null) form.append('use_enhancer', String(options.use_enhancer));
    if (options?.batch_size != null) form.append('batch_size', String(options.batch_size));
    if (options?.size != null) form.append('size', String(options.size));
    if (options?.pose_style != null) form.append('pose_style', String(options.pose_style));

    const { job_id } = await startJob(apiBase, form);
    setJobId(job_id);
    setStatus('running');

    unsub.current?.();
    unsub.current = subscribeProgress(apiBase, job_id, (evt) => {
      if (typeof evt.progress === 'number') setProgress(evt.progress);
      if (evt.stage === 'done') {
        setStatus('done');
        if (evt.s3_url) setS3Url(evt.s3_url);
      }
      if (evt.stage === 'error') {
        setStatus('error');
      }
    });
  }, [apiBase]);

  useEffect(() => () => { unsub.current?.(); }, []);

  return { generate, jobId, progress, status, s3Url };
}
```

## Performance recommendations

- Keep models loaded in GPU worker processes, 1 per GPU; consume jobs from a queue (Redis/RQ or Celery).
- Pre-warm models at startup; enable mixed precision (AMP) where safe; ensure fast disk for temp files.
- Store outputs in S3 and serve via CDN; limit maximum input duration to keep latency predictable.


