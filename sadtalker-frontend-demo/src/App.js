import React, { useState, useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';

// API Configuration
const API_BASE_URL = 'http://localhost:7860';

function App() {
  const [activeTab, setActiveTab] = useState('create');
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Health check state
  const [healthStatus, setHealthStatus] = useState(null);

  // Create job state
  const [formData, setFormData] = useState({
    source_image: null,
    driven_audio: null,
    preprocess: 'crop',
    still_mode: 'false',
    use_enhancer: 'false',
    batch_size: '1',
    size: '256',
    pose_style: '0'
  });

  // Job status polling
  const [pollingJobs, setPollingJobs] = useState(new Set());

  // Load jobs on component mount
  useEffect(() => {
    loadJobs();
    checkHealth();
  }, []);

  // Check API health
  const checkHealth = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/health`);
      const data = await response.json();
      setHealthStatus(data);
    } catch (error) {
      console.error('Health check failed:', error);
      setHealthStatus({ status: 'error', message: 'API not reachable' });
    }
  };

  // Load all jobs
  const loadJobs = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/jobs`);
      const data = await response.json();
      setJobs(data.jobs || []);
    } catch (error) {
      console.error('Failed to load jobs:', error);
      toast.error('Failed to load jobs');
    }
  };

  // Create new job
  const createJob = async (e) => {
    e.preventDefault();
    
    if (!formData.source_image || !formData.driven_audio) {
      toast.error('Please select both image and audio files');
      return;
    }

    setIsLoading(true);
    const jobFormData = new FormData();
    
    // Add files
    jobFormData.append('source_image', formData.source_image);
    jobFormData.append('driven_audio', formData.driven_audio);
    
    // Add parameters
    Object.keys(formData).forEach(key => {
      if (key !== 'source_image' && key !== 'driven_audio') {
        jobFormData.append(key, formData[key]);
      }
    });

    try {
      const response = await fetch(`${API_BASE_URL}/api/jobs`, {
        method: 'POST',
        body: jobFormData
      });

      const data = await response.json();
      
      if (response.ok) {
        toast.success('Job created successfully!');
        setSelectedJob(data);
        loadJobs(); // Refresh jobs list
        startPolling(data.job_id);
      } else {
        toast.error(data.error || 'Failed to create job');
      }
    } catch (error) {
      console.error('Error creating job:', error);
      toast.error('Failed to create job');
    } finally {
      setIsLoading(false);
    }
  };

  // Start polling for job status
  const startPolling = (jobId) => {
    setPollingJobs(prev => new Set([...prev, jobId]));
    
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/jobs/${jobId}`);
        const data = await response.json();
        
        if (data.status === 'completed' || data.status === 'failed') {
          clearInterval(pollInterval);
          setPollingJobs(prev => {
            const newSet = new Set(prev);
            newSet.delete(jobId);
            return newSet;
          });
          loadJobs(); // Refresh jobs list
          
          if (data.status === 'completed') {
            toast.success('Job completed successfully!');
          } else {
            toast.error('Job failed: ' + (data.error || 'Unknown error'));
          }
        }
      } catch (error) {
        console.error('Error polling job status:', error);
      }
    }, 2000);
  };

  // Get job status
  const getJobStatus = async (jobId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/jobs/${jobId}`);
      const data = await response.json();
      setSelectedJob(data);
    } catch (error) {
      console.error('Error getting job status:', error);
      toast.error('Failed to get job status');
    }
  };

  // Delete job
  const deleteJob = async (jobId) => {
    if (!window.confirm('Are you sure you want to delete this job?')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/jobs/${jobId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        toast.success('Job deleted successfully');
        loadJobs(); // Refresh jobs list
        if (selectedJob && selectedJob.job_id === jobId) {
          setSelectedJob(null);
        }
      } else {
        const data = await response.json();
        toast.error(data.error || 'Failed to delete job');
      }
    } catch (error) {
      console.error('Error deleting job:', error);
      toast.error('Failed to delete job');
    }
  };

  // Handle file upload
  const handleFileUpload = (field, file) => {
    setFormData(prev => ({
      ...prev,
      [field]: file
    }));
  };

  // Handle parameter change
  const handleParameterChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div className="container">
      <div className="header">
        <h1>🎭 Prama Vodcast</h1>
        {/* <p>Test all API endpoints for talking face video generation</p> */}
      </div>

      {/* Health Status */}
      {healthStatus && (
        <div className={`status-card ${healthStatus.status === 'healthy' ? 'completed' : 'failed'}`}>
          <strong>API Status:</strong> {healthStatus.status} - {healthStatus.message}
          {healthStatus.active_jobs !== undefined && (
            <span> | Active Jobs: {healthStatus.active_jobs}</span>
          )}
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'create' ? 'active' : ''}`}
          onClick={() => setActiveTab('create')}
        >
          🚀 Create Job
        </button>
        <button 
          className={`tab ${activeTab === 'jobs' ? 'active' : ''}`}
          onClick={() => setActiveTab('jobs')}
        >
          📋 All Jobs
        </button>
        <button 
          className={`tab ${activeTab === 'status' ? 'active' : ''}`}
          onClick={() => setActiveTab('status')}
        >
          📊 Job Status
        </button>
        <button 
          className={`tab ${activeTab === 'health' ? 'active' : ''}`}
          onClick={() => setActiveTab('health')}
        >
          ❤️ Health Check
        </button>
      </div>

      {/* Create Job Tab */}
      {activeTab === 'create' && (
        <div className="tab-content">
          <h2>Create New Job</h2>
          <form onSubmit={createJob}>
            <div className="grid">
              <div className="card">
                <h3>📁 File Upload</h3>
                
                <div className="form-group">
                  <label>Source Image *</label>
                  <div className="file-upload">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => handleFileUpload('source_image', e.target.files[0])}
                    />
                    <div className="file-upload-text">
                      {formData.source_image ? formData.source_image.name : 'Click to select image'}
                    </div>
                  </div>
                </div>

                <div className="form-group">
                  <label>Audio File *</label>
                  <div className="file-upload">
                    <input
                      type="file"
                      accept="audio/*"
                      onChange={(e) => handleFileUpload('driven_audio', e.target.files[0])}
                    />
                    <div className="file-upload-text">
                      {formData.driven_audio ? formData.driven_audio.name : 'Click to select audio'}
                    </div>
                  </div>
                </div>
              </div>

              <div className="card">
                <h3>⚙️ Parameters</h3>
                
                <div className="form-group">
                  <label>Preprocess</label>
                  <select 
                    value={formData.preprocess}
                    onChange={(e) => handleParameterChange('preprocess', e.target.value)}
                  >
                    <option value="crop">Crop</option>
                    <option value="resize">Resize</option>
                    <option value="full">Full</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Still Mode</label>
                  <select 
                    value={formData.still_mode}
                    onChange={(e) => handleParameterChange('still_mode', e.target.value)}
                  >
                    <option value="false">False</option>
                    <option value="true">True</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Use Enhancer</label>
                  <select 
                    value={formData.use_enhancer}
                    onChange={(e) => handleParameterChange('use_enhancer', e.target.value)}
                  >
                    <option value="false">False</option>
                    <option value="true">True</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Batch Size</label>
                  <select 
                    value={formData.batch_size}
                    onChange={(e) => handleParameterChange('batch_size', e.target.value)}
                  >
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="4">4</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Size</label>
                  <select 
                    value={formData.size}
                    onChange={(e) => handleParameterChange('size', e.target.value)}
                  >
                    <option value="256">256</option>
                    <option value="512">512</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Pose Style (0-45)</label>
                  <input
                    type="number"
                    min="0"
                    max="45"
                    value={formData.pose_style}
                    onChange={(e) => handleParameterChange('pose_style', e.target.value)}
                  />
                </div>
              </div>
            </div>

            <button type="submit" className="btn" disabled={isLoading}>
              {isLoading ? <span className="loading"></span> : '🚀 Create Job'}
            </button>
          </form>

          {/* Selected Job Display */}
          {selectedJob && (
            <div className="status-card">
              <h3>Selected Job</h3>
              <div className="response-display">
                {JSON.stringify(selectedJob, null, 2)}
              </div>
            </div>
          )}
        </div>
      )}

      {/* All Jobs Tab */}
      {activeTab === 'jobs' && (
        <div className="tab-content">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h2>All Jobs ({jobs.length})</h2>
            <button className="btn btn-secondary" onClick={loadJobs}>
              🔄 Refresh
            </button>
          </div>

          <div className="job-list">
            {jobs.length === 0 ? (
              <div className="status-card">
                <p>No jobs found. Create a job to get started!</p>
              </div>
            ) : (
              jobs.map(job => (
                <div key={job.job_id} className="job-item">
                  <div className="job-info">
                    <div className="job-id">ID: {job.job_id}</div>
                    <div className="job-status">
                      Status: {job.status} 
                      {pollingJobs.has(job.job_id) && <span className="loading" style={{ marginLeft: '10px' }}></span>}
                    </div>
                    <div className="job-progress">
                      Progress: {job.progress}% | 
                      Size: {job.size} | 
                      Created: {new Date(job.created_at * 1000).toLocaleString()}
                    </div>
                    {job.image_filename && (
                      <div className="job-progress">
                        Files: {job.image_filename} + {job.audio_filename}
                      </div>
                    )}
                  </div>
                  <div className="job-actions">
                    <button 
                      className="btn btn-secondary" 
                      onClick={() => getJobStatus(job.job_id)}
                    >
                      📊 Status
                    </button>
                    {job.status === 'completed' && job.s3_url && (
                      <a 
                        href={job.s3_url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="btn btn-success"
                      >
                        📥 Download
                      </a>
                    )}
                    <button 
                      className="btn btn-danger" 
                      onClick={() => deleteJob(job.job_id)}
                    >
                      🗑️ Delete
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Job Status Tab */}
      {activeTab === 'status' && (
        <div className="tab-content">
          <h2>Check Job Status</h2>
          <div className="form-group">
            <label>Job ID</label>
            <input
              type="text"
              placeholder="Enter job ID to check status"
              onChange={(e) => setSelectedJob({ job_id: e.target.value })}
            />
          </div>
          <button 
            className="btn" 
            onClick={() => selectedJob && getJobStatus(selectedJob.job_id)}
            disabled={!selectedJob?.job_id}
          >
            📊 Get Status
          </button>

          {selectedJob && selectedJob.status && (
            <div className="status-card">
              <h3>Job Status</h3>
              <div className="response-display">
                {JSON.stringify(selectedJob, null, 2)}
              </div>
              
              {selectedJob.status === 'processing' && (
                <div className="progress-container">
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ width: `${selectedJob.progress}%` }}
                    ></div>
                  </div>
                  <div className="progress-text">{selectedJob.progress}% Complete</div>
                </div>
              )}

              {selectedJob.status === 'completed' && selectedJob.s3_url && (
                <div className="video-container">
                  <h3>Generated Video</h3>
                  <video controls width="100%" maxWidth="600">
                    <source src={selectedJob.s3_url} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                  <br />
                  <a 
                    href={selectedJob.s3_url} 
                    download="talking_face_video.mp4"
                    className="btn btn-success"
                    style={{ marginTop: '10px' }}
                  >
                    📥 Download Video
                  </a>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Health Check Tab */}
      {activeTab === 'health' && (
        <div className="tab-content">
          <h2>API Health Check</h2>
          <button className="btn" onClick={checkHealth}>
            ❤️ Check Health
          </button>

          {healthStatus && (
            <div className="status-card">
              <h3>Health Status</h3>
              <div className="response-display">
                {JSON.stringify(healthStatus, null, 2)}
              </div>
            </div>
          )}
        </div>
      )}

      <ToastContainer 
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </div>
  );
}

export default App;
