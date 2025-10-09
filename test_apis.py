#!/usr/bin/env python3
"""
SadTalker API Testing Script
Comprehensive test suite for all API endpoints
"""

import requests
import json
import time
import base64
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:7860"
TIMEOUT = 30

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print formatted step"""
    print(f"\n{step}. {description}")
    print("-" * 40)

def test_health():
    """Test health endpoint"""
    print_step("1", "Testing Health Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check Passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Active Jobs: {data.get('active_jobs', 0)}")
            return True
        else:
            print(f"❌ Health Check Failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        print("   Make sure the API server is running on http://localhost:7860")
        return False

def test_text_to_speech():
    """Test TTS endpoint with multiple languages"""
    print_step("2", "Testing Text-to-Speech API")
    
    test_cases = [
        {
            "text": "Hello, this is a test of the SadTalker API",
            "language_code": "en-US",
            "language_name": "English (US)"
        },
        {
            "text": "السلام علیکم، یہ SadTalker API کا ٹیسٹ ہے",
            "language_code": "ur-PK", 
            "language_name": "Urdu (Pakistan)"
        },
        {
            "text": "नमस्ते, यह SadTalker API का परीक्षण है",
            "language_code": "hi-IN",
            "language_name": "Hindi (India)"
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   {i}. Testing {test_case['language_name']} TTS...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/text-to-speech", 
                json=test_case, 
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ {test_case['language_name']} TTS successful")
                print(f"      📁 File: {result['filename']}")
                print(f"      📊 Size: {result['file_size']} bytes")
                print(f"      🎵 Format: {result['audio_format']}")
                success_count += 1
            else:
                print(f"   ❌ {test_case['language_name']} TTS failed")
                print(f"      Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {test_case['language_name']} TTS error: {e}")
    
    print(f"\n   📊 TTS Results: {success_count}/{len(test_cases)} successful")
    return success_count == len(test_cases)

def test_create_job():
    """Test job creation"""
    print_step("3", "Testing Job Creation")
    
    # Check if example files exist
    image_path = "examples/source_image/people_0.png"
    audio_path = "examples/driven_audio/imagine.wav"
    
    if not os.path.exists(image_path):
        print(f"❌ Example image not found: {image_path}")
        return None
        
    if not os.path.exists(audio_path):
        print(f"❌ Example audio not found: {audio_path}")
        return None
    
    print(f"   📁 Using image: {image_path}")
    print(f"   🎵 Using audio: {audio_path}")
    
    try:
        with open(image_path, 'rb') as img_file, open(audio_path, 'rb') as aud_file:
            files = {
                'source_image': img_file,
                'driven_audio': aud_file
            }
            data = {
                'preprocess': 'crop',
                'still_mode': 'false',
                'use_enhancer': 'false',
                'batch_size': '1',
                'size': '256',
                'pose_style': '0'
            }
            
            response = requests.post(
                f"{BASE_URL}/api/jobs", 
                files=files, 
                data=data, 
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Job created successfully")
                print(f"      🆔 Job ID: {result['job_id']}")
                print(f"      📊 Status: {result['status']}")
                return result['job_id']
            else:
                print(f"   ❌ Job creation failed")
                print(f"      Error: {response.text}")
                return None
                
    except FileNotFoundError as e:
        print(f"   ❌ File error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request error: {e}")
        return None

def test_job_status(job_id):
    """Test job status checking"""
    print(f"\n   📊 Checking job status for {job_id[:8]}...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/jobs/{job_id}", timeout=TIMEOUT)
        
        if response.status_code == 200:
            status = response.json()
            print(f"      📈 Status: {status['status']}")
            print(f"      📊 Progress: {status.get('progress', 0)}%")
            
            if status['status'] == 'completed':
                print(f"      ✅ Job completed successfully!")
                if 's3_url' in status:
                    print(f"      🔗 Video URL: {status['s3_url']}")
                return 'completed'
            elif status['status'] == 'failed':
                print(f"      ❌ Job failed: {status.get('error', 'Unknown error')}")
                return 'failed'
            else:
                return 'processing'
        else:
            print(f"      ❌ Status check failed: {response.text}")
            return 'error'
            
    except requests.exceptions.RequestException as e:
        print(f"      ❌ Request error: {e}")
        return 'error'

def monitor_job(job_id, max_checks=12):
    """Monitor job until completion"""
    print_step("4", "Monitoring Job Progress")
    print(f"   🆔 Job ID: {job_id}")
    print(f"   ⏱️  Max checks: {max_checks} (30 seconds each)")
    
    for i in range(max_checks):
        status = test_job_status(job_id)
        
        if status in ['completed', 'failed', 'error']:
            return status
            
        if i < max_checks - 1:  # Don't wait after last check
            print(f"      ⏳ Waiting 30 seconds... (Check {i+1}/{max_checks})")
            time.sleep(30)
    
    print(f"      ⏰ Timeout reached after {max_checks} checks")
    return 'timeout'

def test_list_jobs():
    """Test listing all jobs"""
    print_step("5", "Testing Job Listing")
    
    try:
        response = requests.get(f"{BASE_URL}/api/jobs", timeout=TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Job listing successful")
            print(f"      📊 Total jobs: {result['total']}")
            
            if result['jobs']:
                print(f"      📋 Recent jobs:")
                for job in result['jobs'][:5]:  # Show last 5 jobs
                    print(f"         🆔 {job['job_id'][:8]}... - {job['status']} ({job.get('progress', 0)}%)")
            else:
                print(f"      📋 No jobs found")
                
            return True
        else:
            print(f"   ❌ Job listing failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request error: {e}")
        return False

def main():
    """Main test function"""
    print_header("SadTalker API Testing Suite")
    print("This script will test all API endpoints and functionality.")
    print("Make sure the API server is running on http://localhost:7860")
    
    # Test results tracking
    results = {
        'health': False,
        'tts': False,
        'job_creation': False,
        'job_monitoring': False,
        'job_listing': False
    }
    
    # Test 1: Health Check
    results['health'] = test_health()
    if not results['health']:
        print("\n❌ Health check failed. Please start the API server first.")
        print("   Run: python real_api_server.py")
        return
    
    # Test 2: Text-to-Speech
    results['tts'] = test_text_to_speech()
    
    # Test 3: Job Creation
    job_id = test_create_job()
    results['job_creation'] = job_id is not None
    
    # Test 4: Job Monitoring (if job was created)
    if job_id:
        final_status = monitor_job(job_id)
        results['job_monitoring'] = final_status in ['completed', 'failed']
    else:
        print_step("4", "Skipping Job Monitoring (No job created)")
    
    # Test 5: Job Listing
    results['job_listing'] = test_list_jobs()
    
    # Print final results
    print_header("Test Results Summary")
    
    test_names = {
        'health': 'Health Check',
        'tts': 'Text-to-Speech',
        'job_creation': 'Job Creation',
        'job_monitoring': 'Job Monitoring',
        'job_listing': 'Job Listing'
    }
    
    passed = 0
    total = len(results)
    
    for test, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"   {test_names[test]}: {status}")
        if passed_test:
            passed += 1
    
    print(f"\n📊 Overall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your SadTalker API is working perfectly.")
    elif passed >= total * 0.8:
        print("⚠️  Most tests passed. Check failed tests above.")
    else:
        print("❌ Multiple tests failed. Please check your setup.")
    
    print(f"\n💡 Tips:")
    print(f"   - Make sure Google Cloud credentials are set up")
    print(f"   - Check that all model files are in checkpoints/")
    print(f"   - Verify example files exist in examples/")
    print(f"   - Check the API server logs for detailed error messages")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("   Please check your setup and try again")
