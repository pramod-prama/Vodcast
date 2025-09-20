#!/usr/bin/env python3
"""
Test the specific filename that's failing
"""
import os
from scipy.io import savemat
import numpy as np

def test_specific_filename():
    """Test the exact filename that's failing"""
    
    # The exact failing path
    failing_dir = "results/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45/2025_09_19_07.29.53"
    failing_filename = "4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_image_WhatsApp_Image_2025-05-07_at_2.39.41_PM##4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_audio_audio-output-1_p9e8CVDx.mat"
    
    print(f"🔍 Testing specific failing filename")
    print(f"📁 Directory: {failing_dir}")
    print(f"📄 Filename: {failing_filename}")
    
    try:
        # Check if directory exists
        if not os.path.exists(failing_dir):
            print(f"❌ Directory does not exist: {failing_dir}")
            return False
        
        print(f"✅ Directory exists")
        
        # Create the full path
        full_path = os.path.join(failing_dir, failing_filename)
        print(f"📄 Full path: {full_path}")
        
        # Check path length
        print(f"📏 Path length: {len(full_path)} characters")
        
        # Test file creation
        test_data = np.random.rand(10, 70)  # Similar to coeffs_pred_numpy
        
        print(f"🔍 Attempting to create file...")
        savemat(full_path, {'coeff_3dmm': test_data})
        print(f"✅ File created successfully!")
        
        # Check if file exists
        if os.path.exists(full_path):
            print(f"✅ File exists: {full_path}")
            
            # Get file size
            file_size = os.path.getsize(full_path)
            print(f"📊 File size: {file_size} bytes")
            
            # Clean up
            os.remove(full_path)
            print(f"✅ Cleanup successful")
            
            return True
        else:
            print(f"❌ File does not exist after creation")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

def test_filename_components():
    """Test different parts of the filename"""
    
    failing_dir = "results/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45/2025_09_19_07.29.53"
    
    # Test different filename components
    test_cases = [
        "simple_test.mat",
        "test_image##test_audio.mat",
        "4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_image_WhatsApp_Image_2025-05-07_at_2.39.41_PM.mat",
        "4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_audio_audio-output-1_p9e8CVDx.mat",
        "4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_image_WhatsApp_Image_2025-05-07_at_2.39.41_PM##4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_audio_audio-output-1_p9e8CVDx.mat"
    ]
    
    print(f"\n🔍 Testing filename components")
    
    for i, filename in enumerate(test_cases):
        print(f"\n📄 Test case {i+1}: {filename}")
        
        try:
            full_path = os.path.join(failing_dir, filename)
            test_data = np.random.rand(5, 10)
            
            savemat(full_path, {'test_data': test_data})
            print(f"✅ Success")
            
            # Clean up
            os.remove(full_path)
            
        except Exception as e:
            print(f"❌ Failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Specific Filename")
    print("=" * 60)
    
    # Test the exact failing filename
    success = test_specific_filename()
    
    if success:
        print("\n✅ Specific filename test passed")
    else:
        print("\n❌ Specific filename test failed")
    
    # Test filename components
    test_filename_components()
