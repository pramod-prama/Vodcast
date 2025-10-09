# 🧪 SadTalker API Testing Guide

This guide provides comprehensive instructions for testing the SadTalker API server and frontend demo.

## 📋 Prerequisites

- Python 3.8+ installed
- Google Cloud credentials set up
- All dependencies installed (`pip install -r requirements.txt`)

## 🚀 Quick Testing Setup

### Step 1: Start the API Server
```bash
# Navigate to project directory
cd C:\Users\alira\OneDrive\Desktop\Internship Projects\Vodcast

# Start the server
python real_api_server.py
```

**Expected Output:**
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

### Step 2: Open Frontend Demo
```bash
# Open demo.html in your browser
# Path: sadtalker-frontend-demo/demo.html
```

Or simply double-click on `sadtalker-frontend-demo/demo.html` in your file explorer.

---

## 🎯 Testing Methods

### Method 1: Frontend Demo Testing (Recommended)

#### 🌍 Text-to-Speech Testing

1. **Open the Demo**: Navigate to `sadtalker-frontend-demo/demo.html`
2. **Go to TTS Tab**: Click on "Text-to-Speech" tab
3. **Select Language**: Choose from dropdown:
   - 🇺🇸 English (en-US)
   - 🇵🇰 Urdu (ur-PK) 
   - 🇮🇳 Hindi (hi-IN)
4. **Enter Text**: Type your text in the text area
5. **Generate Speech**: Click "Generate Speech" button
6. **Verify Output**: Audio should be generated and loaded automatically

**Test Examples:**
- **English**: "Hello, this is a test of the text-to-speech API"
- **Urdu**: "السلام علیکم، یہ ٹیکسٹ ٹو اسپیچ API کا ٹیسٹ ہے"
- **Hindi**: "नमस्ते, यह टेक्स्ट-टू-स्पीच API का परीक्षण है"

#### 🎭 Video Generation Testing

1. **Go to Create Job Tab**: Click on "Create Job" tab
2. **Upload Source Image**: 
   - Click "Choose Image File"
   - Select an image from `examples/source_image/` or upload your own
   - Supported formats: PNG, JPG, JPEG
3. **Upload Audio**:
   - Option A: Use generated TTS audio (from previous step)
   - Option B: Upload audio file from `examples/driven_audio/`
   - Supported formats: WAV, MP3, MP4
4. **Configure Parameters** (Optional):
   - Preprocess: crop, full, resize
   - Still Mode: true/false
   - Use Enhancer: true/false
   - Batch Size: 1
   - Size: 256 or 512
   - Pose Style: 0-45
5. **Create Job**: Click "Create Job" button
6. **Monitor Progress**: 
   - Go to "Job Status" tab
   - Enter the job ID
   - Click "Check Status"
   - Watch progress updates
7. **Download Result**: When completed, download the generated video

#### 📊 Job Management Testing

1. **View All Jobs**: Go to "All Jobs" tab to see all created jobs
2. **Check Individual Status**: Use "Job Status" tab with specific job ID
3. **Download Results**: Access completed videos via download links

---

### Method 2: API Testing with cURL

#### Health Check
```bash
curl -X GET http://localhost:7860/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "SadTalker API is running",
  "timestamp": 1757876421.1140838,
  "active_jobs": 0
}
```

#### Text-to-Speech Testing

**English TTS:**
```bash
curl -X POST http://localhost:7860/api/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test of the API",
    "language_code": "en-US"
  }'
```

**Urdu TTS:**
```bash
curl -X POST http://localhost:7860/api/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "السلام علیکم، یہ API کا ٹیسٹ ہے",
    "language_code": "ur-PK"
  }'
```

**Hindi TTS:**
```bash
curl -X POST http://localhost:7860/api/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्ते, यह API का परीक्षण है",
    "language_code": "hi-IN"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Text converted to speech successfully in English (US)",
  "audio_data": "base64_encoded_mp3_data",
  "filename": "generated_speech_en-US_1234567890.mp3",
  "language_code": "en-US",
  "language_name": "English (US)",
  "file_size": 12345,
  "audio_format": "mp3"
}
```

#### Video Generation Testing

**Create Job:**
```bash
curl -X POST http://localhost:7860/api/jobs \
  -F "source_image=@examples/source_image/people_0.png" \
  -F "driven_audio=@examples/driven_audio/imagine.wav" \
  -F "preprocess=crop" \
  -F "still_mode=false" \
  -F "use_enhancer=false"
```

**Expected Response:**
```json
{
  "job_id": "a8435aad-1a00-4eb0-b751-282b30d2b21e",
  "status": "created",
  "message": "Job created successfully"
}
```

**Check Job Status:**
```bash
curl -X GET http://localhost:7860/api/jobs/{job_id}
```

**Expected Response:**
```json
{
  "job_id": "a8435aad-1a00-4eb0-b751-282b30d2b21e",
  "status": "processing",
  "progress": 45,
  "created_at": 1757876421.1140838,
  "preprocess": "crop",
  "still_mode": "false",
  "use_enhancer": "false",
  "batch_size": "1",
  "size": "256",
  "pose_style": "0",
  "image_path": "uploads/...",
  "audio_path": "uploads/..."
}
```

---

### Method 3: Python Script Testing

Create a test script `test_apis.py`:

```python
import requests
import json
import time
import base64

# Base URL
BASE_URL = "http://localhost:7860"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_text_to_speech():
    """Test TTS endpoint with multiple languages"""
    print("\n🎤 Testing Text-to-Speech...")
    
    test_cases = [
        {
            "text": "Hello, this is a test of the API",
            "language_code": "en-US",
            "language_name": "English"
        },
        {
            "text": "السلام علیکم، یہ API کا ٹیسٹ ہے",
            "language_code": "ur-PK", 
            "language_name": "Urdu"
        },
        {
            "text": "नमस्ते, यह API का परीक्षण है",
            "language_code": "hi-IN",
            "language_name": "Hindi"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n  Testing {test_case['language_name']} TTS...")
        response = requests.post(f"{BASE_URL}/api/text-to-speech", json=test_case)
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ {test_case['language_name']} TTS successful")
            print(f"  📁 File: {result['filename']}")
            print(f"  📊 Size: {result['file_size']} bytes")
        else:
            print(f"  ❌ {test_case['language_name']} TTS failed: {response.text}")
    
    return True

def test_create_job():
    """Test job creation"""
    print("\n🎬 Testing job creation...")
    
    try:
        files = {
            'source_image': open('examples/source_image/people_0.png', 'rb'),
            'driven_audio': open('examples/driven_audio/imagine.wav', 'rb')
        }
        data = {
            'preprocess': 'crop',
            'still_mode': 'false',
            'use_enhancer': 'false',
            'batch_size': '1',
            'size': '256',
            'pose_style': '0'
        }
        
        response = requests.post(f"{BASE_URL}/api/jobs", files=files, data=data)
        result = response.json()
        
        # Close files
        files['source_image'].close()
        files['driven_audio'].close()
        
        if response.status_code == 200:
            print(f"  ✅ Job created successfully")
            print(f"  🆔 Job ID: {result['job_id']}")
            return result['job_id']
        else:
            print(f"  ❌ Job creation failed: {response.text}")
            return None
            
    except FileNotFoundError as e:
        print(f"  ❌ File not found: {e}")
        return None

def test_job_status(job_id):
    """Test job status checking"""
    print(f"\n📊 Testing job status for {job_id}...")
    
    response = requests.get(f"{BASE_URL}/api/jobs/{job_id}")
    
    if response.status_code == 200:
        status = response.json()
        print(f"  📈 Status: {status['status']}")
        print(f"  📊 Progress: {status.get('progress', 0)}%")
        
        if status['status'] == 'completed':
            print(f"  ✅ Job completed!")
            if 's3_url' in status:
                print(f"  🔗 Video URL: {status['s3_url']}")
        elif status['status'] == 'failed':
            print(f"  ❌ Job failed: {status.get('error', 'Unknown error')}")
        
        return status
    else:
        print(f"  ❌ Status check failed: {response.text}")
        return None

def monitor_job(job_id, max_checks=20):
    """Monitor job until completion"""
    print(f"\n⏳ Monitoring job {job_id}...")
    
    for i in range(max_checks):
        status = test_job_status(job_id)
        
        if not status:
            break
            
        if status['status'] in ['completed', 'failed']:
            break
            
        print(f"  ⏱️  Waiting 10 seconds... (Check {i+1}/{max_checks})")
        time.sleep(10)
    
    return status

def test_list_jobs():
    """Test listing all jobs"""
    print("\n📋 Testing job listing...")
    
    response = requests.get(f"{BASE_URL}/api/jobs")
    
    if response.status_code == 200:
        result = response.json()
        print(f"  ✅ Found {result['total']} jobs")
        for job in result['jobs']:
            print(f"    🆔 {job['job_id'][:8]}... - {job['status']} ({job.get('progress', 0)}%)")
    else:
        print(f"  ❌ Job listing failed: {response.text}")

if __name__ == "__main__":
    print("🧪 SadTalker API Testing Suite")
    print("=" * 50)
    
    # Test health
    if not test_health():
        print("❌ Health check failed. Make sure the server is running.")
        exit(1)
    
    # Test TTS
    test_text_to_speech()
    
    # Test job creation
    job_id = test_create_job()
    
    if job_id:
        # Monitor job
        final_status = monitor_job(job_id)
        
        # Test job listing
        test_list_jobs()
        
        print("\n🎉 Testing completed!")
        if final_status and final_status['status'] == 'completed':
            print("✅ All tests passed successfully!")
        else:
            print("⚠️  Some tests may have issues. Check the logs above.")
    else:
        print("\n❌ Job creation failed. Check your setup.")
```

**Run the test script:**
```bash
python test_apis.py
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. **Server Won't Start**
```bash
# Check if port is in use
netstat -an | findstr 7860

# Try different port
python real_api_server.py --port 8000
```

#### 2. **Google Cloud Authentication Error**
```bash
# Verify credentials file
ls -la revoiz-ai-dd6bb5e7b3ee.json

# Check environment variable
echo $GOOGLE_APPLICATION_CREDENTIALS
```

#### 3. **Frontend Can't Connect**
- Ensure API server is running on `http://localhost:7860`
- Check browser console for errors
- Verify CORS settings

#### 4. **File Upload Issues**
- Check file formats (PNG, JPG, JPEG for images)
- Verify file sizes (not too large)
- Ensure uploads directory exists

#### 5. **Job Processing Stuck**
- Check SadTalker model files in `checkpoints/`
- Verify `inference.py` is working
- Check system resources

### Debug Commands

```bash
# Run with debug logging
python real_api_server.py --debug

# Check server logs
tail -f logs/api.log

# Test individual components
python inference.py --help
```

---

## 📊 Expected Test Results

### Successful Test Flow:
1. ✅ Health check returns 200 OK
2. ✅ TTS generates audio for all languages
3. ✅ Job creation returns job ID
4. ✅ Job status shows progress updates
5. ✅ Job completes with video URL
6. ✅ Video can be downloaded and played

### Performance Expectations:
- **TTS Generation**: 2-5 seconds per request
- **Video Generation**: 30-120 seconds depending on system
- **File Upload**: < 5 seconds for typical files
- **Status Updates**: Real-time via polling

---

## 🎯 Test Checklist

- [ ] API server starts successfully
- [ ] Health endpoint responds
- [ ] TTS works for English
- [ ] TTS works for Urdu  
- [ ] TTS works for Hindi
- [ ] Job creation works
- [ ] Job status monitoring works
- [ ] Video generation completes
- [ ] Frontend demo loads
- [ ] Frontend can create jobs
- [ ] Frontend can monitor progress
- [ ] Generated videos are playable

---

This testing guide ensures comprehensive validation of all API endpoints and frontend functionality. Follow the steps in order for best results!
