#!/usr/bin/env python3
"""
Check job status and show detailed information
"""
import requests
import json
import time

API_BASE_URL = 'http://localhost:7860'
JOB_ID = '1b6addb0-43d4-412b-a67a-e1865b291af1'

def check_job_status():
    """Check and display job status"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/jobs/{JOB_ID}")
        if response.status_code == 200:
            data = response.json()
            print(f"Job ID: {data['job_id']}")
            print(f"Status: {data['status']}")
            print(f"Progress: {data['progress']}%")
            print(f"Created: {time.ctime(data['created_at'])}")
            print(f"Image: {data['image_path']}")
            print(f"Audio: {data['audio_path']}")
            print(f"Parameters:")
            print(f"  - Preprocess: {data['preprocess']}")
            print(f"  - Still Mode: {data['still_mode']}")
            print(f"  - Use Enhancer: {data['use_enhancer']}")
            print(f"  - Batch Size: {data['batch_size']}")
            print(f"  - Size: {data['size']}")
            print(f"  - Pose Style: {data['pose_style']}")
            
            if 'error' in data:
                print(f"Error: {data['error']}")
            
            if 'result_path' in data:
                print(f"Result: {data['result_path']}")
            
            if 's3_url' in data:
                print(f"Download URL: {data['s3_url']}")
                
        else:
            print(f"Failed to get job status: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error checking job status: {e}")

if __name__ == "__main__":
    check_job_status()
