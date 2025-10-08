# 🎤 Google TTS Client - Complete Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Basic Usage](#basic-usage)
4. [Advanced Configuration](#advanced-configuration)
5. [Language Support](#language-support)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Error Handling](#error-handling)
9. [Performance Tips](#performance-tips)
10. [Troubleshooting](#troubleshooting)

---

## 🚀 Overview

The Google TTS Client (`f5tts_client_api.py`) is a comprehensive Python library for Google Cloud Text-to-Speech integration. It provides high-quality speech synthesis in multiple languages with extensive customization options.

### Key Features
- ✅ **Multi-language Support**: English, Urdu, Hindi
- ✅ **Multiple Voice Options**: 26+ voices across all languages
- ✅ **Advanced Voice Control**: Speed, pitch, volume adjustment
- ✅ **Batch Processing**: Generate multiple audio files efficiently
- ✅ **Flexible Audio Formats**: MP3, WAV, OGG_OPUS
- ✅ **Production Ready**: Comprehensive error handling and logging
- ✅ **Easy Integration**: Simple API with detailed documentation

---

## 🔧 Installation & Setup

### Prerequisites
```bash
pip install google-cloud-texttospeech google-auth requests
```

### Google Cloud Setup
1. **Create Service Account**:
   - Go to Google Cloud Console
   - Create new service account
   - Download JSON credentials file

2. **Enable APIs**:
   - Enable Text-to-Speech API
   - Enable Cloud Storage API (for file storage)

3. **Place Credentials**:
   ```bash
   # Place your service account JSON file in project root
   cp your-service-account.json revoiz-ai-dd6bb5e7b3ee.json
   ```

### Environment Variables (Optional)
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

---

## 🎯 Basic Usage

### Simple Text-to-Speech
```python
from f5tts_client_api import GoogleTTSClient

# Initialize client
tts = GoogleTTSClient()

# Generate speech
output_file = tts.text_to_speech(
    text="Hello, this is a test",
    language="english"
)

print(f"Audio saved to: {output_file}")
```

### Multi-Language Examples
```python
# English
english_file = tts.text_to_speech(
    text="Hello, how are you?",
    language="english",
    output_path="english_output.mp3"
)

# Urdu
urdu_file = tts.text_to_speech(
    text="السلام علیکم، آپ کیسے ہیں؟",
    language="urdu",
    output_path="urdu_output.mp3"
)

# Hindi
hindi_file = tts.text_to_speech(
    text="नमस्ते, आप कैसे हैं?",
    language="hindi",
    output_path="hindi_output.mp3"
)
```

---

## ⚙️ Advanced Configuration

### Voice Configuration
```python
from f5tts_client_api import VoiceConfig, AudioConfig

# Custom voice settings
voice_config = VoiceConfig(
    language_code="en-US",
    voice_name="en-US-Standard-B",  # Male voice
    ssml_gender="MALE",
    speaking_rate=0.8,  # Slower speech
    pitch=5.0,  # Higher pitch
    volume_gain_db=2.0  # Louder volume
)

# Audio settings
audio_config = AudioConfig(
    audio_encoding="MP3",
    sample_rate_hertz=44100,  # High quality
    effects_profile_id=None
)

# Use custom configurations
output_file = tts.synthesize_speech(
    text="This is with custom voice settings",
    voice_config=voice_config,
    audio_config=audio_config
)
```

### Batch Processing
```python
# Generate multiple audio files
texts = [
    "First text in English",
    "دوسرا متن اردو میں",
    "तीसरा पाठ हिंदी में"
]

generated_files = tts.batch_text_to_speech(
    texts=texts,
    language="english",
    output_dir="batch_output"
)

print(f"Generated {len(generated_files)} files")
```

---

## 🌍 Language Support

### Available Languages

#### 🇺🇸 English
```python
# Language codes
"english", "en", "en-US"

# Available voices
voices = tts.get_available_voices("english")
# Returns: {
#   "en-US-Standard-A": "American English - Female",
#   "en-US-Standard-B": "American English - Male",
#   "en-GB-Standard-A": "British English - Female",
#   "en-AU-Standard-A": "Australian English - Female",
#   # ... and more
# }
```

#### 🇵🇰 Urdu
```python
# Language codes
"urdu", "ur", "ur-PK"

# Example usage
urdu_text = "یہ اردو میں ٹیسٹ ہے"
output = tts.text_to_speech(
    text=urdu_text,
    language="urdu",
    voice_name="ur-PK-Standard-A"
)
```

#### 🇮🇳 Hindi
```python
# Language codes
"hindi", "hi", "hi-IN"

# Example usage
hindi_text = "यह हिंदी में परीक्षण है"
output = tts.text_to_speech(
    text=hindi_text,
    language="hindi",
    voice_name="hi-IN-Standard-A"
)
```

---

## 📚 API Reference

### GoogleTTSClient Class

#### `__init__(credentials_path=None)`
Initialize the TTS client.

**Parameters:**
- `credentials_path` (str, optional): Path to Google Cloud service account JSON file

**Example:**
```python
tts = GoogleTTSClient("path/to/credentials.json")
```

#### `text_to_speech(text, language="english", voice_name=None, ...)`
Complete TTS workflow with simplified parameters.

**Parameters:**
- `text` (str): Text to convert to speech
- `language` (str): Language code ("english", "urdu", "hindi")
- `voice_name` (str, optional): Specific voice name
- `gender` (str): Voice gender ("NEUTRAL", "MALE", "FEMALE")
- `speaking_rate` (float): Speaking rate (0.25 to 4.0)
- `pitch` (float): Voice pitch (-20.0 to 20.0)
- `volume_gain_db` (float): Volume gain (-96.0 to 16.0)
- `audio_encoding` (str): Audio format ("MP3", "LINEAR16", "OGG_OPUS")
- `sample_rate_hertz` (int): Sample rate
- `output_path` (str, optional): Output file path

**Returns:**
- `str`: Path to generated audio file or `None` if failed

#### `batch_text_to_speech(texts, language="english", output_dir="output", **kwargs)`
Generate speech for multiple texts.

**Parameters:**
- `texts` (List[str]): List of texts to convert
- `language` (str): Language for all texts
- `output_dir` (str): Output directory
- `**kwargs`: Additional parameters for text_to_speech

**Returns:**
- `List[str]`: List of generated file paths

#### `get_available_voices(language=None)`
Get available voices for a language or all languages.

**Parameters:**
- `language` (str, optional): Language code or None for all

**Returns:**
- `Dict[str, Any]`: Dictionary of available voices

#### `get_voice_info(voice_name)`
Get information about a specific voice.

**Parameters:**
- `voice_name` (str): Voice name to get info for

**Returns:**
- `Dict[str, Any]`: Voice information or `None`

---

## 💡 Examples

### Example 1: Basic Multi-Language TTS
```python
from f5tts_client_api import GoogleTTSClient

def demo_multi_language():
    tts = GoogleTTSClient()
    
    # English
    english_file = tts.text_to_speech(
        text="Hello, welcome to our TTS system!",
        language="english",
        voice_name="en-US-Standard-A",
        output_path="demo_english.mp3"
    )
    
    # Urdu
    urdu_file = tts.text_to_speech(
        text="السلام علیکم، ہمارے TTS سسٹم میں خوش آمدید!",
        language="urdu",
        voice_name="ur-PK-Standard-A",
        output_path="demo_urdu.mp3"
    )
    
    # Hindi
    hindi_file = tts.text_to_speech(
        text="नमस्ते, हमारे TTS सिस्टम में आपका स्वागत है!",
        language="hindi",
        voice_name="hi-IN-Standard-A",
        output_path="demo_hindi.mp3"
    )
    
    print(f"Generated files: {english_file}, {urdu_file}, {hindi_file}")

if __name__ == "__main__":
    demo_multi_language()
```

### Example 2: Custom Voice Effects
```python
def demo_voice_effects():
    tts = GoogleTTSClient()
    
    # Slow, low-pitched voice
    slow_voice = tts.text_to_speech(
        text="This is a slow, deep voice",
        language="english",
        voice_name="en-US-Standard-B",
        speaking_rate=0.6,
        pitch=-5.0,
        output_path="slow_voice.mp3"
    )
    
    # Fast, high-pitched voice
    fast_voice = tts.text_to_speech(
        text="This is a fast, high-pitched voice",
        language="english",
        voice_name="en-US-Standard-A",
        speaking_rate=1.5,
        pitch=8.0,
        output_path="fast_voice.mp3"
    )
    
    # Loud voice with echo effect
    loud_voice = tts.text_to_speech(
        text="This is a loud voice with effects",
        language="english",
        voice_name="en-US-Standard-C",
        volume_gain_db=6.0,
        output_path="loud_voice.mp3"
    )
```

### Example 3: Batch Processing with Different Languages
```python
def demo_batch_processing():
    tts = GoogleTTSClient()
    
    # Mixed language texts
    texts = [
        "Welcome to our system",
        "ہمارے سسٹم میں خوش آمدید",
        "हमारे सिस्टम में आपका स्वागत है",
        "Thank you for using our service",
        "ہماری سروس استعمال کرنے کا شکریہ",
        "हमारी सेवा का उपयोग करने के लिए धन्यवाद"
    ]
    
    # Generate all in English
    english_files = tts.batch_text_to_speech(
        texts=texts,
        language="english",
        output_dir="batch_english"
    )
    
    # Generate each in its native language
    for i, text in enumerate(texts):
        if i % 3 == 0:  # English
            lang = "english"
        elif i % 3 == 1:  # Urdu
            lang = "urdu"
        else:  # Hindi
            lang = "hindi"
        
        tts.text_to_speech(
            text=text,
            language=lang,
            output_path=f"native_lang_{i+1}.mp3"
        )
```

### Example 4: Integration with SadTalker API
```python
import requests
import base64

def generate_audio_for_sadtalker():
    tts = GoogleTTSClient()
    
    # Generate speech
    audio_file = tts.text_to_speech(
        text="Hello, this is a test for SadTalker integration",
        language="english",
        voice_name="en-US-Standard-A"
    )
    
    # Create SadTalker job
    with open(audio_file, 'rb') as f:
        audio_data = f.read()
    
    # Convert to base64 for API
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    
    # Send to SadTalker API
    response = requests.post('http://localhost:7860/api/text-to-speech', json={
        'text': 'Hello, this is a test for SadTalker integration',
        'language_code': 'en-US'
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"Generated audio: {result['filename']}")
        return result['audio_data']
    
    return None
```

---

## 🚨 Error Handling

### Common Error Scenarios

#### 1. Authentication Errors
```python
try:
    tts = GoogleTTSClient("invalid_credentials.json")
except ValueError as e:
    print(f"Authentication error: {e}")
    # Handle: Check credentials file path and validity
```

#### 2. Invalid Language Codes
```python
try:
    output = tts.text_to_speech(
        text="Test",
        language="invalid_language"
    )
except ValueError as e:
    print(f"Language error: {e}")
    # Handle: Use supported language codes
```

#### 3. Network/API Errors
```python
try:
    output = tts.text_to_speech("Test text")
    if output is None:
        print("TTS generation failed")
        # Handle: Check network connection and API quotas
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Error Response Handling
```python
def safe_tts_generation(text, language="english"):
    try:
        tts = GoogleTTSClient()
        output = tts.text_to_speech(text, language=language)
        
        if output:
            return {"success": True, "file": output}
        else:
            return {"success": False, "error": "TTS generation failed"}
            
    except ValueError as e:
        return {"success": False, "error": f"Configuration error: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e}"}

# Usage
result = safe_tts_generation("Hello, world!")
if result["success"]:
    print(f"Audio generated: {result['file']}")
else:
    print(f"Error: {result['error']}")
```

---

## ⚡ Performance Tips

### 1. Batch Processing
```python
# Efficient: Process multiple texts in one call
texts = ["Text 1", "Text 2", "Text 3"]
files = tts.batch_text_to_speech(texts, language="english")

# Less efficient: Individual calls
files = []
for text in texts:
    file = tts.text_to_speech(text, language="english")
    files.append(file)
```

### 2. Voice Caching
```python
# Cache voice configurations
voice_configs = {
    "english_female": VoiceConfig(
        language_code="en-US",
        voice_name="en-US-Standard-A",
        ssml_gender="FEMALE"
    ),
    "urdu_male": VoiceConfig(
        language_code="ur-PK",
        voice_name="ur-PK-Standard-B",
        ssml_gender="MALE"
    )
}

# Reuse configurations
def generate_with_cached_voice(text, voice_type):
    config = voice_configs[voice_type]
    return tts.synthesize_speech(text, config, AudioConfig())
```

### 3. Audio Format Optimization
```python
# For web delivery: Use MP3
web_config = AudioConfig(
    audio_encoding="MP3",
    sample_rate_hertz=22050  # Lower quality for smaller files
)

# For high quality: Use WAV
hq_config = AudioConfig(
    audio_encoding="LINEAR16",
    sample_rate_hertz=44100  # Higher quality
)
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "API key is required" Error
```bash
# Solution: Ensure credentials file exists
ls -la revoiz-ai-dd6bb5e7b3ee.json

# Or set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

#### 2. "Voice not found" Warning
```python
# Check available voices
voices = tts.get_available_voices("english")
print(voices.keys())

# Use a valid voice name
output = tts.text_to_speech(
    text="Test",
    language="english",
    voice_name="en-US-Standard-A"  # Use valid voice
)
```

#### 3. Network/Quota Issues
```python
# Check API quotas in Google Cloud Console
# Implement retry logic
import time

def tts_with_retry(text, max_retries=3):
    for attempt in range(max_retries):
        try:
            return tts.text_to_speech(text)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise e
```

#### 4. File Permission Issues
```python
# Ensure output directory exists and is writable
import os

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

output = tts.text_to_speech(
    text="Test",
    output_path=os.path.join(output_dir, "test.mp3")
)
```

### Debug Mode
```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Initialize client with debug info
tts = GoogleTTSClient()
print(f"Available voices: {tts.get_available_voices()}")

# Test with simple text
output = tts.text_to_speech("Test", language="english")
print(f"Output: {output}")
```

---

## 📞 Support

### Getting Help
1. **Check Logs**: Enable debug logging for detailed error information
2. **Verify Credentials**: Ensure Google Cloud service account is properly configured
3. **Test Connectivity**: Verify network connection to Google Cloud APIs
4. **Check Quotas**: Ensure Text-to-Speech API quotas are not exceeded

### Useful Resources
- [Google Cloud Text-to-Speech Documentation](https://cloud.google.com/text-to-speech/docs)
- [Voice List Reference](https://cloud.google.com/text-to-speech/docs/voices)
- [API Quotas and Limits](https://cloud.google.com/text-to-speech/quotas)

---

This comprehensive documentation covers all aspects of the Google TTS Client implementation, from basic usage to advanced configuration and troubleshooting. The client provides a robust, production-ready solution for multi-language text-to-speech generation in your SadTalker application.
