#!/usr/bin/env python3
"""
Check if the directory fix is working
"""
import os
import requests
import json
import time

API_BASE_URL = 'http://localhost:7860'
JOB_ID = 'df91d575-97d5-430f-87a4-530d38c7e99f'

def check_directory_structure():
    """Check if the directory structure was created correctly"""
    result_dir = os.path.join('results', JOB_ID)
    
    print(f"🔍 Checking directory structure for job: {JOB_ID}")
    print(f"📁 Result directory: {result_dir}")
    
    if os.path.exists(result_dir):
        print("✅ Main result directory exists")
        
        # List contents
        contents = os.listdir(result_dir)
        print(f"📋 Contents: {contents}")
        
        # Check for timestamped subdirectories
        timestamped_dirs = [d for d in contents if os.path.isdir(os.path.join(result_dir, d)) and '_' in d]
        if timestamped_dirs:
            print(f"✅ Found timestamped subdirectories: {timestamped_dirs}")
            
            # Check the first timestamped directory
            timestamped_dir = os.path.join(result_dir, timestamped_dirs[0])
            print(f"📁 Checking: {timestamped_dir}")
            
            if os.path.exists(timestamped_dir):
                sub_contents = os.listdir(timestamped_dir)
                print(f"📋 Subdirectory contents: {sub_contents}")
                
                # Look for .mat files (intermediate files)
                mat_files = [f for f in sub_contents if f.endswith('.mat')]
                if mat_files:
                    print(f"✅ Found .mat files: {mat_files}")
                else:
                    print("⚠️  No .mat files found yet")
        else:
            print("⚠️  No timestamped subdirectories found")
    else:
        print("❌ Main result directory does not exist")

def check_job_status():
    """Check current job status"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/jobs/{JOB_ID}")
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Job Status:")
            print(f"   Status: {data['status']}")
            print(f"   Progress: {data['progress']}%")
            if 'error' in data:
                print(f"   Error: {data['error']}")
            return data
        else:
            print(f"❌ Failed to get job status: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error checking job status: {e}")
        return None

def main():
    print("🔧 Checking Directory Fix")
    print("=" * 50)
    
    check_directory_structure()
    check_job_status()
    
    print("\n⏳ Waiting 10 seconds and checking again...")
    time.sleep(10)
    
    print("\n" + "=" * 50)
    check_directory_structure()
    check_job_status()

if __name__ == "__main__":
    main()
