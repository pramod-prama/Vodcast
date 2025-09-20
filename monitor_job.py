#!/usr/bin/env python3
"""
Monitor job progress in real-time
"""
import requests
import json
import time
import sys

API_BASE_URL = 'http://localhost:7860'
JOB_ID = '1b6addb0-43d4-412b-a67a-e1865b291af1'

def monitor_job():
    """Monitor job progress"""
    print(f"🔍 Monitoring job: {JOB_ID}")
    print("Press Ctrl+C to stop monitoring")
    print("-" * 50)
    
    try:
        while True:
            response = requests.get(f"{API_BASE_URL}/api/jobs/{JOB_ID}")
            if response.status_code == 200:
                data = response.json()
                status = data['status']
                progress = data['progress']
                
                # Create progress bar
                bar_length = 30
                filled_length = int(bar_length * progress / 100)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                
                print(f"\rStatus: {status:12} | Progress: {progress:3}% |{bar}|", end='', flush=True)
                
                if status in ['completed', 'failed']:
                    print(f"\n\n🎉 Job {status}!")
                    if status == 'completed':
                        print(f"✅ Result available at: {data.get('s3_url', 'N/A')}")
                    elif status == 'failed':
                        print(f"❌ Error: {data.get('error', 'Unknown error')}")
                    break
                    
            else:
                print(f"\n❌ Failed to get job status: {response.status_code}")
                break
                
            time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error monitoring job: {e}")

if __name__ == "__main__":
    monitor_job()
