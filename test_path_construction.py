#!/usr/bin/env python3
"""
Test path construction to find the issue
"""
import os

def test_path_construction():
    """Test different ways of constructing the path"""
    
    # Base directory
    base_dir = "results"
    job_id = "4d0f859f-1ac0-4de1-b0f5-b91374c5bd45"
    timestamp = "2025_09_19_07.29.53"
    filename = "4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_image_WhatsApp_Image_2025-05-07_at_2.39.41_PM##4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_audio_audio-output-1_p9e8CVDx.mat"
    
    print(f"🔍 Testing path construction")
    print(f"📁 Base dir: {base_dir}")
    print(f"🆔 Job ID: {job_id}")
    print(f"⏰ Timestamp: {timestamp}")
    print(f"📄 Filename: {filename}")
    
    # Test different path construction methods
    methods = [
        ("Method 1: os.path.join with forward slashes", lambda: os.path.join(base_dir, job_id, timestamp, filename)),
        ("Method 2: os.path.join with backslashes", lambda: os.path.join(base_dir.replace('/', '\\'), job_id, timestamp, filename)),
        ("Method 3: Manual construction", lambda: f"{base_dir}/{job_id}/{timestamp}/{filename}"),
        ("Method 4: Manual with backslashes", lambda: f"{base_dir}\\{job_id}\\{timestamp}\\{filename}"),
        ("Method 5: os.path.normpath", lambda: os.path.normpath(os.path.join(base_dir, job_id, timestamp, filename))),
        ("Method 6: os.path.abspath", lambda: os.path.abspath(os.path.join(base_dir, job_id, timestamp, filename))),
    ]
    
    for method_name, method_func in methods:
        try:
            path = method_func()
            print(f"\n📄 {method_name}:")
            print(f"   Path: {path}")
            print(f"   Length: {len(path)}")
            print(f"   Exists: {os.path.exists(path)}")
            
            # Check if parent directory exists
            parent_dir = os.path.dirname(path)
            print(f"   Parent exists: {os.path.exists(parent_dir)}")
            
            if os.path.exists(parent_dir):
                print(f"   Parent contents: {os.listdir(parent_dir)}")
            
        except Exception as e:
            print(f"\n❌ {method_name}: {e}")

def test_actual_directory():
    """Test the actual directory that exists"""
    
    print(f"\n🔍 Testing actual directory")
    
    # The directory that actually exists
    actual_dir = "results/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45/2025_09_19_07.29.53"
    
    print(f"📁 Actual directory: {actual_dir}")
    print(f"📁 Exists: {os.path.exists(actual_dir)}")
    
    if os.path.exists(actual_dir):
        print(f"📁 Absolute path: {os.path.abspath(actual_dir)}")
        print(f"📁 Contents: {os.listdir(actual_dir)}")
        
        # Test creating a file in this directory
        test_filename = "test_file.mat"
        test_path = os.path.join(actual_dir, test_filename)
        print(f"📄 Test file path: {test_path}")
        
        try:
            with open(test_path, 'w') as f:
                f.write("test")
            print(f"✅ File creation successful")
            
            # Clean up
            os.remove(test_path)
            print(f"✅ Cleanup successful")
            
        except Exception as e:
            print(f"❌ File creation failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Path Construction")
    print("=" * 60)
    
    # Test path construction
    test_path_construction()
    
    # Test actual directory
    test_actual_directory()
