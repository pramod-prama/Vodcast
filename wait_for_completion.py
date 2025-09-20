#!/usr/bin/env python3
"""
Wait for job completion and show detailed status
"""
import requests
import json
import time
import os

API_BASE_URL = 'http://localhost:7860'
JOB_ID = 'df91d575-97d5-430f-87a4-530d38c7e99f'

def wait_for_completion():
    """Wait for job to complete or fail"""
    print(f"⏳ Waiting for job completion: {JOB_ID}")
    print("Press Ctrl+C to stop monitoring")
    print("-" * 60)
    
    start_time = time.time()
    last_progress = 0
    
    try:
        while True:
            response = requests.get(f"{API_BASE_URL}/api/jobs/{JOB_ID}")
            if response.status_code == 200:
                data = response.json()
                status = data['status']
                progress = data['progress']
                elapsed = time.time() - start_time
                
                # Show progress bar
                bar_length = 30
                filled_length = int(bar_length * progress / 100)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                
                print(f"\r[{elapsed:6.1f}s] {status:12} | {progress:3}% |{bar}|", end='', flush=True)
                
                # Check if progress changed
                if progress != last_progress:
                    print(f"\n📈 Progress updated: {last_progress}% → {progress}%")
                    last_progress = progress
                
                # Check for completion or failure
                if status in ['completed', 'failed']:
                    print(f"\n\n🎉 Job {status.upper()}!")
                    print(f"⏱️  Total time: {elapsed:.1f} seconds")
                    
                    if status == 'completed':
                        print(f"✅ Result available at: {data.get('s3_url', 'N/A')}")
                        print(f"📁 Result path: {data.get('result_path', 'N/A')}")
                    elif status == 'failed':
                        print(f"❌ Error: {data.get('error', 'Unknown error')}")
                    
                    # Check directory contents
                    result_dir = os.path.join('results', JOB_ID)
                    if os.path.exists(result_dir):
                        print(f"\n📁 Result directory contents:")
                        for root, dirs, files in os.walk(result_dir):
                            level = root.replace(result_dir, '').count(os.sep)
                            indent = ' ' * 2 * level
                            print(f"{indent}{os.path.basename(root)}/")
                            subindent = ' ' * 2 * (level + 1)
                            for file in files:
                                print(f"{subindent}{file}")
                    
                    break
                
                # Timeout after 10 minutes
                if elapsed > 600:
                    print(f"\n⏰ Timeout after 10 minutes")
                    break
                    
            else:
                print(f"\n❌ Failed to get job status: {response.status_code}")
                break
                
            time.sleep(5)
            
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error monitoring job: {e}")

if __name__ == "__main__":
    wait_for_completion()
