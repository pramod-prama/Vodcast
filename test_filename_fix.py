#!/usr/bin/env python3
"""
Test the filename length fix
"""
import os
from scipy.io import savemat
import numpy as np

def test_filename_fix():
    """Test the filename length fix"""
    
    # The exact failing path
    failing_dir = "results/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45/2025_09_19_07.29.53"
    
    # Original long names
    pic_name = "4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_image_WhatsApp_Image_2025-05-07_at_2.39.41_PM"
    audio_name = "4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_audio_audio-output-1_p9e8CVDx"
    
    print(f"🔍 Testing filename length fix")
    print(f"📁 Directory: {failing_dir}")
    print(f"📄 Original pic_name: {pic_name} ({len(pic_name)} chars)")
    print(f"📄 Original audio_name: {audio_name} ({len(audio_name)} chars)")
    
    # Test the fix
    pic_name_short = pic_name[:50] if len(pic_name) > 50 else pic_name
    audio_name_short = audio_name[:50] if len(audio_name) > 50 else audio_name
    filename = '%s##%s.mat'%(pic_name_short, audio_name_short)
    
    print(f"\n📄 Shortened pic_name: {pic_name_short} ({len(pic_name_short)} chars)")
    print(f"📄 Shortened audio_name: {audio_name_short} ({len(audio_name_short)} chars)")
    print(f"📄 Shortened filename: {filename} ({len(filename)} chars)")
    
    try:
        # Check if directory exists
        if not os.path.exists(failing_dir):
            print(f"❌ Directory does not exist: {failing_dir}")
            return False
        
        print(f"✅ Directory exists")
        
        # Test file creation with shortened filename
        file_path = os.path.join(failing_dir, filename)
        file_path = os.path.normpath(file_path)
        
        print(f"📄 Full path: {file_path}")
        print(f"📏 Path length: {len(file_path)} characters")
        
        # Test file creation
        test_data = np.random.rand(10, 70)  # Similar to coeffs_pred_numpy
        
        print(f"🔍 Attempting to create file with shortened filename...")
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
    print("🧪 Testing Filename Length Fix")
    print("=" * 60)
    
    # Test the filename fix
    success = test_filename_fix()
    
    if success:
        print("\n✅ Filename length fix test passed")
    else:
        print("\n❌ Filename length fix test failed")
