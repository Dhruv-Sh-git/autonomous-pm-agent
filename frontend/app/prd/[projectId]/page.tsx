'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import ReactMarkdown from 'react-markdown';
import { getToken } from '@/lib/api';

export default function PRDPage() {
  const router = useRouter();
  const params = useParams();
  const projectId = params.projectId as string;
  const [prdContent, setPrdContent] = useState<string>('');

  useEffect(() => {
    if (!getToken()) {
      router.push('/login');
      return;
    }

    // Get PRD from sessionStorage
    const storedPRD = sessionStorage.getItem('prd_output');
    if (storedPRD) {
      setPrdContent(storedPRD);
    } else {
      // If no PRD in session, redirect back to workspace
      router.push(`/workspace/${projectId}`);
    }
  }, [router, projectId]);

  if (!prdContent) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Product Requirements Document</h1>
          <button
            onClick={() => router.push(`/workspace/${projectId}`)}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
          >
            Back to Workspace
          </button>
        </div>

        <div className="bg-white p-8 rounded-lg shadow">
          <div className="prose max-w-none">
            <ReactMarkdown>{prdContent}</ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
}

