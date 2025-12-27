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
        // Store the PRD output and navigate to viewer
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
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Project Workspace</h1>
          <button
            onClick={() => router.push('/dashboard')}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
          >
            Back to Dashboard
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        {uploadStatus && (
          <div className="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
            {uploadStatus}
          </div>
        )}

        {/* File Upload Section */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h2 className="text-xl font-semibold mb-4">Upload Document</h2>
          <div className="space-y-4">
            <div>
              <label htmlFor="file-input" className="block text-sm font-medium text-gray-700 mb-1">
                Select File (PDF or CSV)
              </label>
              <input
                id="file-input"
                type="file"
                accept=".pdf,.csv"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
            </div>
            {file && (
              <p className="text-sm text-gray-600">Selected: {file.name}</p>
            )}
            <button
              onClick={handleUpload}
              disabled={uploading || !file}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {uploading ? 'Uploading...' : 'Upload'}
            </button>
          </div>
        </div>

        {/* Agent Input Section */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Run Agent</h2>
          <form onSubmit={handleRunAgent} className="space-y-4">
            <div>
              <label htmlFor="goal" className="block text-sm font-medium text-gray-700 mb-1">
                Goal
              </label>
              <textarea
                id="goal"
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={4}
                placeholder="Enter the goal for the agent..."
              />
            </div>
            <button
              type="submit"
              disabled={running}
              className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {running ? 'Running Agent...' : 'Run Agent'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

