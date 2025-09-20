#!/usr/bin/env python3
"""
Test the fixed SadTalker API with correct parameters
"""
import requests
import json
import time

API_BASE_URL = 'http://localhost:7860'

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_create_job():
    """Test job creation with sample files"""
    print("\n🚀 Testing job creation...")
    
    # Use sample files from the examples directory
    image_path = "examples/source_image/people_0.png"
    audio_path = "examples/driven_audio/bus_chinese.wav"
    
    try:
        with open(image_path, 'rb') as img_file, open(audio_path, 'rb') as aud_file:
            files = {
                'source_image': ('people_0.png', img_file, 'image/png'),
                'driven_audio': ('bus_chinese.wav', aud_file, 'audio/wav')
            }
            
            data = {
                'preprocess': 'crop',
                'still_mode': 'false',
                'use_enhancer': 'false',
                'batch_size': '1',
                'size': '256',
                'pose_style': '0'
            }
            
            response = requests.post(f"{API_BASE_URL}/api/jobs", files=files, data=data)
            
            if response.status_code == 200:
                job_data = response.json()
                print(f"✅ Job created successfully: {job_data['job_id']}")
                return job_data['job_id']
            else:
                print(f"❌ Job creation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
    except FileNotFoundError as e:
        print(f"❌ Sample files not found: {e}")
        return None
    except Exception as e:
        print(f"❌ Job creation error: {e}")
        return None

def test_job_status(job_id):
    """Test job status checking"""
    print(f"\n📊 Testing job status for {job_id}...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/jobs/{job_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Job status: {data['status']} ({data['progress']}%)")
            if 'error' in data:
                print(f"⚠️  Error: {data['error']}")
            return data
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Status check error: {e}")
        return None

def test_list_jobs():
    """Test listing all jobs"""
    print("\n📋 Testing job listing...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/jobs")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total']} jobs")
            for job in data['jobs']:
                print(f"   - {job['job_id']}: {job['status']} ({job['progress']}%)")
            return True
        else:
            print(f"❌ Job listing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Job listing error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Fixed SadTalker API")
    print("=" * 50)
    
    # Test health
    if not test_health():
        print("\n❌ API is not running. Please start the server first.")
        return
    
    # Test job creation
    job_id = test_create_job()
    if not job_id:
        print("\n❌ Job creation failed. Stopping tests.")
        return
    
    # Test job status
    test_job_status(job_id)
    
    # Test job listing
    test_list_jobs()
    
    print("\n⏳ Waiting for job to process...")
    print("   (Check the server logs for detailed processing information)")
    
    # Monitor job for a bit
    for i in range(10):
        time.sleep(2)
        status = test_job_status(job_id)
        if status and status['status'] in ['completed', 'failed']:
            break
    
    print("\n✅ API testing completed!")
    print("   Check the server logs for detailed command execution information.")

if __name__ == "__main__":
    main()
