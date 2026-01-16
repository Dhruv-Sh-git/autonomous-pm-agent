🚀 Agentic AI Platform with Retrieval-Augmented Generation (RAG)

A production-grade, multi-agent AI system that enables users to upload documents, create projects, and interact with intelligent agents capable of planning, researching, analyzing, and generating structured outputs — all grounded in private data.

🔥 Why This Project Exists

Most AI chatbots:

Hallucinate
Lack memory
Can’t reason across documents
Are single-prompt based

This platform solves that by combining:
✅ Agentic AI (LangGraph)
✅ Secure RAG pipeline
✅ Project-based document isolation
✅ Production deployment

🧠 Core Features

🔐 Authentication

Email-based OTP authentication (Resend API)
JWT-secured API routes
Future-ready for OAuth (Google Auth planned)

📂 Document Intelligence (RAG)

Upload PDF / CSV files
Automatic text extraction
Chunking with overlap
Vector embeddings

Semantic search with strict filtering:

user_id
project_id
document_id

🤖 Agentic AI Layer

Built using LangGraph, enabling:

Planner Agent → breaks user goals into tasks
Research Agent → retrieves context (documents + tools)
Analyzer Agent → performs reasoning
Generator Agent → produces structured outputs (PRDs, reports)

Supports:

Conditional execution
Shared memory
Tool retries
Future multi-agent expansion

🧱 Tech Stack

Backend

FastAPI (Python)
LangGraph
JWT Authentication
PostgreSQL (metadata & users)
Qdrant (vector database)

Frontend

Next.js
Deployed on Vercel

Infrastructure

Backend + DB: Railway
Frontend: Vercel
Dockerized services
AI / ML
Sentence Transformers
Retrieval-Augmented Generation (RAG)
Vector similarity search

🗂 Project Structure
backend/
 ├── app/
 │   ├── auth/        # OTP auth, JWT, dependencies
 │   ├── chat/        # Chat routes + agent execution
 │   ├── documents/  # Upload, parsing, chunking, embeddings
 │   ├── rag/         # Vector store + retrieval logic
 │   ├── llm/         # LLM clients (Groq)
 │   ├── projects/   # Project management
 │   ├── db/          # SQLAlchemy models & sessions
 │   └── main.py


🏗 High-Level Architecture
┌────────────┐
│  Frontend  │  (Next.js - Vercel)
└─────┬──────┘
      │ HTTPS + JWT
┌─────▼──────┐
│  FastAPI   │
│  Backend   │
│ (Railway)  │
└─────┬──────┘
      │
 ┌────▼─────────────┐
 │ Authentication   │
 │ OTP + JWT        │
 └────┬─────────────┘
      │
┌─────▼───────────┐
│ Project Layer   │
│ User Isolation  │
└─────┬───────────┘
      │
┌─────▼───────────┐
│ Document Service│
│ PDF / CSV Upload│
└─────┬───────────┘
      │
┌─────▼───────────┐
│ Chunking Engine │
│ Overlap Strategy│
└─────┬───────────┘
      │
┌─────▼───────────┐
│ Embeddings      │
│ Sentence Models │
└─────┬───────────┘
      │
┌─────▼───────────┐
│ Qdrant Vector DB│
│ (user+project)  │
└─────┬───────────┘
      │
┌─────▼───────────┐
│ Agentic Layer   │
│ LangGraph       │
│ Planner → Exec  │
└─────┬───────────┘
      │
┌─────▼───────────┐
│ LLM (Groq)      │
│ Context-Grounded│
└─────────────────┘

🔍 Key Design Decisions

Strict data isolation at vector DB level
Agent orchestration over prompt chaining
Stateless backend + persistent memory
Deployment-first mindset

🌍 Real-World Use Cases

Enterprise internal knowledge assistants
Product requirement document (PRD) generators
Legal / policy document analysis
Research copilots
Startup ideation & validation tools

📈 Outcomes

Reduced hallucinations by grounding responses in user data
Achieved sub-second semantic retrieval
Built with real production constraints (auth, deployment, infra)

🛠 Future Enhancements

Google OAuth
Streaming responses
Agent observability & tracing
Tool marketplace
Multi-user collaboration

👨‍💻 Author
Dhruv Shaswat
AI Systems · Backend · Agentic Architectures