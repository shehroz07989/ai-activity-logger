# AI Activity Logger

> Reliability and observability infrastructure for AI-powered workflows —
> retry logic, decision tracing, failure recovery, and execution transparency.

---

## Problem

Most AI applications focus only on generating outputs.

They ignore everything else:

- What happened when a call failed?
- How many retries occurred?
- Which step broke the workflow?
- What decision was made and why?
- How do you debug it later?

Without answers to these questions, AI systems become black boxes.
Failures are invisible. Debugging is guesswork.

---

## Solution

AI Activity Logger wraps your AI workflow with a structured
observability layer.

Every execution is tracked, every failure is recorded,
every retry is logged, every decision has an explanation.

**The system captures:**
- Inputs and outputs
- Step-by-step execution trace
- Retry attempts and outcomes
- AI-generated decision explanations
- Error categorization and recovery actions

---

## Current Features

### Input Validation
- Type checking and range validation
- Structured error responses

### API Integration Layer
- External API calls with timeout handling
- Response parsing and data extraction

### Reliability Engine
- Automatic retry on temporary failures
- Permanent failure detection and termination
- Exponential backoff between retries
- Per-attempt trace logging

### AI Explanation Layer
- AI-generated plain-English explanations for each workflow outcome
- Structured JSON output parsing
- Explanation storage alongside execution data

### Workflow Tracing
- Multi-step execution tracking
- Step ordering and status per step
- Attempt counts per workflow stage

### Persistent Storage
- SQLite-based log storage
- Full execution history
- Queryable by request ID

### REST API Access
- FastAPI endpoints for log retrieval
- Query logs by ID
- JSON responses

---

## Architecture

```text
User Input
    │
    ▼
Validation Layer
    │
    ▼
API Call Workflow
    │
    ▼
Retry Policy Engine
    │
    ▼
Data Extraction Layer
    │
    ▼
AI Explanation Workflow
    │
    ▼
SQLite Storage
    │
    ▼
FastAPI Access Layer
```

---

## Tech Stack

- Python
- FastAPI
- SQLite
- Requests
- python-dotenv

---

## Setup

```bash
# Clone the repo
git clone https://github.com/shehrozahmad/ai-activity-logger
cd ai-activity-logger

# Install dependencies
pip install -r requirements.txt

# Add your API key
cp .env.example .env
# Open .env and add your OPENROUTER_API_KEY

# Run
python main.py
```

---

## Project Structure

```text
project/
│
├── services/
│   ├── main_executor.py
│   ├── retry_policy.py
│   ├── trace_service.py
│   └── attempts_trace.py
│
├── work_flows/
│   ├── api_call_workflow.py
│   └── ai_workflow.py
│
├── domain_specific_functions/
│   ├── api_call_functions.py
│   └── ai_functions.py
│
├── general_functions/
│   └── utils.py
│
├── sqlite/
│   ├── data_base.py
│   └── system.db
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Roadmap

- [ ] Monitoring dashboard (success rate, fail rate, error trends)
- [ ] Automated scheduled runs
- [ ] Multi-agent workflow tracing
- [ ] Production deployment (VPS + background process)
- [ ] Analytics layer

---

## Author

**Shehroz Ahmad**

Building AI workflow systems to understand reliability, tracing, and observability in production environments.

Building production-grade infrastructure for AI workflows —
logging, tracing, retry systems, and failure recovery.

[GitHub](https://github.com/shehrozahmad)
[LinkedIn](https://linkedin.com/in/shehrozahmad)
