# SadTalker API Frontend Demo

A complete React.js frontend application for testing all SadTalker API endpoints. This demo provides a user-friendly interface to interact with the SadTalker API and test all functionality.

## 🚀 Features

- **Complete API Testing**: Test all 6 API endpoints
- **Real-time Job Monitoring**: Live progress tracking with polling
- **File Upload**: Drag & drop support for images and audio
- **Job Management**: Create, view, delete jobs
- **Video Preview**: Built-in video player for generated content
- **Responsive Design**: Works on desktop and mobile
- **Error Handling**: Comprehensive error messages and validation
- **Health Monitoring**: API status checking

## 📋 API Endpoints Tested

1. **GET /api/health** - Health check
2. **POST /api/jobs** - Create new job
3. **GET /api/jobs** - List all jobs
4. **GET /api/jobs/{id}** - Get job status
5. **DELETE /api/jobs/{id}** - Delete job
6. **GET /api/results/{id}/{file}** - Download results

## 🛠️ Setup Instructions

### Prerequisites

- Node.js (version 14 or higher)
- SadTalker API server running on `http://localhost:7860`

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd sadtalker-frontend-demo
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   ```
   http://localhost:3000
   ```

### API Server Setup

Make sure the SadTalker API server is running:

```bash
# In the main project directory
python simple_api_server.py
```

The API should be available at `http://localhost:7860`

## 🎯 How to Use

### 1. Create Job Tab
- Upload an image file (PNG, JPG, JPEG)
- Upload an audio file (WAV, MP3, MP4)
- Configure parameters (size, pose style, etc.)
- Click "Create Job" to start processing
- Monitor real-time progress

### 2. All Jobs Tab
- View all created jobs
- See job status and progress
- Download completed videos
- Delete jobs
- Refresh the list

### 3. Job Status Tab
- Enter a job ID to check specific job status
- View detailed job information
- Download completed videos
- Monitor progress in real-time

### 4. Health Check Tab
- Check API server status
- View server information
- Monitor active jobs

## 📁 Project Structure

```
sadtalker-frontend-demo/
├── public/
│   └── index.html
├── src/
│   ├── App.js          # Main application component
│   ├── App.css         # Component-specific styles
│   ├── index.js        # Application entry point
│   └── index.css       # Global styles
├── package.json        # Dependencies and scripts
└── README.md          # This file
```

## 🎨 Features Breakdown

### File Upload
- **Drag & Drop**: Intuitive file selection
- **File Validation**: Automatic file type checking
- **Preview**: Shows selected file names
- **Multiple Formats**: Supports all required file types

### Job Management
- **Real-time Updates**: Automatic status polling
- **Progress Tracking**: Visual progress bars
- **Status Indicators**: Color-coded job states
- **Bulk Operations**: View and manage multiple jobs

### Video Handling
- **Built-in Player**: Preview generated videos
- **Download Support**: Direct download links
- **Format Support**: MP4 video playback
- **Responsive**: Works on all screen sizes

### Error Handling
- **Validation**: Client-side form validation
- **API Errors**: Server error display
- **Network Issues**: Connection error handling
- **User Feedback**: Toast notifications

## 🔧 Configuration

### API Base URL
To change the API server URL, modify the `API_BASE_URL` constant in `src/App.js`:

```javascript
const API_BASE_URL = 'http://your-api-server:port';
```

### Polling Interval
To adjust job status polling frequency, modify the interval in the `startPolling` function:

```javascript
const pollInterval = setInterval(async () => {
  // ... polling logic
}, 2000); // Change 2000ms to your preferred interval
```

## 🚀 Production Build

To create a production build:

```bash
npm run build
```

The build files will be in the `build/` directory.

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure the SadTalker API server is running
   - Check the API_BASE_URL in App.js
   - Verify CORS settings

2. **File Upload Issues**
   - Check file size limits
   - Ensure supported file formats
   - Verify file selection

3. **Job Status Not Updating**
   - Check network connection
   - Verify job ID is correct
   - Check browser console for errors

### Debug Mode

Enable debug logging by opening browser developer tools and checking the console for detailed error messages.

## 📱 Mobile Support

The application is fully responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones
- Touch devices

## 🔒 Security Notes

- No authentication required for demo
- File uploads are validated client-side
- API calls use standard HTTP methods
- No sensitive data is stored locally

## 🤝 Contributing

To contribute to this frontend demo:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues with this frontend demo:
- Check the browser console for errors
- Verify API server is running
- Check network connectivity
- Review the API documentation

## 🎉 Demo Tips

1. **Start with Health Check**: Verify API is running
2. **Use Sample Files**: Try the example files from the API
3. **Monitor Progress**: Watch real-time job updates
4. **Test All Tabs**: Explore all functionality
5. **Try Different Parameters**: Test various settings
6. **Download Results**: Verify video generation works

Enjoy testing the SadTalker API! 🎭✨
