import os
import streamlit as st
import subprocess
from datetime import datetime
import re
import soundfile as sf


# Set up paths
UPLOAD_DIR = "data/uploads"
GENERATED_DIR = "data/generated"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)

def extract_audio_from_video(video_path, audio_output_path):
    try:
        command = [
            "ffmpeg", "-y", "-i", video_path,
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_output_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(audio_output_path):
            return audio_output_path
        else:
            st.error("Audio extraction failed: output file not found.")
            return None
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to extract audio: {e}")
        return None

def generate_tts_audio(text, output_path, reference_audio_path):
    try:
        from chatterbox.pipeline import VoiceCloningPipeline

        # Denoise reference audio
        clean_ref_audio_path = os.path.join(UPLOAD_DIR, "ref_audio_denoised.wav")
        if not denoise_audio(reference_audio_path, clean_ref_audio_path):
            return None

        # Use Chatterbox multilingual voice cloning
        vc = VoiceCloningPipeline.from_pretrained("chatterbox/voice-cloning-multilingual")
        audio = vc(text, reference_audio=clean_ref_audio_path)

        # Save output audio
        sf.write(output_path, audio.audio, audio.sample_rate)
        return output_path if os.path.exists(output_path) else None
    except Exception as e:
        st.error(f"TTS generation failed (Chatterbox): {e}")
        return None

def run_wav2lip(face_video_path, audio_path, output_path):
    try:
        command = [
            "python", os.path.join(WAV2LIP_DIR, "inference.py"),
            "--checkpoint_path", WAV2LIP_CHECKPOINT,
            "--face", face_video_path,
            "--audio", audio_path,
            "--outfile", output_path
        ]
        subprocess.run(command, check=True)
        return output_path if os.path.exists(output_path) else None
    except subprocess.CalledProcessError as e:
        st.error(f"Wav2Lip failed: {e}")
        return None

def show_main_app():
    st.title("🎥 Prama Vodcast")

    uploaded_file = st.file_uploader("📤 Upload your face video (mp4/mov)", type=["mp4", "mov"])
    script_text = st.text_area("📝 Enter your script", height=150)
    language = st.selectbox("🌐 Select language for TTS (Note: Mixed English & Hindi supported)", options=["English", "Hindi"])
    generate_trigger = st.button("🎬 Generate Video")

    if generate_trigger:
        if not uploaded_file:
            st.warning("⚠️ Please upload a video file.")
            return
        if not script_text.strip():
            st.warning("⚠️ Please enter a script.")
            return

        with st.spinner("🛠️ Processing video and generating audio..."):
            filename = f"VIDEO-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.mp4"
            face_video_path = os.path.join(UPLOAD_DIR, filename)
            with open(face_video_path, "wb") as f:
                f.write(uploaded_file.read())
            st.success("✅ Video uploaded.")

            reference_audio_path = os.path.join(UPLOAD_DIR, "ref_audio.wav")
            if not extract_audio_from_video(face_video_path, reference_audio_path):
                return

            audio_path = os.path.join(GENERATED_DIR, "output_audio.wav")
            if not generate_tts_audio(script_text, audio_path, reference_audio_path):
                st.error("⚠️ TTS audio generation failed.")
                return

            st.success("✅ Audio generated from script with voice cloning.")

            final_video_path = os.path.join(GENERATED_DIR, "final_lipsynced_video.mp4")
            if run_wav2lip(face_video_path, audio_path, final_video_path):
                st.success("🎉 Lip-synced video generated successfully!")
                st.video(final_video_path)
            else:
                st.error("❌ Wav2Lip video generation failed.")

if __name__ == "__main__":
    show_main_app()
