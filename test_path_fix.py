#!/usr/bin/env python3
"""
Test the path fix
"""
import os
from scipy.io import savemat
import numpy as np

def test_path_fix():
    """Test the path normalization fix"""
    
    # The exact failing path
    failing_dir = "results/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45/2025_09_19_07.29.53"
    failing_filename = "4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_image_WhatsApp_Image_2025-05-07_at_2.39.41_PM##4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_audio_audio-output-1_p9e8CVDx.mat"
    
    print(f"🔍 Testing path fix")
    print(f"📁 Directory: {failing_dir}")
    print(f"📄 Filename: {failing_filename}")
    
    try:
        # Check if directory exists
        if not os.path.exists(failing_dir):
            print(f"❌ Directory does not exist: {failing_dir}")
            return False
        
        print(f"✅ Directory exists")
        
        # Test the old way (with double backslashes)
        old_path = os.path.join(failing_dir, failing_filename)
        print(f"📄 Old path: {old_path}")
        
        # Test the new way (with path normalization)
        filename = failing_filename
        file_path = os.path.join(failing_dir, filename)
        file_path = os.path.normpath(file_path)
        print(f"📄 New path: {file_path}")
        
        # Test file creation with normalized path
        test_data = np.random.rand(10, 70)  # Similar to coeffs_pred_numpy
        
        print(f"🔍 Attempting to create file with normalized path...")
        savemat(file_path, {'coeff_3dmm': test_data})
        print(f"✅ File created successfully!")
        
        # Check if file exists
        if os.path.exists(file_path):
            print(f"✅ File exists: {file_path}")
            
            # Get file size
            file_size = os.path.getsize(file_path)
            print(f"📊 File size: {file_size} bytes")
            
            # Clean up
            os.remove(file_path)
            print(f"✅ Cleanup successful")
            
            return True
        else:
            print(f"❌ File does not exist after creation")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Path Fix")
    print("=" * 50)
    
    # Test the path fix
    success = test_path_fix()
    
    if success:
        print("\n✅ Path fix test passed")
    else:
        print("\n❌ Path fix test failed")
