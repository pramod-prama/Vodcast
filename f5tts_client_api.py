#!/usr/bin/env python3
"""
Google Text-to-Speech Client API
Multi-language TTS support for English, Urdu, and Hindi
Ready-to-use API client for Google TTS integration
"""

import os
import io
import json
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from google.cloud import texttospeech
from google.oauth2 import service_account
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VoiceConfig:
    """Voice configuration for TTS"""
    language_code: str
    voice_name: str
    ssml_gender: str = "NEUTRAL"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0

@dataclass
class AudioConfig:
    """Audio output configuration"""
    audio_encoding: str = "MP3"  # MP3, LINEAR16, OGG_OPUS
    sample_rate_hertz: int = 22050
    effects_profile_id: Optional[str] = None

class GoogleTTSClient:
    """Google Text-to-Speech API Client with multi-language support"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google TTS client
        
        Args:
            credentials_path: Path to Google Cloud service account JSON file
        """
        self.credentials_path = credentials_path
        self.client = None
        self._initialize_client()
        
        # Available voices for each language
        self.available_voices = {
            "en": {
                "en-US-Standard-A": "American English - Female",
                "en-US-Standard-B": "American English - Male", 
                "en-US-Standard-C": "American English - Female",
                "en-US-Standard-D": "American English - Male",
                "en-US-Standard-E": "American English - Female",
                "en-US-Standard-F": "American English - Female",
                "en-US-Standard-G": "American English - Female",
                "en-US-Standard-H": "American English - Female",
                "en-US-Standard-I": "American English - Male",
                "en-US-Standard-J": "American English - Male",
                "en-GB-Standard-A": "British English - Female",
                "en-GB-Standard-B": "British English - Male",
                "en-GB-Standard-C": "British English - Female",
                "en-GB-Standard-D": "British English - Male",
                "en-AU-Standard-A": "Australian English - Female",
                "en-AU-Standard-B": "Australian English - Male",
                "en-AU-Standard-C": "Australian English - Female",
                "en-AU-Standard-D": "Australian English - Male"
            },
            "ur": {
                "ur-PK-Standard-A": "Urdu (Pakistan) - Female",
                "ur-PK-Standard-B": "Urdu (Pakistan) - Male",
                "ur-PK-Standard-C": "Urdu (Pakistan) - Female",
                "ur-PK-Standard-D": "Urdu (Pakistan) - Male"
            },
            "hi": {
                "hi-IN-Standard-A": "Hindi (India) - Female",
                "hi-IN-Standard-B": "Hindi (India) - Male",
                "hi-IN-Standard-C": "Hindi (India) - Female",
                "hi-IN-Standard-D": "Hindi (India) - Male"
            }
        }
        
        # Language codes mapping
        self.language_codes = {
            "english": "en",
            "urdu": "ur", 
            "hindi": "hi",
            "en": "en",
            "ur": "ur",
            "hi": "hi"
        }

    def _initialize_client(self):
        """Initialize Google TTS client with credentials"""
        try:
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                self.client = texttospeech.TextToSpeechClient(credentials=credentials)
                logger.info("Google TTS client initialized with service account credentials")
            else:
                # Try to use default credentials (environment variable or gcloud auth)
                self.client = texttospeech.TextToSpeechClient()
                logger.info("Google TTS client initialized with default credentials")
        except Exception as e:
            logger.error(f"Failed to initialize Google TTS client: {e}")
            raise ValueError(f"Google TTS client initialization failed: {e}")

    def get_available_voices(self, language: str = None) -> Dict[str, Any]:
        """
        Get available voices for a language or all languages
        
        Args:
            language: Language code (en, ur, hi) or None for all
            
        Returns:
            Dictionary of available voices
        """
        if language:
            lang_code = self.language_codes.get(language.lower(), language.lower())
            if lang_code in self.available_voices:
                return {lang_code: self.available_voices[lang_code]}
            else:
                return {}
        return self.available_voices

    def create_voice_config(
        self,
        language: str,
        voice_name: Optional[str] = None,
        gender: str = "NEUTRAL",
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
        volume_gain_db: float = 0.0
    ) -> VoiceConfig:
        """
        Create voice configuration
        
        Args:
            language: Language (english, urdu, hindi, en, ur, hi)
            voice_name: Specific voice name (optional)
            gender: Voice gender (NEUTRAL, MALE, FEMALE)
            speaking_rate: Speaking rate (0.25 to 4.0)
            pitch: Voice pitch (-20.0 to 20.0)
            volume_gain_db: Volume gain (-96.0 to 16.0)
            
        Returns:
            VoiceConfig object
        """
        lang_code = self.language_codes.get(language.lower(), language.lower())
        
        if lang_code not in self.available_voices:
            raise ValueError(f"Unsupported language: {language}")
        
        # Get default voice if not specified
        if not voice_name:
            voice_name = list(self.available_voices[lang_code].keys())[0]
        
        # Validate voice name
        if voice_name not in self.available_voices[lang_code]:
            logger.warning(f"Voice '{voice_name}' not found for {language}, using default")
            voice_name = list(self.available_voices[lang_code].keys())[0]
        
        # Extract language code from voice name
        language_code = voice_name.split('-')[0] + '-' + voice_name.split('-')[1]
        
        return VoiceConfig(
            language_code=language_code,
            voice_name=voice_name,
            ssml_gender=gender,
            speaking_rate=speaking_rate,
            pitch=pitch,
            volume_gain_db=volume_gain_db
        )

    def create_audio_config(
        self,
        audio_encoding: str = "MP3",
        sample_rate_hertz: int = 22050,
        effects_profile_id: Optional[str] = None
    ) -> AudioConfig:
        """
        Create audio configuration
        
        Args:
            audio_encoding: Audio format (MP3, LINEAR16, OGG_OPUS)
            sample_rate_hertz: Sample rate (8000, 16000, 22050, 24000, 32000, 44100, 48000)
            effects_profile_id: Audio effects profile ID
            
        Returns:
            AudioConfig object
        """
        return AudioConfig(
            audio_encoding=audio_encoding,
            sample_rate_hertz=sample_rate_hertz,
            effects_profile_id=effects_profile_id
        )

    def synthesize_speech(
        self,
        text: str,
        voice_config: VoiceConfig,
        audio_config: AudioConfig,
        output_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Synthesize speech from text
        
        Args:
            text: Text to convert to speech
            voice_config: Voice configuration
            audio_config: Audio configuration
            output_path: Output file path (auto-generated if None)
            
        Returns:
            Path to generated audio file or None if failed
        """
        try:
            if not text.strip():
                raise ValueError("Text cannot be empty")
            
            # Create synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Create voice selection
            voice = texttospeech.VoiceSelectionParams(
                language_code=voice_config.language_code,
                name=voice_config.voice_name,
                ssml_gender=getattr(texttospeech.SsmlVoiceGender, voice_config.ssml_gender)
            )
            
            # Create audio config
            audio_config_obj = texttospeech.AudioConfig(
                audio_encoding=getattr(texttospeech.AudioEncoding, audio_config.audio_encoding),
                sample_rate_hertz=audio_config.sample_rate_hertz,
                speaking_rate=voice_config.speaking_rate,
                pitch=voice_config.pitch,
                volume_gain_db=voice_config.volume_gain_db
            )
            
            if audio_config.effects_profile_id:
                audio_config_obj.effects_profile_id = [audio_config.effects_profile_id]
            
            # Perform synthesis
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config_obj
            )
            
            # Generate output path if not provided
            if not output_path:
                file_extension = audio_config.audio_encoding.lower()
                if file_extension == "linear16":
                    file_extension = "wav"
                output_path = f"tts_output_{uuid.uuid4().hex[:8]}.{file_extension}"
            
            # Save audio file
            with open(output_path, 'wb') as out:
                out.write(response.audio_content)
            
            logger.info(f"Audio generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Speech synthesis failed: {e}")
            return None

    def text_to_speech(
        self,
        text: str,
        language: str = "english",
        voice_name: Optional[str] = None,
        gender: str = "NEUTRAL",
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
        volume_gain_db: float = 0.0,
        audio_encoding: str = "MP3",
        sample_rate_hertz: int = 22050,
        output_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Complete TTS workflow with simplified parameters
        
        Args:
            text: Text to convert to speech
            language: Language (english, urdu, hindi, en, ur, hi)
            voice_name: Specific voice name (optional)
            gender: Voice gender (NEUTRAL, MALE, FEMALE)
            speaking_rate: Speaking rate (0.25 to 4.0)
            pitch: Voice pitch (-20.0 to 20.0)
            volume_gain_db: Volume gain (-96.0 to 16.0)
            audio_encoding: Audio format (MP3, LINEAR16, OGG_OPUS)
            sample_rate_hertz: Sample rate
            output_path: Output file path (auto-generated if None)
            
        Returns:
            Path to generated audio file or None if failed
        """
        try:
            # Create configurations
            voice_config = self.create_voice_config(
                language=language,
                voice_name=voice_name,
                gender=gender,
                speaking_rate=speaking_rate,
                pitch=pitch,
                volume_gain_db=volume_gain_db
            )
            
            audio_config = self.create_audio_config(
                audio_encoding=audio_encoding,
                sample_rate_hertz=sample_rate_hertz
            )
            
            # Synthesize speech
            return self.synthesize_speech(text, voice_config, audio_config, output_path)
            
        except Exception as e:
            logger.error(f"TTS workflow failed: {e}")
            return None

    def batch_text_to_speech(
        self,
        texts: List[str],
        language: str = "english",
        voice_name: Optional[str] = None,
        output_dir: str = "output",
        **kwargs
    ) -> List[str]:
        """
        Generate speech for multiple texts
        
        Args:
            texts: List of texts to convert
            language: Language for all texts
            voice_name: Voice name for all texts
            output_dir: Output directory
            **kwargs: Additional parameters for text_to_speech
            
        Returns:
            List of generated file paths
        """
        generated_files = []
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        for i, text in enumerate(texts):
            logger.info(f"Generating speech for text {i+1}/{len(texts)}...")
            
            # Generate output filename
            output_filename = f"speech_{i+1}_{uuid.uuid4().hex[:8]}.mp3"
            output_path = os.path.join(output_dir, output_filename)
            
            # Generate speech
            result = self.text_to_speech(
                text=text,
                language=language,
                voice_name=voice_name,
                output_path=output_path,
                **kwargs
            )
            
            if result:
                generated_files.append(result)
                logger.info(f"✅ Generated: {result}")
            else:
                logger.error(f"❌ Failed to generate speech for text {i+1}")
        
        return generated_files

    def get_voice_info(self, voice_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific voice
        
        Args:
            voice_name: Voice name to get info for
            
        Returns:
            Voice information dictionary or None
        """
        for lang_code, voices in self.available_voices.items():
            if voice_name in voices:
                return {
                    "voice_name": voice_name,
                    "description": voices[voice_name],
                    "language_code": lang_code,
                    "language": self._get_language_name(lang_code)
                }
        return None

    def _get_language_name(self, lang_code: str) -> str:
        """Get full language name from code"""
        language_names = {
            "en": "English",
            "ur": "Urdu", 
            "hi": "Hindi"
        }
        return language_names.get(lang_code, lang_code)


# Convenience functions for quick usage
def quick_tts(
    text: str,
    language: str = "english",
    output_file: str = "output.mp3",
    credentials_path: Optional[str] = None
) -> bool:
    """
    Quick text-to-speech generation
    
    Args:
        text: Text to convert to speech
        language: Language (english, urdu, hindi)
        output_file: Output file name
        credentials_path: Path to Google Cloud credentials
        
    Returns:
        True if successful, False otherwise
    """
    try:
        client = GoogleTTSClient(credentials_path)
        result = client.text_to_speech(text, language=language, output_path=output_file)
        return result is not None
    except Exception as e:
        logger.error(f"Quick TTS failed: {e}")
        return False

def batch_tts(
    texts: List[str],
    language: str = "english",
    output_dir: str = "output",
    credentials_path: Optional[str] = None
) -> List[str]:
    """
    Generate speech for multiple texts
    
    Args:
        texts: List of texts to convert
        language: Language for all texts
        output_dir: Output directory
        credentials_path: Path to Google Cloud credentials
        
    Returns:
        List of generated file paths
    """
    try:
        client = GoogleTTSClient(credentials_path)
        return client.batch_text_to_speech(texts, language=language, output_dir=output_dir)
    except Exception as e:
        logger.error(f"Batch TTS failed: {e}")
        return []


# Example usage and testing
def main():
    """Example usage of GoogleTTSClient class"""
    
    # Initialize TTS client
    try:
        # Try to use credentials file if it exists
        credentials_path = None
        possible_paths = [
            "gcs_credentials.json",
            "revoiz-ai-dd6bb5e7b3ee.json",
            "google_credentials.json"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                credentials_path = path
                break
        
        tts = GoogleTTSClient(credentials_path)
        print("✅ Google TTS client initialized successfully")
        
    except Exception as e:
        print(f"❌ Error initializing Google TTS client: {e}")
        print("Please ensure you have Google Cloud credentials set up")
        return
    
    # Example 1: English TTS
    print("\n🌍 Example 1: English TTS")
    english_text = "Hello, this is a test of Google Text-to-Speech API. How does it sound?"
    
    output_file = tts.text_to_speech(
        text=english_text,
        language="english",
        voice_name="en-US-Standard-A",
        output_path="example_english.mp3"
    )
    
    if output_file:
        print(f"✅ English audio saved to: {output_file}")
    else:
        print("❌ Failed to generate English audio")
    
    # Example 2: Urdu TTS
    print("\n🌍 Example 2: Urdu TTS")
    urdu_text = "السلام علیکم، یہ Google Text-to-Speech API کا ٹیسٹ ہے۔ آپ کو کیسا لگ رہا ہے؟"
    
    output_file = tts.text_to_speech(
        text=urdu_text,
        language="urdu",
        voice_name="ur-PK-Standard-A",
        output_path="example_urdu.mp3"
    )
    
    if output_file:
        print(f"✅ Urdu audio saved to: {output_file}")
    else:
        print("❌ Failed to generate Urdu audio")
    
    # Example 3: Hindi TTS
    print("\n🌍 Example 3: Hindi TTS")
    hindi_text = "नमस्ते, यह Google Text-to-Speech API का परीक्षण है। आपको कैसा लग रहा है?"
    
    output_file = tts.text_to_speech(
        text=hindi_text,
        language="hindi",
        voice_name="hi-IN-Standard-A",
        output_path="example_hindi.mp3"
    )
    
    if output_file:
        print(f"✅ Hindi audio saved to: {output_file}")
    else:
        print("❌ Failed to generate Hindi audio")
    
    # Example 4: Custom voice settings
    print("\n🎛️ Example 4: Custom voice settings")
    custom_text = "This is with custom voice settings - slower speed and higher pitch."
    
    output_file = tts.text_to_speech(
        text=custom_text,
        language="english",
        voice_name="en-US-Standard-B",
        speaking_rate=0.8,
        pitch=5.0,
        volume_gain_db=2.0,
        output_path="example_custom.mp3"
    )
    
    if output_file:
        print(f"✅ Custom audio saved to: {output_file}")
    else:
        print("❌ Failed to generate custom audio")
    
    # Example 5: Batch processing
    print("\n📦 Example 5: Batch processing")
    batch_texts = [
        "First text in English",
        "دوسرا متن اردو میں",
        "तीसरा पाठ हिंदी में"
    ]
    
    generated_files = tts.batch_text_to_speech(
        texts=batch_texts,
        language="english",  # All will be in English for this example
        output_dir="batch_output"
    )
    
    print(f"✅ Generated {len(generated_files)} files in batch processing")
    
    # Show available voices
    print(f"\n🎤 Available voices:")
    for lang, voices in tts.get_available_voices().items():
        print(f"\n{lang.upper()}:")
        for voice_name, description in voices.items():
            print(f"  - {voice_name}: {description}")


if __name__ == "__main__":
    main()