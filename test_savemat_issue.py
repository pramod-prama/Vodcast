#!/usr/bin/env python3
"""
Test the savemat function with the exact failing filename
"""
import os
from scipy.io import savemat
import numpy as np

def test_savemat_issue():
    """Test the savemat function with the exact failing filename"""
    
    # The exact failing path
    failing_dir = "results/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45/2025_09_19_07.29.53"
    failing_filename = "4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_image_WhatsApp_Image_2025-05-07_at_2.39.41_PM##4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_audio_audio-output-1_p9e8CVDx.mat"
    
    print(f"🔍 Testing savemat function")
    print(f"📁 Directory: {failing_dir}")
    print(f"📄 Filename: {failing_filename}")
    
    try:
        # Check if directory exists
        if not os.path.exists(failing_dir):
            print(f"❌ Directory does not exist: {failing_dir}")
            return False
        
        print(f"✅ Directory exists")
        
        # Test different approaches
        approaches = [
            ("Approach 1: Direct os.path.join", lambda: os.path.join(failing_dir, failing_filename)),
            ("Approach 2: os.path.normpath", lambda: os.path.normpath(os.path.join(failing_dir, failing_filename))),
            ("Approach 3: os.path.abspath", lambda: os.path.abspath(os.path.join(failing_dir, failing_filename))),
            ("Approach 4: Replace separators", lambda: os.path.join(failing_dir, failing_filename).replace('/', '\\')),
            ("Approach 5: Replace separators reverse", lambda: os.path.join(failing_dir, failing_filename).replace('\\', '/')),
        ]
        
        for approach_name, approach_func in approaches:
            try:
                print(f"\n🔍 {approach_name}")
                file_path = approach_func()
                print(f"   Path: {file_path}")
                print(f"   Length: {len(file_path)}")
                
                # Test file creation
                test_data = np.random.rand(10, 70)
                savemat(file_path, {'coeff_3dmm': test_data})
                print(f"   ✅ Success!")
                
                # Clean up
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"   ✅ Cleanup successful")
                
                return True
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
                print(f"   ❌ Error type: {type(e).__name__}")
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_savemat_with_shorter_filename():
    """Test savemat with a shorter filename"""
    
    print(f"\n🔍 Testing savemat with shorter filename")
    
    failing_dir = "results/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45/2025_09_19_07.29.53"
    
    # Test with shorter filename
    shorter_filename = "test_image##test_audio.mat"
    
    try:
        file_path = os.path.join(failing_dir, shorter_filename)
        print(f"📄 Path: {file_path}")
        
        test_data = np.random.rand(10, 70)
        savemat(file_path, {'coeff_3dmm': test_data})
        print(f"✅ Success with shorter filename!")
        
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"✅ Cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed with shorter filename: {e}")
        return False

def test_filename_length_limit():
    """Test if there's a filename length limit"""
    
    print(f"\n🔍 Testing filename length limit")
    
    failing_dir = "results/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45/2025_09_19_07.29.53"
    
    # Test with progressively longer filenames
    base_filename = "test_image##test_audio.mat"
    
    for i in range(5):
        # Add more characters to the filename
        extended_filename = base_filename.replace("test", "test" + "x" * (i * 20))
        file_path = os.path.join(failing_dir, extended_filename)
        
        print(f"\n📄 Test {i+1}: {len(extended_filename)} characters")
        print(f"   Filename: {extended_filename}")
        
        try:
            test_data = np.random.rand(5, 10)
            savemat(file_path, {'test_data': test_data})
            print(f"   ✅ Success!")
            
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            break

if __name__ == "__main__":
    print("🧪 Testing savemat Issue")
    print("=" * 60)
    
    # Test the exact failing case
    success = test_savemat_issue()
    
    if not success:
        # Test with shorter filename
        test_savemat_with_shorter_filename()
        
        # Test filename length limit
        test_filename_length_limit()
