# Vodcast - SadTalker API Integration

This repository includes a Gradio UI for SadTalker and now exposes a production-friendly API for React integration, including background jobs, WebSocket progress updates, and optional S3 uploads.

## Endpoints

- POST `/api/jobs`
  - Form (multipart/form-data):
    - `source_image` (file)
    - `driven_audio` (file)
    - Optional fields: `preprocess`, `still_mode`, `use_enhancer`, `batch_size`, `size`, `pose_style`
  - Response: `{ "status": "ok", "job_id": "<uuid>" }`

- GET `/api/jobs/{job_id}`
  - Response: `{ status, progress, result_path?, s3_url?, error?, last_event? }`

- WS `/ws/jobs/{job_id}`
  - Streams JSON events such as `{ "job_id": "...", "stage": "preprocess", "progress": 20, "message": "..." }`, finishing with `{ "stage": "done", "progress": 100, "output_path": "...", "s3_url": "..." }`.

## Environment Variables (S3)

- `S3_BUCKET` (optional): bucket to upload the final mp4
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`: AWS credentials

If `S3_BUCKET` is set and credentials are valid, the server uploads the result and returns `s3_url`.

## Run the server

```
pip install -r requirements.txt
python app_sadtalker.py
```

Production example:

```
uvicorn app_sadtalker:app --host 0.0.0.0 --port 7860
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


