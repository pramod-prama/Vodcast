#!/usr/bin/env python3
"""
Test the directory fix by checking the structure
"""
import os
import requests
import json
import time

API_BASE_URL = 'http://localhost:7860'
JOB_ID = 'bfee37b4-0510-47c8-be02-79a4d7f5f06e'

def check_directory_structure():
    """Check the directory structure"""
    result_dir = os.path.join('results', JOB_ID)
    
    print(f"🔍 Checking directory structure for job: {JOB_ID}")
    print(f"📁 Result directory: {result_dir}")
    
    if os.path.exists(result_dir):
        print("✅ Main result directory exists")
        
        # List contents
        contents = os.listdir(result_dir)
        print(f"📋 Contents: {contents}")
        
        # Check for timestamped subdirectories created by SadTalker
        timestamped_dirs = [d for d in contents if os.path.isdir(os.path.join(result_dir, d)) and '_' in d]
        if timestamped_dirs:
            print(f"✅ Found SadTalker timestamped subdirectories: {timestamped_dirs}")
            
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
                    
                # Look for .mp4 files (final output)
                mp4_files = [f for f in sub_contents if f.endswith('.mp4')]
                if mp4_files:
                    print(f"✅ Found .mp4 files: {mp4_files}")
                else:
                    print("⚠️  No .mp4 files found yet")
        else:
            print("⚠️  No SadTalker timestamped subdirectories found yet")
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
    print("🔧 Testing Directory Fix")
    print("=" * 50)
    
    check_directory_structure()
    check_job_status()
    
    print("\n⏳ Waiting 15 seconds and checking again...")
    time.sleep(15)
    
    print("\n" + "=" * 50)
    check_directory_structure()
    check_job_status()

if __name__ == "__main__":
    main()
