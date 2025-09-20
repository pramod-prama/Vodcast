#!/usr/bin/env python3
"""
Test script for SadTalker API endpoints and WebSocket
"""
import requests
import json
import time
import websocket
import threading
from pathlib import Path

API_BASE = "http://localhost:7860"

def test_create_job():
    """Test job creation"""
    print("🚀 Creating job...")
    
    # Use example files
    image_path = "examples/source_image/people_0.png"
    audio_path = "examples/driven_audio/bus_chinese.wav"
    
    if not Path(image_path).exists():
        print(f"❌ Image not found: {image_path}")
        return None
        
    if not Path(audio_path).exists():
        print(f"❌ Audio not found: {audio_path}")
        return None
    
    files = {
        'source_image': open(image_path, 'rb'),
        'driven_audio': open(audio_path, 'rb')
    }
    
    data = {
        'preprocess': 'crop',
        'still_mode': 'false',
        'use_enhancer': 'false',
        'batch_size': '1',
        'size': '256',
        'pose_style': '0'
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/jobs", files=files, data=data)
        files['source_image'].close()
        files['driven_audio'].close()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Job created: {result['job_id']}")
            return result['job_id']
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_get_job_status(job_id):
    """Test job status polling"""
    print(f"📊 Checking status for job: {job_id}")
    
    try:
        response = requests.get(f"{API_BASE}/api/jobs/{job_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {result['status']}, Progress: {result['progress']}%")
            if result.get('s3_url'):
                print(f"🎥 S3 URL: {result['s3_url']}")
            if result.get('result_path'):
                print(f"📁 Local Path: {result['result_path']}")
            return result
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def on_ws_message(ws, message):
    """Handle WebSocket messages"""
    try:
        data = json.loads(message)
        print(f"📡 WebSocket: {data}")
        
        # Check for video URLs
        if data.get('s3_url'):
            print(f"🎥 S3 Video URL: {data['s3_url']}")
        if data.get('output_path'):
            print(f"📁 Local Video Path: {data['output_path']}")
        if data.get('stage') == 'done':
            print("✅ Generation Complete!")
            ws.close()
    except Exception as e:
        print(f"❌ WebSocket error: {e}")

def test_websocket(job_id):
    """Test WebSocket connection"""
    print(f"🔌 Connecting to WebSocket for job: {job_id}")
    
    ws_url = f"ws://localhost:7860/ws/jobs/{job_id}"
    
    try:
        ws = websocket.WebSocketApp(ws_url, on_message=on_ws_message)
        ws.run_forever()
    except Exception as e:
        print(f"❌ WebSocket exception: {e}")

def main():
    print("🧪 Testing SadTalker API...")
    print("=" * 50)
    
    # Test 1: Create job
    job_id = test_create_job()
    if not job_id:
        print("❌ Failed to create job, exiting")
        return
    
    print("\n" + "=" * 50)
    
    # Test 2: Poll status a few times
    for i in range(3):
        print(f"\n📊 Poll #{i+1}:")
        test_get_job_status(job_id)
        time.sleep(2)
    
    print("\n" + "=" * 50)
    
    # Test 3: WebSocket (this will block until completion)
    print("🔌 Starting WebSocket monitoring...")
    test_websocket(job_id)
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    main()

