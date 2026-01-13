'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { uploadDocument, runAgent, getToken, removeToken } from '@/lib/api';

export default function WorkspacePage() {
  const router = useRouter();
  const params = useParams();
  const projectId = params.projectId as string;

  const [file, setFile] = useState<File | null>(null);
  const [goal, setGoal] = useState('');
  const [uploading, setUploading] = useState(false);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [uploadStatus, setUploadStatus] = useState('');

  useEffect(() => {
    if (!getToken()) {
      router.push('/login');
    }
  }, [router]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      // Check file type
      const allowedTypes = ['application/pdf', 'text/csv'];
      if (!allowedTypes.includes(selectedFile.type)) {
        setError('Please upload a PDF or CSV file');
        return;
      }
      setFile(selectedFile);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setError('');
    setUploading(true);
    setUploadStatus('');

    try {
      await uploadDocument(projectId, file);
      setUploadStatus('File uploaded successfully');
      setFile(null);
      // Reset file input
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (err) {
      if (err instanceof Error && err.message === 'Unauthorized') {
        removeToken();
        router.push('/login');
      } else {
        setError(err instanceof Error ? err.message : 'Upload failed');
      }
    } finally {
      setUploading(false);
    }
  };

  const handleRunAgent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!goal.trim()) {
      setError('Please enter a goal');
      return;
    }

    setError('');
    setRunning(true);

    try {
      const response = await runAgent(projectId, goal);
      if (response.final_output) {
        // Store the user input and PRD output and navigate to viewer
        sessionStorage.setItem('prd_input', goal);
        sessionStorage.setItem('prd_output', response.final_output);
        router.push(`/prd/${projectId}`);
      } else {
        setError('Agent run completed but no output generated');
      }
    } catch (err) {
      if (err instanceof Error && err.message === 'Unauthorized') {
        removeToken();
        router.push('/login');
      } else {
        setError(err instanceof Error ? err.message : 'Failed to run agent');
      }
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="min-h-screen gradient-bg">
      {/* Header */}
      <div className="glass border-b border-glass-border">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg shadow-primary/50">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-text-primary">Project Workspace</h1>
                <p className="text-sm text-text-secondary">Build your PRD with AI assistance</p>
              </div>
            </div>
            <button
              onClick={() => router.push('/dashboard')}
              className="btn-secondary flex items-center space-x-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              <span>Dashboard</span>
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 text-red-400 rounded-xl animate-fade-in">
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {error}
            </div>
          </div>
        )}

        {/* Success Alert */}
        {uploadStatus && (
          <div className="mb-6 p-4 bg-green-500/10 border border-green-500/50 text-green-400 rounded-xl animate-fade-in">
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {uploadStatus}
            </div>
          </div>
        )}

        {/* Workflow Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-4">
            <div className="flex items-center">
              <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white font-bold shadow-lg shadow-primary/50">
                1
              </div>
              <span className="ml-2 text-text-primary font-medium">Upload Docs</span>
            </div>
            <svg className="w-6 h-6 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
            <div className="flex items-center">
              <div className="w-10 h-10 rounded-full bg-secondary flex items-center justify-center text-white font-bold shadow-lg shadow-secondary/50">
                2
              </div>
              <span className="ml-2 text-text-primary font-medium">Set Goal</span>
            </div>
            <svg className="w-6 h-6 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
            <div className="flex items-center">
              <div className="w-10 h-10 rounded-full bg-accent flex items-center justify-center text-white font-bold shadow-lg shadow-accent/50">
                3
              </div>
              <span className="ml-2 text-text-primary font-medium">Generate PRD</span>
            </div>
          </div>
        </div>

        {/* File Upload Section */}
        <div className="card p-8 mb-6 animate-fade-in">
          <div className="flex items-center mb-6">
            <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center mr-3">
              <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-bold text-text-primary">Upload Document</h2>
              <p className="text-sm text-text-secondary">Upload PDFs or CSV files to provide context</p>
            </div>
          </div>
          
          <div className="space-y-6">
            <div className="border-2 border-dashed border-glass-border rounded-xl p-8 text-center hover:border-primary transition-colors">
              <input
                id="file-input"
                type="file"
                accept=".pdf,.csv"
                onChange={handleFileChange}
                className="hidden"
              />
              <label htmlFor="file-input" className="cursor-pointer">
                <div className="w-16 h-16 bg-gradient-to-br from-primary to-secondary rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-primary/30">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <p className="text-text-primary font-medium mb-1">Click to upload or drag and drop</p>
                <p className="text-text-secondary text-sm">PDF or CSV files only</p>
              </label>
            </div>
            
            {file && (
              <div className="flex items-center justify-between p-4 bg-primary/10 border border-primary/30 rounded-lg animate-fade-in">
                <div className="flex items-center space-x-3">
                  <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <div>
                    <p className="text-text-primary font-medium">{file.name}</p>
                    <p className="text-text-secondary text-xs">{(file.size / 1024).toFixed(2)} KB</p>
                  </div>
                </div>
                <button
                  onClick={() => setFile(null)}
                  className="text-text-muted hover:text-red-400 transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            )}
            
            <button
              onClick={handleUpload}
              disabled={uploading || !file}
              className="btn-primary w-full flex items-center justify-center space-x-2"
            >
              {uploading ? (
                <>
                  <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>Uploading...</span>
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <span>Upload Document</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Agent Input Section */}
        <div className="card p-8 animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <div className="flex items-center mb-6">
            <div className="w-10 h-10 bg-accent/20 rounded-lg flex items-center justify-center mr-3">
              <svg className="w-6 h-6 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-bold text-text-primary">Run AI Agent</h2>
              <p className="text-sm text-text-secondary">Let AI analyze and generate your PRD</p>
            </div>
          </div>
          
          <form onSubmit={handleRunAgent} className="space-y-6">
            <div>
              <label htmlFor="goal" className="label">
                Product Goal
              </label>
              <div className="mb-3 p-3 bg-accent/5 border border-accent/20 rounded-lg">
                <p className="text-xs text-text-secondary leading-relaxed">
                  💡 <strong className="text-text-primary">Pro tip:</strong> Describe your product goal in 1-3 sentences. 
                  Keep it short and high-level. For example: "Create a PRD for a feature that lets users upload and 
                  search through meeting notes." The AI will analyze your documents and generate a comprehensive PRD.
                </p>
              </div>
              <textarea
                id="goal"
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                required
                maxLength={600}
                className="input"
                rows={5}
                placeholder="Short, 1–3 sentence description of your product goal..."
              />
              <div className="mt-2 flex justify-between text-xs text-text-muted">
                <span>Maximum 600 characters</span>
                <span>{goal.length}/600</span>
              </div>
            </div>
            
            <button
              type="submit"
              disabled={running}
              className="btn-primary w-full flex items-center justify-center space-x-2"
              style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)' }}
            >
              {running ? (
                <>
                  <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>AI is working on your PRD...</span>
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <span>Generate PRD with AI</span>
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

