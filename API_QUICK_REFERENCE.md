# SadTalker API - Quick Reference

## 🚀 Base URL
```
http://localhost:7860
```

## 📋 Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/jobs` | Create new job |
| `GET` | `/api/jobs` | List all jobs |
| `GET` | `/api/jobs/{id}` | Get job status |
| `DELETE` | `/api/jobs/{id}` | Delete job |
| `GET` | `/api/results/{id}/{file}` | Download results |

## 🎯 Quick Start

### 1. Create Job
```javascript
const formData = new FormData();
formData.append('source_image', imageFile);
formData.append('driven_audio', audioFile);

fetch('http://localhost:7860/api/jobs', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data.job_id));
```

### 2. Check Status
```javascript
fetch(`http://localhost:7860/api/jobs/${jobId}`)
.then(res => res.json())
.then(data => {
  console.log(`Status: ${data.status}, Progress: ${data.progress}%`);
});
```

### 3. Download Video
```javascript
// Direct link
const videoUrl = `http://localhost:7860/api/results/${jobId}/output.mp4`;

// Or programmatically
fetch(videoUrl)
.then(res => res.blob())
.then(blob => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'video.mp4';
  a.click();
});
```

## 📊 Job Status Flow

```
created → processing → completed
    ↓         ↓           ↓
  0%        10-90%      100%
```

## 🔧 Required Parameters

### Create Job (POST /api/jobs)
- `source_image` (file) - Image file
- `driven_audio` (file) - Audio file

### Optional Parameters
- `still_mode` - "false" (default)
- `use_enhancer` - "false" (default)
- `batch_size` - "1" (default)
- `size` - "256" or "512" (default: "256")
- `pose_style` - "0" to "45" (default: "0")

## 📁 File Types

### Supported Image Formats
- PNG
- JPG
- JPEG

### Supported Audio Formats
- WAV
- MP3
- MP4

## ⚡ Response Examples

### Job Created
```json
{
  "job_id": "abc123...",
  "status": "created",
  "message": "Job created successfully"
}
```

### Job Processing
```json
{
  "job_id": "abc123...",
  "status": "processing",
  "progress": 45
}
```

### Job Completed
```json
{
  "job_id": "abc123...",
  "status": "completed",
  "progress": 100,
  "result_path": "results/abc123.../output.mp4",
  "s3_url": "http://localhost:7860/api/results/abc123.../output.mp4"
}
```

## 🚨 Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| `200` | Success | Continue |
| `400` | Bad Request | Check parameters |
| `404` | Not Found | Check job ID |
| `500` | Server Error | Retry later |

## 💡 Tips

1. **Polling**: Check status every 2-3 seconds during processing
2. **File Size**: Keep files under 50MB for better performance
3. **Timeout**: Jobs typically complete in 10-30 seconds
4. **Cleanup**: Delete completed jobs to save space
5. **CORS**: API supports CORS for web applications

## 🔄 Complete Workflow

```javascript
async function generateTalkingFace(imageFile, audioFile) {
  // 1. Create job
  const formData = new FormData();
  formData.append('source_image', imageFile);
  formData.append('driven_audio', audioFile);
  
  const createResponse = await fetch('http://localhost:7860/api/jobs', {
    method: 'POST',
    body: formData
  });
  const { job_id } = await createResponse.json();
  
  // 2. Poll for completion
  const pollStatus = async () => {
    const statusResponse = await fetch(`http://localhost:7860/api/jobs/${job_id}`);
    const status = await statusResponse.json();
    
    if (status.status === 'completed') {
      return status.s3_url; // Video URL
    } else if (status.status === 'failed') {
      throw new Error('Job failed');
    } else {
      // Still processing, check again in 2 seconds
      await new Promise(resolve => setTimeout(resolve, 2000));
      return pollStatus();
    }
  };
  
  return await pollStatus();
}
```
