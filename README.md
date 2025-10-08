# Vodcast - SadTalker API Integration with Multi-Language TTS

This repository includes a comprehensive SadTalker API system with multi-language Text-to-Speech support. It features a production-ready API for React integration, background job processing, real-time progress updates, Google Cloud Storage integration, and advanced TTS capabilities supporting English, Urdu, and Hindi languages.

## 🎯 Key Features

- **🎭 SadTalker Integration**: Generate talking face videos from images and audio
- **🌍 Multi-Language TTS**: Google Cloud TTS supporting English, Urdu, and Hindi
- **⚡ Async Processing**: Background job processing with real-time progress updates
- **☁️ Cloud Storage**: Google Cloud Storage integration for scalable file management
- **🎨 Modern Frontend**: React-based web interface with real-time updates
- **🔧 Production Ready**: Comprehensive error handling and monitoring

## 📡 API Endpoints

### Video Generation
- **POST** `/api/jobs`
  - Form (multipart/form-data):
    - `source_image` (file)
    - `driven_audio` (file)
    - Optional fields: `preprocess`, `still_mode`, `use_enhancer`, `batch_size`, `size`, `pose_style`
  - Response: `{ "status": "ok", "job_id": "<uuid>" }`

- **GET** `/api/jobs/{job_id}`
  - Response: `{ status, progress, result_path?, s3_url?, error?, last_event? }`

### Text-to-Speech
- **POST** `/api/text-to-speech`
  - JSON body: `{ "text": "Your text", "language_code": "en-US" }`
  - Response: `{ "status": "success", "audio_data": "base64_encoded_mp3", "filename": "..." }`

### System Health
- **GET** `/api/health`
  - Response: `{ "status": "healthy", "message": "API is running", "active_jobs": 0 }`

## 🌍 Supported Languages

### Text-to-Speech Languages
- **🇺🇸 English (US)**: `en-US` - High-quality American English voices
- **🇵🇰 Urdu (Pakistan)**: `ur-PK` - Natural Urdu speech synthesis  
- **🇮🇳 Hindi (India)**: `hi-IN` - Clear Hindi voice generation

### Voice Options
Each language includes multiple voice options:
- **English**: 18 voices (US, UK, Australian accents, Male/Female)
- **Urdu**: 4 voices (Pakistani Urdu, Male/Female)
- **Hindi**: 4 voices (Indian Hindi, Male/Female)

## 🔧 Configuration

### Google Cloud Setup
- **Service Account**: `revoiz-ai-dd6bb5e7b3ee.json` (Text-to-Speech API enabled)
- **Storage Bucket**: `gcs-vodacast-bucket` for video file storage
- **Authentication**: Automatic OAuth2 token generation

### Environment Variables
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account JSON
- `GCS_BUCKET_NAME`: Google Cloud Storage bucket name

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Google Cloud Credentials
```bash
# Ensure your service account JSON is in place
cp revoiz-ai-dd6bb5e7b3ee.json gcs_credentials.json
```

### 3. Start the API Server
```bash
# Development
python real_api_server.py

# Production
uvicorn real_api_server:app --host 0.0.0.0 --port 7860
```

### 4. Access the Frontend
```bash
# Open in browser
open sadtalker-frontend-demo/demo.html
```

## 🎮 Usage Examples

### Text-to-Speech API
```javascript
// Generate English speech
const response = await fetch('/api/text-to-speech', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "Hello, this is a test",
    language_code: "en-US"
  })
});

// Generate Urdu speech
const urduResponse = await fetch('/api/text-to-speech', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "السلام علیکم، یہ ٹیسٹ ہے",
    language_code: "ur-PK"
  })
});
```

### Video Generation
```javascript
// Create talking face video
const formData = new FormData();
formData.append('source_image', imageFile);
formData.append('driven_audio', audioFile);

const job = await fetch('/api/jobs', {
  method: 'POST',
  body: formData
});
```

## Minimal React usage

```tsx
// api.ts
export async function startJob(baseUrl: string, data: FormData) {
  const res = await fetch(`${baseUrl}/api/jobs`, { method: 'POST', body: data });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ status: string; job_id: string }>; 
}

export function subscribeProgress(wsBaseUrl: string, jobId: string, onMessage: (evt: any) => void) {
  const ws = new WebSocket(`${wsBaseUrl.replace(/^http/, 'ws')}/ws/jobs/${jobId}`);
  ws.onmessage = (e) => onMessage(JSON.parse(e.data));
  return () => ws.close();
}
```

```tsx
// useGenerateVideo.tsx
import { useCallback, useEffect, useRef, useState } from 'react';
import { startJob, subscribeProgress } from './api';

export function useGenerateVideo(apiBase = 'http://localhost:7860') {
  const [jobId, setJobId] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const [status, setStatus] = useState<'idle' | 'running' | 'done' | 'error'>('idle');
  const [s3Url, setS3Url] = useState<string | null>(null);
  const unsub = useRef<() => void>();

  const generate = useCallback(async (sourceFile: File, audioFile: File, options?: Partial<{ preprocess: string; still_mode: boolean; use_enhancer: boolean; batch_size: number; size: number; pose_style: number }>) => {
    const form = new FormData();
    form.append('source_image', sourceFile);
    form.append('driven_audio', audioFile);
    if (options?.preprocess) form.append('preprocess', String(options.preprocess));
    if (options?.still_mode != null) form.append('still_mode', String(options.still_mode));
    if (options?.use_enhancer != null) form.append('use_enhancer', String(options.use_enhancer));
    if (options?.batch_size != null) form.append('batch_size', String(options.batch_size));
    if (options?.size != null) form.append('size', String(options.size));
    if (options?.pose_style != null) form.append('pose_style', String(options.pose_style));

    const { job_id } = await startJob(apiBase, form);
    setJobId(job_id);
    setStatus('running');

    unsub.current?.();
    unsub.current = subscribeProgress(apiBase, job_id, (evt) => {
      if (typeof evt.progress === 'number') setProgress(evt.progress);
      if (evt.stage === 'done') {
        setStatus('done');
        if (evt.s3_url) setS3Url(evt.s3_url);
      }
      if (evt.stage === 'error') {
        setStatus('error');
      }
    });
  }, [apiBase]);

  useEffect(() => () => { unsub.current?.(); }, []);

  return { generate, jobId, progress, status, s3Url };
}
```

## Performance recommendations

- Keep models loaded in GPU worker processes, 1 per GPU; consume jobs from a queue (Redis/RQ or Celery).
- Pre-warm models at startup; enable mixed precision (AMP) where safe; ensure fast disk for temp files.
- Store outputs in S3 and serve via CDN; limit maximum input duration to keep latency predictable.


