#!/usr/bin/env python3
"""
Test the batch data that's causing the issue
"""
import os
import sys

# Add the src directory to the path
sys.path.append('src')

from generate_batch import get_data

def test_batch_data():
    """Test the batch data generation"""
    
    print(f"🔍 Testing batch data generation")
    
    # Use the same files that are failing
    first_coeff_path = "results/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45/2025_09_19_07.29.53/first_frame_dir/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_image_WhatsApp_Image_2025-05-07_at_2.39.41_PM.mat"
    audio_path = "uploads/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45_audio_audio-output-1_p9e8CVDx.mp3"
    device = "cpu"
    
    print(f"📁 First coeff path: {first_coeff_path}")
    print(f"📁 Audio path: {audio_path}")
    print(f"📁 Device: {device}")
    
    try:
        # Generate batch data
        batch = get_data(first_coeff_path, audio_path, device, None, still=False)
        
        print(f"\n📊 Batch data:")
        print(f"   Keys: {list(batch.keys())}")
        
        if 'pic_name' in batch:
            print(f"   pic_name: {batch['pic_name']}")
            print(f"   pic_name type: {type(batch['pic_name'])}")
            print(f"   pic_name repr: {repr(batch['pic_name'])}")
        
        if 'audio_name' in batch:
            print(f"   audio_name: {batch['audio_name']}")
            print(f"   audio_name type: {type(batch['audio_name'])}")
            print(f"   audio_name repr: {repr(batch['audio_name'])}")
        
        # Test filename construction
        if 'pic_name' in batch and 'audio_name' in batch:
            filename = '%s##%s.mat'%(batch['pic_name'], batch['audio_name'])
            print(f"\n📄 Constructed filename: {filename}")
            print(f"   Length: {len(filename)}")
            print(f"   Contains backslashes: {'\\\\' in filename}")
            print(f"   Contains forward slashes: {'/' in filename}")
            
            # Test path construction
            coeff_save_dir = "results/4d0f859f-1ac0-4de1-b0f5-b91374c5bd45/2025_09_19_07.29.53"
            file_path = os.path.join(coeff_save_dir, filename)
            print(f"\n📄 Full path: {file_path}")
            print(f"   Length: {len(file_path)}")
            print(f"   Contains double backslashes: {'\\\\' in file_path}")
            
            # Test if the issue is with the filename
            test_filename = "simple_test.mat"
            test_path = os.path.join(coeff_save_dir, test_filename)
            print(f"\n📄 Test path: {test_path}")
            print(f"   Contains double backslashes: {'\\\\' in test_path}")
        
    except Exception as e:
        print(f"❌ Error generating batch data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Testing Batch Data")
    print("=" * 50)
    
    # Test batch data generation
    test_batch_data()
