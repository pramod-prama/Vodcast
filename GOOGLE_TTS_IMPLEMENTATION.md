# 🌍 Google Cloud Text-to-Speech Implementation

## 📋 Overview
This implementation provides a comprehensive Google Cloud Text-to-Speech solution with multi-language support. It replaces the previous F5TTS implementation with a robust, production-ready TTS client supporting English, Urdu, and Hindi languages with multiple voice options for each.

## 🎤 Supported Languages & Voices

### 🇺🇸 English (US/UK/Australian)
- **en-US-Standard-A**: American English - Female
- **en-US-Standard-B**: American English - Male
- **en-US-Standard-C**: American English - Female
- **en-US-Standard-D**: American English - Male
- **en-US-Standard-E**: American English - Female
- **en-US-Standard-F**: American English - Female
- **en-US-Standard-G**: American English - Female
- **en-US-Standard-H**: American English - Female
- **en-US-Standard-I**: American English - Male
- **en-US-Standard-J**: American English - Male
- **en-GB-Standard-A**: British English - Female
- **en-GB-Standard-B**: British English - Male
- **en-GB-Standard-C**: British English - Female
- **en-GB-Standard-D**: British English - Male
- **en-AU-Standard-A**: Australian English - Female
- **en-AU-Standard-B**: Australian English - Male
- **en-AU-Standard-C**: Australian English - Female
- **en-AU-Standard-D**: Australian English - Male

### 🇵🇰 Urdu (Pakistan)
- **ur-PK-Standard-A**: Urdu (Pakistan) - Female
- **ur-PK-Standard-B**: Urdu (Pakistan) - Male
- **ur-PK-Standard-C**: Urdu (Pakistan) - Female
- **ur-PK-Standard-D**: Urdu (Pakistan) - Male

### 🇮🇳 Hindi (India)
- **hi-IN-Standard-A**: Hindi (India) - Female
- **hi-IN-Standard-B**: Hindi (India) - Male
- **hi-IN-Standard-C**: Hindi (India) - Female
- **hi-IN-Standard-D**: Hindi (India) - Male

## 🔧 TTS Client Implementation

### Core Classes

#### `GoogleTTSClient`
Main client class providing comprehensive TTS functionality:

```python
from f5tts_client_api import GoogleTTSClient, VoiceConfig, AudioConfig

# Initialize client
tts = GoogleTTSClient(credentials_path="revoiz-ai-dd6bb5e7b3ee.json")

# Simple usage
output_file = tts.text_to_speech(
    text="Hello, world!",
    language="english",
    output_path="output.mp3"
)
```

#### `VoiceConfig`
Voice configuration dataclass:
```python
voice_config = VoiceConfig(
    language_code="en-US",
    voice_name="en-US-Standard-A",
    ssml_gender="FEMALE",
    speaking_rate=1.0,
    pitch=0.0,
    volume_gain_db=0.0
)
```

#### `AudioConfig`
Audio output configuration:
```python
audio_config = AudioConfig(
    audio_encoding="MP3",  # MP3, LINEAR16, OGG_OPUS
    sample_rate_hertz=22050,
    effects_profile_id=None
)
```

## 📡 API Integration

### Endpoint: `POST /api/text-to-speech`

#### Request Body
```json
{
    "text": "Your text here",
    "language_code": "en-US",  // Optional, defaults to "en-US"
    "voice_name": "en-US-Standard-A",  // Optional
    "speaking_rate": 1.0,  // Optional, 0.25 to 4.0
    "pitch": 0.0,  // Optional, -20.0 to 20.0
    "volume_gain_db": 0.0  // Optional, -96.0 to 16.0
}
```

#### Response
```json
{
    "status": "success",
    "message": "Text converted to speech successfully in English (US)",
    "audio_data": "base64_encoded_mp3_data",
    "filename": "generated_speech_en-US_1234567890.mp3",
    "language_code": "en-US",
    "language_name": "English (US)",
    "file_size": 12345,
    "audio_format": "mp3",
    "voice_name": "en-US-Standard-A"
}
```

## Frontend Changes

### Language Selection
- Added dropdown menu with language options
- Visual flags for each language (🇺🇸 🇵🇰 🇮🇳)
- Language selection is sent with the API request

### Audio Format
- Changed from WAV to MP3 format for better compression
- Updated file input to accept MP3 files
- Updated audio blob creation to handle MP3 format

## Configuration

### Required Files
- `revoiz-ai-dd6bb5e7b3ee.json` - Google Cloud service account credentials
- Must have Text-to-Speech API enabled in Google Cloud Console

### Dependencies
- `requests` - For making HTTP requests to Google Cloud API
- `google-auth` - For authentication (already included in requirements.txt)
- `google-cloud-storage` - For GCS integration (already included in requirements.txt)

## Testing

### Manual Testing
1. Start the API server: `python real_api_server.py`
2. Open the frontend: `sadtalker-frontend-demo/demo.html`
3. Select a language from the dropdown
4. Enter text and click "Generate Speech"
5. The generated MP3 audio will be automatically loaded into the audio file input

### Automated Testing
Run the test scripts:
```bash
# Test the API endpoint
python test_google_tts.py

# Test direct curl-style requests (requires gcloud CLI)
python test_curl_tts.py
```

These will test all three languages and save the generated audio files.

## Error Handling
- Validates language codes against supported languages
- Provides clear error messages for invalid inputs
- Handles Google Cloud API errors gracefully
- Falls back to informative error messages

## Implementation Details

### REST API Approach
The implementation uses direct HTTP requests to Google Cloud Text-to-Speech API, matching the curl request format:

```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "x-goog-user-project: revoiz-ai" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "input": {"text": "Your text here"},
    "voice": {
      "languageCode": "ur-IN",
      "name": "ur-IN-Standard-A",
      "ssmlGender": "FEMALE"
    },
    "audioConfig": {"audioEncoding": "MP3"}
  }' \
  "https://texttospeech.googleapis.com/v1/text:synthesize"
```

### Authentication
- Uses service account credentials from `revoiz-ai-dd6bb5e7b3ee.json`
- Generates OAuth2 access tokens for API requests
- Includes `x-goog-user-project: revoiz-ai` header for billing

## Benefits
1. **High Quality**: Google Cloud TTS provides superior audio quality
2. **Multiple Languages**: Support for English, Urdu, and Hindi
3. **Better Compression**: MP3 format reduces file sizes
4. **Cloud-based**: No local TTS engine dependencies
5. **Scalable**: Can easily add more languages by updating the voice configuration
6. **REST API**: Direct HTTP requests for better control and debugging
