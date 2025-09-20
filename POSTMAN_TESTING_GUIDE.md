# SadTalker API Testing with Postman

## 🚀 Server Setup

The SadTalker API server is now running on `http://localhost:7860` and can handle real file uploads!

## 📋 Available Endpoints

### 1. Health Check
- **Method**: GET
- **URL**: `http://localhost:7860/api/health`
- **Description**: Check if the API is running

### 2. Create Job (with real files)
- **Method**: POST
- **URL**: `http://localhost:7860/api/jobs`
- **Content-Type**: `multipart/form-data`
- **Required Files**:
  - `source_image`: Image file (PNG, JPG, JPEG)
  - `driven_audio`: Audio file (WAV, MP3, MP4)
- **Optional Parameters**:
  - `preprocess`: "crop" (default)
  - `still_mode`: "false" (default)
  - `use_enhancer`: "false" (default)
  - `batch_size`: "1" (default)
  - `size`: "256" (default)
  - `pose_style`: "0" (default)

### 3. Get Job Status
- **Method**: GET
- **URL**: `http://localhost:7860/api/jobs/{job_id}`
- **Description**: Check the status and progress of a job

### 4. List All Jobs
- **Method**: GET
- **URL**: `http://localhost:7860/api/jobs`
- **Description**: Get a list of all jobs

### 5. Delete Job
- **Method**: DELETE
- **URL**: `http://localhost:7860/api/jobs/{job_id}`
- **Description**: Delete a specific job

### 6. Download Result Files
- **Method**: GET
- **URL**: `http://localhost:7860/api/results/{job_id}/{filename}`
- **Description**: Download result files (e.g., output.mp4)

## 🧪 Testing Steps

### Step 1: Import Postman Collection
1. Open Postman
2. Click "Import" button
3. Select the `SadTalker_API_Postman_Collection.json` file
4. The collection will be imported with all endpoints

### Step 2: Test Health Check
1. Select "Health Check" request
2. Click "Send"
3. You should get a response like:
```json
{
  "status": "healthy",
  "message": "SadTalker API is running",
  "timestamp": 1757876421.1140838,
  "active_jobs": 0
}
```

### Step 3: Test File Upload
1. Select "Create Job (Basic)" request
2. In the Body tab, select "form-data"
3. For `source_image` and `driven_audio`:
   - Change type from "Text" to "File"
   - Click "Select Files" and choose your image and audio files
4. Click "Send"
5. You should get a response with a job_id

### Step 4: Check Job Status
1. Copy the job_id from the previous response
2. Select "Get Job Status" request
3. Replace `{{job_id}}` in the URL with the actual job_id
4. Click "Send"
5. You should see the job status and progress

### Step 5: Download Results
1. Once the job is completed, use the "Download Result Files" request
2. Replace `{job_id}` and `{filename}` in the URL
3. For example: `http://localhost:7860/api/results/your-job-id/output.mp4`

## 📁 File Locations

- **Uploaded files**: `uploads/` directory
- **Results**: `results/{job_id}/` directory
- **Example files**: `examples/source_image/` and `examples/driven_audio/`

## 🔧 Example Files Available

You can use these example files for testing:
- **Images**: `examples/source_image/people_0.png`, `art_0.png`, etc.
- **Audio**: `examples/driven_audio/bus_chinese.wav`, `chinese_news.wav`, etc.

## 📊 Expected Response Format

### Job Creation Response:
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

### Job Status Response:
```json
{
  "job_id": "a8435aad-1a00-4eb0-b751-282b30d2b21e",
  "status": "completed",
  "progress": 100,
  "created_at": 1757876421.1140838,
  "result_path": "results/a8435aad-1a00-4eb0-b751-282b30d2b21e/output.mp4",
  "s3_url": "http://localhost:7860/api/results/a8435aad-1a00-4eb0-b751-282b30d2b21e/output.mp4"
}
```

## 🎯 Testing Tips

1. **File Types**: Make sure to use supported file types (PNG/JPG for images, WAV/MP3 for audio)
2. **File Size**: Keep files reasonably sized for faster processing
3. **Job ID**: Always copy the job_id from the creation response for status checks
4. **Progress**: Jobs typically take 10-15 seconds to complete
5. **Results**: Check the `results/` directory to see all generated files

## 🚨 Troubleshooting

- **Connection refused**: Make sure the server is running (`python simple_api_server.py`)
- **File not found**: Check that the job_id exists and the job is completed
- **Upload failed**: Verify file types and sizes are within limits
- **Server error**: Check the server console for error messages

## 📝 Notes

- This is a simplified version that handles real file uploads and processing
- The actual SadTalker inference is simulated (creates mock output files)
- For production use, you would need to integrate with the real SadTalker processing pipeline
- All uploaded files are stored locally in the `uploads/` directory
- Results are stored in the `results/` directory with job-specific folders
