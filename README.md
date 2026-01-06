# DocuShield

**Hybrid AI Document Risk Analysis System**
*(Production-Inspired AI Engineering Project)*

---

## Overview

**DocuShield** is a hybrid AI system for analyzing legal contracts by integrating managed AI services, external LLM inference, and cloud-native infrastructure.

This project is **not about training models**.
It is about **engineering reliable systems around unreliable AI components**.

The system ingests legal documents, extracts structured text using AWS Textract, performs legal risk reasoning using an external LLM (Groq + Llama 3), stores operational results, and enables clause-level retrieval for question answering.

The primary goal is to demonstrate **real-world AI engineering practices**, not to build a toy LLM application.

---

## Core Problem This Project Solves

> **How do you build a reliable, observable, secure distributed system when the core intelligence (AI models) is probabilistic, slow, expensive, and failure-prone?**

DocuShield treats AI models as **external dependencies**, not magic.

---

## System Architecture (Mental Model)

The system is organized into **five layers**, each with a single responsibility:

```
┌─────────────────────────────┐
│  Streamlit (UI Layer)       │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  FastAPI (Orchestration)    │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  AI Services                │
│  - AWS Textract (OCR)       │
│  - Groq + Llama 3 (LLM)     │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  Storage & State            │
│  - S3 (Documents)           │
│  - DynamoDB (Results)       │
│  - FAISS (Vectors)          │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│  Infrastructure & Ops       │
│  - EKS (Kubernetes)         │
│  - IAM / IRSA               │
│  - Observability            │
└─────────────────────────────┘
```

---

## What This Project Is (And Is Not)

### This Project **IS**

* AI engineering
* Distributed systems design
* Cloud-native architecture
* Secure AI integration
* Observability-first development

### This Project **IS NOT**

* A production legal product
* A model training project
* A prompt-only LLM demo
* A frontend-heavy application
* A SaaS marketing prototype

---

## Technology Stack

### Frontend

* **Streamlit**

  * Internal operator UI
  * Document upload
  * Risk result inspection
  * “Chat with Contract” interface

### Backend

* **FastAPI**

  * Async orchestration layer
  * AI service coordination
  * API boundary enforcement

### AI Services

* **AWS Textract**

  * Managed OCR and layout extraction
* **Groq + Llama 3**

  * External LLM inference for reasoning

### Storage

* **AWS S3**

  * Immutable document storage
* **AWS DynamoDB**

  * Operational audit results
* **FAISS**

  * Clause-level vector retrieval

### Infrastructure

* **AWS EKS (Kubernetes)**
* **IAM + IRSA**
* **Terraform**
* **Prometheus + Grafana**
* **Locust (Load Testing)**

---

## Detailed Component Breakdown

### 1. Streamlit (UI Layer)

**Purpose**

* Acts as an internal operator console.

**Responsibilities**

* Upload PDF documents
* Trigger contract audits
* Display risk scores and flagged clauses
* Enable clause-grounded Q&A
* Show basic system metrics

**Explicit Non-Responsibilities**

* No authentication
* No business logic
* No AI calls
* No file processing

All logic flows through the backend API.

---

### 2. FastAPI (Backend Orchestrator)

**Purpose**

* Central control plane of the system.

**Why FastAPI**

* Async-first (critical for external APIs)
* Dependency injection
* Production-ready performance

**Responsibilities**

* Accept document uploads
* Store files in S3
* Trigger Textract jobs
* Poll async OCR results
* Call Groq for risk reasoning
* Normalize and validate AI outputs
* Persist results to DynamoDB
* Serve RAG-based queries

**Design Rule**

> FastAPI contains **no UI logic** and **no hardcoded credentials**.

---

### 3. AWS S3 (Document Storage)

**Purpose**

* Store raw, immutable contract PDFs.

**Storage Pattern**

```
s3://<bucket-name>/documents/{document_id}.pdf
```

**Why S3**

* Stateless compute
* Infinite scalability
* Durable storage
* Event-friendly architecture

This enforces **separation of compute and storage**.

---

### 4. AWS Textract (OCR & Layout Extraction)

**Purpose**

* Convert complex legal PDFs into structured text.

**Why Textract**

* Handles scanned documents
* Extracts tables and forms
* Production-grade managed ML

**Integration Flow**

1. Backend submits Textract job with S3 object
2. Textract processes asynchronously
3. Backend polls job status
4. Output is normalized into plain text

**Key Lesson**
Textract is treated as an **unreliable dependency**:

* Latency
* Timeouts
* Partial failures

---

### 5. Groq + Llama 3 (LLM Reasoning)

**Purpose**

* Perform legal risk analysis on extracted text.

**What the LLM Does**

* Assign risk score (0–100)
* Identify dangerous clauses
* Provide structured reasoning output

**Security Model**

* API key stored in Kubernetes Secret
* Injected at runtime
* Never committed
* Never hardcoded

**Engineering Focus**

* Retry logic
* Timeout handling
* Latency measurement
* Prompt versioning

This is **LLM integration**, not prompt hacking.

---

### 6. Prompt Engineering (Done Properly)

Prompts are:

* Versioned
* Stored as code
* Logged with outputs

LLMs are instructed to return **strict JSON**, not prose.

This enables:

* Schema validation
* Storage
* Prompt comparison
* Regression analysis

---

### 7. DynamoDB (Operational State)

**Purpose**

* Store AI audit results.

**Why DynamoDB**

* Simple access patterns
* High write throughput
* No relational complexity

**Stored Fields**

* `document_id` (partition key)
* `risk_score`
* `flagged_clauses`
* `model_version`
* `latency_ms`
* `timestamp`

This separates **operational data** from raw documents.

---

### 8. RAG System (Clause-Level Retrieval)

**Purpose**

* Enable grounded “Chat with Contract”.

**Key Design Decision**

> Chunking is done by **legal clauses**, not pages or tokens.

Each chunk includes:

* Clause text
* Clause type
* Document reference

**Vector Store**

* FAISS (local, per-document)

**RAG Flow**

1. User asks a question
2. Query is embedded
3. FAISS retrieves top clauses
4. Clauses passed to Groq
5. Answer generated with citations

This mitigates hallucinations and controls context size.

---

### 9. Kubernetes (EKS)

**Purpose**

* Run the system in a production-like environment.

**Services Deployed**

* FastAPI backend
* Streamlit frontend
* Observability stack (optional)

**Key Lessons**

* Stateless design
* Pod lifecycle management
* Horizontal scaling
* Service discovery

Without Kubernetes, this project would not qualify as AI engineering.

---

### 10. IAM + IRSA (Security Model)

**Purpose**

* Secure AWS access without credentials.

**How It Works**

* Kubernetes service account ↔ IAM role
* Pod assumes role automatically
* Access granted via IAM policies

**Result**

* No AWS keys in environment variables
* No secrets leakage
* Cloud-native security posture

This is a **senior-level AWS pattern**.

---

### 11. Observability (Prometheus + Grafana)

**Purpose**

* Measure reality instead of guessing.

**Metrics Collected**

* API latency (p50, p95)
* Error rates
* Request throughput
* CPU / memory usage

AI systems without observability are unusable in practice.

---

### 12. Load Testing (Locust)

**Purpose**

* Stress the system under real conditions.

**Scenarios**

* Concurrent uploads
* Concurrent audits
* Concurrent RAG queries

**Outcomes**

* Identify bottlenecks
* Observe scaling behavior
* Validate system assumptions

---

### 13. Infrastructure as Code (Terraform)

**Purpose**

* Reproducible infrastructure.

**Resources Managed**

* VPC
* EKS cluster
* S3 bucket
* DynamoDB table
* IAM roles

**Rule**

> Click-ops are forbidden.

---

### 14.LangSmith

**Use Case**

* Trace LLM calls
* Inspect prompt inputs/outputs
* Debug reasoning failures

**Non-Critical**

* Not required for correctness
* Used strictly for observability
