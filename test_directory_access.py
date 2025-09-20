#!/usr/bin/env python3
"""
Test directory access and file creation
"""
import os
import tempfile
from scipy.io import savemat
import numpy as np

def test_directory_access():
    """Test if we can create and access directories like SadTalker does"""
    
    # Test the exact path structure that's failing
    test_dir = "results/test_job/2025_09_19_07.29.53"
    
    print(f"🔍 Testing directory access: {test_dir}")
    
    try:
        # Create the directory
        os.makedirs(test_dir, exist_ok=True)
        print(f"✅ Directory created successfully")
        
        # Check if directory exists
        if os.path.exists(test_dir):
            print(f"✅ Directory exists: {test_dir}")
        else:
            print(f"❌ Directory does not exist: {test_dir}")
            return False
        
        # Test file creation like SadTalker does
        test_file = os.path.join(test_dir, "test_image##test_audio.mat")
        print(f"🔍 Testing file creation: {test_file}")
        
        # Create test data
        test_data = np.random.rand(10, 70)  # Similar to coeffs_pred_numpy
        
        # Try to save the file
        savemat(test_file, {'coeff_3dmm': test_data})
        print(f"✅ File created successfully: {test_file}")
        
        # Check if file exists
        if os.path.exists(test_file):
            print(f"✅ File exists: {test_file}")
        else:
            print(f"❌ File does not exist: {test_file}")
            return False
        
        # Clean up
        os.remove(test_file)
        os.rmdir(test_dir)
        print(f"✅ Cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_actual_paths():
    """Test with actual paths from the failing job"""
    
    # Use the actual failing path
    failing_dir = "results/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45/2025_09_19_07.29.53"
    
    print(f"\n🔍 Testing with actual failing path: {failing_dir}")
    
    try:
        # Check if directory exists
        if os.path.exists(failing_dir):
            print(f"✅ Directory exists: {failing_dir}")
            
            # List contents
            contents = os.listdir(failing_dir)
            print(f"📋 Directory contents: {contents}")
            
            # Test file creation
            test_file = os.path.join(failing_dir, "test_file.mat")
            test_data = np.random.rand(5, 10)
            
            savemat(test_file, {'test_data': test_data})
            print(f"✅ File creation successful: {test_file}")
            
            # Clean up
            os.remove(test_file)
            
        else:
            print(f"❌ Directory does not exist: {failing_dir}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Directory Access")
    print("=" * 50)
    
    # Test basic directory access
    success = test_directory_access()
    
    if success:
        print("\n✅ Basic directory access test passed")
    else:
        print("\n❌ Basic directory access test failed")
    
    # Test with actual failing paths
    test_with_actual_paths()
