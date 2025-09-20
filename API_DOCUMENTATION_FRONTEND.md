# SadTalker API Documentation for Frontend Developers

## 🚀 Overview

The SadTalker API provides endpoints for creating talking face videos from static images and audio files. This API allows frontend applications to upload images and audio, process them, and download the generated talking face videos.

## 📋 Base URL

```
http://localhost:7860
```

## 🔧 Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

## 📊 API Endpoints

### 1. Health Check

**Endpoint:** `GET /api/health`

**Description:** Check if the API server is running and healthy.

**Request:**
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "SadTalker API is running",
  "timestamp": 1757876421.1140838,
  "active_jobs": 0
}
```

**Status Codes:**
- `200` - Server is healthy
- `500` - Server error

---

### 2. Create Job

**Endpoint:** `POST /api/jobs`

**Description:** Create a new job to generate a talking face video from an image and audio file.

**Request:**
```http
POST /api/jobs
Content-Type: multipart/form-data
```

**Form Data:**
| Field | Type | Required | Description | Default |
|-------|------|----------|-------------|---------|
| `source_image` | File | Yes | Image file (PNG, JPG, JPEG) | - |
| `driven_audio` | File | Yes | Audio file (WAV, MP3, MP4) | - |
| `preprocess` | String | No | Image preprocessing method | "crop" |
| `still_mode` | String | No | Whether to use still mode | "false" |
| `use_enhancer` | String | No | Whether to use face enhancement | "false" |
| `batch_size` | String | No | Batch size for processing | "1" |
| `size` | String | No | Output video size (256, 512) | "256" |
| `pose_style` | String | No | Pose style (0-45) | "0" |

**Example Request (JavaScript):**
```javascript
const formData = new FormData();
formData.append('source_image', imageFile);
formData.append('driven_audio', audioFile);
formData.append('preprocess', 'crop');
formData.append('still_mode', 'false');
formData.append('use_enhancer', 'false');
formData.append('batch_size', '1');
formData.append('size', '256');
formData.append('pose_style', '0');

fetch('http://localhost:7860/api/jobs', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Response:**
```json
{
  "job_id": "a8435aad-1a00-4eb0-b751-282b30d2b21e",
  "status": "created",
  "message": "Job created successfully",
  "preprocess": "crop",
  "still_mode": "false",
  "use_enhancer": "false",
  "batch_size": "1",
  "size": "256",
  "pose_style": "0",
  "image_filename": "people_0.png",
  "audio_filename": "bus_chinese.wav"
}
```

**Status Codes:**
- `200` - Job created successfully
- `400` - Bad request (missing files or invalid parameters)
- `500` - Server error

---

### 3. Get Job Status

**Endpoint:** `GET /api/jobs/{job_id}`

**Description:** Get the current status and progress of a specific job.

**Request:**
```http
GET /api/jobs/{job_id}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | String | Yes | The unique identifier of the job |

**Example Request:**
```javascript
fetch('http://localhost:7860/api/jobs/a8435aad-1a00-4eb0-b751-282b30d2b21e')
.then(response => response.json())
.then(data => console.log(data));
```

**Response:**
```json
{
  "job_id": "a8435aad-1a00-4eb0-b751-282b30d2b21e",
  "status": "completed",
  "progress": 100,
  "created_at": 1757876421.1140838,
  "preprocess": "crop",
  "still_mode": "false",
  "use_enhancer": "false",
  "batch_size": "1",
  "size": "256",
  "pose_style": "0",
  "image_path": "uploads/a8435aad-1a00-4eb0-b751-282b30d2b21e_image_people_0.png",
  "audio_path": "uploads/a8435aad-1a00-4eb0-b751-282b30d2b21e_audio_bus_chinese.wav",
  "result_path": "results/a8435aad-1a00-4eb0-b751-282b30d2b21e/output.mp4",
  "s3_url": "http://localhost:7860/api/results/a8435aad-1a00-4eb0-b751-282b30d2b21e/output.mp4"
}
```

**Job Statuses:**
- `created` - Job has been created
- `processing` - Job is being processed
- `completed` - Job completed successfully
- `failed` - Job failed with error

**Status Codes:**
- `200` - Job found
- `404` - Job not found
- `500` - Server error

---

### 4. List All Jobs

**Endpoint:** `GET /api/jobs`

**Description:** Get a list of all jobs in the system.

**Request:**
```http
GET /api/jobs
```

**Example Request:**
```javascript
fetch('http://localhost:7860/api/jobs')
.then(response => response.json())
.then(data => console.log(data));
```

**Response:**
```json
{
  "jobs": [
    {
      "job_id": "a8435aad-1a00-4eb0-b751-282b30d2b21e",
      "status": "completed",
      "progress": 100,
      "created_at": 1757876421.1140838,
      "preprocess": "crop",
      "still_mode": "false",
      "use_enhancer": "false",
      "batch_size": "1",
      "size": "256",
      "pose_style": "0",
      "image_filename": "people_0.png",
      "audio_filename": "bus_chinese.wav",
      "result_path": "results/a8435aad-1a00-4eb0-b751-282b30d2b21e/output.mp4",
      "s3_url": "http://localhost:7860/api/results/a8435aad-1a00-4eb0-b751-282b30d2b21e/output.mp4"
    }
  ],
  "total": 1
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

---

### 5. Delete Job

**Endpoint:** `DELETE /api/jobs/{job_id}`

**Description:** Delete a specific job and its associated files.

**Request:**
```http
DELETE /api/jobs/{job_id}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | String | Yes | The unique identifier of the job |

**Example Request:**
```javascript
fetch('http://localhost:7860/api/jobs/a8435aad-1a00-4eb0-b751-282b30d2b21e', {
  method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
```

**Response:**
```json
{
  "message": "Job a8435aad-1a00-4eb0-b751-282b30d2b21e deleted successfully"
}
```

**Status Codes:**
- `200` - Job deleted successfully
- `404` - Job not found
- `500` - Server error

---

### 6. Download Result Files

**Endpoint:** `GET /api/results/{job_id}/{filename}`

**Description:** Download result files (e.g., generated video) for a completed job.

**Request:**
```http
GET /api/results/{job_id}/{filename}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | String | Yes | The unique identifier of the job |
| `filename` | String | Yes | The name of the file to download |

**Example Request:**
```javascript
// Download the output video
window.open('http://localhost:7860/api/results/a8435aad-1a00-4eb0-b751-282b30d2b21e/output.mp4');

// Or fetch and handle the file
fetch('http://localhost:7860/api/results/a8435aad-1a00-4eb0-b751-282b30d2b21e/output.mp4')
.then(response => response.blob())
.then(blob => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'talking_face_video.mp4';
  a.click();
});
```

**Response:**
- Returns the file as binary data
- Content-Type depends on file type (e.g., `video/mp4` for MP4 files)

**Status Codes:**
- `200` - File found and returned
- `404` - File not found
- `500` - Server error

---

## 🎯 Frontend Integration Examples

### Complete React Component Example

```jsx
import React, { useState, useRef } from 'react';

const SadTalkerUpload = () => {
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [progress, setProgress] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);
  
  const imageRef = useRef(null);
  const audioRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!imageRef.current.files[0] || !audioRef.current.files[0]) {
      alert('Please select both image and audio files');
      return;
    }

    const formData = new FormData();
    formData.append('source_image', imageRef.current.files[0]);
    formData.append('driven_audio', audioRef.current.files[0]);
    formData.append('preprocess', 'crop');
    formData.append('still_mode', 'false');
    formData.append('use_enhancer', 'false');
    formData.append('batch_size', '1');
    formData.append('size', '256');
    formData.append('pose_style', '0');

    try {
      const response = await fetch('http://localhost:7860/api/jobs', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      setJobId(data.job_id);
      setIsProcessing(true);
      checkStatus(data.job_id);
    } catch (error) {
      console.error('Error creating job:', error);
    }
  };

  const checkStatus = async (jobId) => {
    try {
      const response = await fetch(`http://localhost:7860/api/jobs/${jobId}`);
      const data = await response.json();
      
      setStatus(data.status);
      setProgress(data.progress);
      
      if (data.status === 'completed') {
        setIsProcessing(false);
        setVideoUrl(data.s3_url);
      } else if (data.status === 'failed') {
        setIsProcessing(false);
        alert('Job failed: ' + (data.error || 'Unknown error'));
      } else if (data.status === 'processing') {
        // Check again in 2 seconds
        setTimeout(() => checkStatus(jobId), 2000);
      }
    } catch (error) {
      console.error('Error checking status:', error);
    }
  };

  return (
    <div className="sadtalker-upload">
      <h2>SadTalker Video Generator</h2>
      
      <form onSubmit={handleSubmit}>
        <div>
          <label>Source Image:</label>
          <input type="file" ref={imageRef} accept="image/*" required />
        </div>
        
        <div>
          <label>Audio File:</label>
          <input type="file" ref={audioRef} accept="audio/*" required />
        </div>
        
        <button type="submit" disabled={isProcessing}>
          {isProcessing ? 'Processing...' : 'Generate Video'}
        </button>
      </form>

      {isProcessing && (
        <div>
          <p>Status: {status}</p>
          <p>Progress: {progress}%</p>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      )}

      {videoUrl && (
        <div>
          <h3>Generated Video:</h3>
          <video controls width="400">
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <br />
          <a href={videoUrl} download="talking_face_video.mp4">
            Download Video
          </a>
        </div>
      )}
    </div>
  );
};

export default SadTalkerUpload;
```

### Vue.js Component Example

```vue
<template>
  <div class="sadtalker-upload">
    <h2>SadTalker Video Generator</h2>
    
    <form @submit.prevent="handleSubmit">
      <div>
        <label>Source Image:</label>
        <input 
          type="file" 
          ref="imageInput" 
          accept="image/*" 
          required 
        />
      </div>
      
      <div>
        <label>Audio File:</label>
        <input 
          type="file" 
          ref="audioInput" 
          accept="audio/*" 
          required 
        />
      </div>
      
      <button type="submit" :disabled="isProcessing">
        {{ isProcessing ? 'Processing...' : 'Generate Video' }}
      </button>
    </form>

    <div v-if="isProcessing">
      <p>Status: {{ status }}</p>
      <p>Progress: {{ progress }}%</p>
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :style="{ width: progress + '%' }"
        ></div>
      </div>
    </div>

    <div v-if="videoUrl">
      <h3>Generated Video:</h3>
      <video controls width="400">
        <source :src="videoUrl" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <br />
      <a :href="videoUrl" download="talking_face_video.mp4">
        Download Video
      </a>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      jobId: null,
      status: null,
      progress: 0,
      isProcessing: false,
      videoUrl: null
    };
  },
  methods: {
    async handleSubmit() {
      if (!this.$refs.imageInput.files[0] || !this.$refs.audioInput.files[0]) {
        alert('Please select both image and audio files');
        return;
      }

      const formData = new FormData();
      formData.append('source_image', this.$refs.imageInput.files[0]);
      formData.append('driven_audio', this.$refs.audioInput.files[0]);
      formData.append('preprocess', 'crop');
      formData.append('still_mode', 'false');
      formData.append('use_enhancer', 'false');
      formData.append('batch_size', '1');
      formData.append('size', '256');
      formData.append('pose_style', '0');

      try {
        const response = await fetch('http://localhost:7860/api/jobs', {
          method: 'POST',
          body: formData
        });
        
        const data = await response.json();
        this.jobId = data.job_id;
        this.isProcessing = true;
        this.checkStatus(data.job_id);
      } catch (error) {
        console.error('Error creating job:', error);
      }
    },

    async checkStatus(jobId) {
      try {
        const response = await fetch(`http://localhost:7860/api/jobs/${jobId}`);
        const data = await response.json();
        
        this.status = data.status;
        this.progress = data.progress;
        
        if (data.status === 'completed') {
          this.isProcessing = false;
          this.videoUrl = data.s3_url;
        } else if (data.status === 'failed') {
          this.isProcessing = false;
          alert('Job failed: ' + (data.error || 'Unknown error'));
        } else if (data.status === 'processing') {
          setTimeout(() => this.checkStatus(jobId), 2000);
        }
      } catch (error) {
        console.error('Error checking status:', error);
      }
    }
  }
};
</script>
```

## 🎨 CSS Styling

```css
.sadtalker-upload {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.sadtalker-upload form {
  margin-bottom: 20px;
}

.sadtalker-upload div {
  margin-bottom: 15px;
}

.sadtalker-upload label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.sadtalker-upload input[type="file"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.sadtalker-upload button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.sadtalker-upload button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.progress-bar {
  width: 100%;
  height: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #007bff;
  transition: width 0.3s ease;
}

.sadtalker-upload video {
  margin-top: 10px;
  border-radius: 4px;
}

.sadtalker-upload a {
  display: inline-block;
  margin-top: 10px;
  color: #007bff;
  text-decoration: none;
}

.sadtalker-upload a:hover {
  text-decoration: underline;
}
```

## 🔧 Error Handling

### Common Error Responses

```json
{
  "error": "Both source_image and driven_audio files are required"
}
```

```json
{
  "error": "Invalid file type"
}
```

```json
{
  "error": "Job not found"
}
```

### Error Handling in JavaScript

```javascript
const handleApiCall = async (url, options = {}) => {
  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// Usage
try {
  const result = await handleApiCall('http://localhost:7860/api/jobs', {
    method: 'POST',
    body: formData
  });
  console.log('Success:', result);
} catch (error) {
  alert('Error: ' + error.message);
}
```

## 📱 Mobile Considerations

- Use `accept` attributes on file inputs for better mobile experience
- Consider file size limits for mobile uploads
- Implement progress indicators for long-running operations
- Test on various mobile browsers

## 🔒 Security Notes

- Always validate file types on the frontend
- Consider implementing file size limits
- Sanitize user inputs
- Use HTTPS in production
- Implement rate limiting for API calls

## 🚀 Production Deployment

- Change base URL from `localhost:7860` to your production domain
- Implement proper error logging
- Add authentication if needed
- Use environment variables for configuration
- Implement proper CORS settings
- Add monitoring and health checks

## 📞 Support

For technical support or questions about the API, please refer to the main project documentation or contact the development team.
