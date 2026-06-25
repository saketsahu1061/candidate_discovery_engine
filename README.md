# Automated Talent Intelligence Pipeline

An enterprise-grade, multi-stage heuristic processing funnel engineered to ingest, filter, and rank over 100k+ unstructured candidate profiles with zero-lag performance. Built to solve heavy computing bottlenecks, this pipeline implements memory-safe data streaming, rigid logistical drop-gates, and infrastructure-focused technical scoring matrices.

---

##  The Solution Overview

* **The Bottleneck:** Traditional applicant tracking pipelines suffer from memory-lock crashes when row-iterating large nested JSON fields, and standard keyword matchers fail by favoring shallow tutorial-level profiles.
* **Our Approach:** A decoupled, 3-stage cascading pipeline that uses fast programmatic drop-filters early on, saving up to 80% of downstream compute power while utilizing high-speed vectorized data handling.

---

##  Repository Architecture

```text
├── .streamlit/
│   └── config.toml             # Configuration setting the file upload cap to 2 GB
├── data/                       # Local target dataset directory (Git-ignored)
├── src/
│   ├── __init__.py             # Makes source directory importable
│   ├── data_streamer.py        # Memory-safe chunk-loading parser for CSV/JSON/JSONL
│   ├── utils.py                # High-speed vectorized data type normalization engine
│   ├── stage1_retrieval.py     # Binary gating engine tracking logistical dealbreakers
│   ├── stage2_reranker.py      # Multi-pillar technical depth scoring engine
│   ├── stage3_schema.py        # Output translation and factual reasoning template generator
│   └── scoring.py              # Orchestrator binding Stage 1 and Stage 2 workflows
├── app.py                      # Interactive Streamlit Web Application
├── main.py                     # Headless Automation Command-Line Interface (CLI)
├── .gitignore                  # Prevents tracking large datasets, cache, and environments
└── README.md                   # System documentation

```

---

##  Core Pipeline Stages

### Stage 1: Logistical Gating (`stage1_retrieval.py`)

Enforces hard binary thresholds on operational telemetry data. Instantly drops candidates with notice periods exceeding 90 days, interview completion rates under 50%, or backgrounds entirely confined to massive outsourcing IT consulting firms.

### Stage 2: Technical Reranker Core (`stage2_reranker.py`)

Applies a strict weighted score fusion matrix:

* **40% Core Infrastructure Depth:** Values experience with distributed systems (Ray, Spark, CUDA), vector databases, and metric frameworks over basic keyword text wrappers.
* **30% Target Alignment:** Optimizes for specific 5–9 year tenure windows and geographic tech hubs.
* **20% Strategic Nice-to-Haves:** Awards bonuses for domain context (HR-tech, marketplace) and model fine-tuning.
* **10% Early Readiness:** factors in recruiter response rates and verification flags.

### Stage 3: Standardized Schema Generator (`stage3_schema.py`)

Isolates the exact top-tier slice requested, down-scales final scores to a normalized format, and auto-generates deterministic, hallucination-free reasoning summaries using raw telemetry values.

---

##  Quick Start & Installation

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-username/talent-intelligence-pipeline.git
cd talent-intelligence-pipeline

# Initialize and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install required dependencies
pip install pandas streamlit

```

### 2. Run via Interactive UI

Launch the browser dashboard supporting streaming up to 2 GB file uploads with smooth state handling:

```bash
streamlit run app.py

```

### 3. Run via Headless CLI Core

Execute automated batch processing across local data paths directly from your terminal:

```bash
python main.py --input data/candidates_dataset.jsonl --count 100 --output final_submission.csv

```

---

##  Tech Stack & System Choices

* **Python & Pandas:** Chosen to enable vectorized array-mapping, eliminating slow row-by-row loops for fast execution.
* **Streamlit Framework:** Selected to deploy a zero-cost local interactive layout with minimal infrastructure overhead.
* **Heuristic Scoring Engine:** Bypasses heavy GPU-reliant LLM processing to achieve instant scaling with completely auditable, zero-hallucination results.


Here is the clean, copy-pasteable Docker Walkthrough section to add directly to your GitHub `README.md`:

```markdown
---

## 🐳 Docker Containerization & Walkthrough

To ensure environmental consistency and bypass local python path issues, you can containerize the entire application using Docker.

### 1. Project Dockerfile
Create a `Dockerfile` in the root directory of the project with the following configuration (includes the fix for container module resolution):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and python packages
RUN pip install --no-cache-dir pandas streamlit

# Set Python Path so the container safely resolves internal 'src' imports
ENV PYTHONPATH=/app

# Copy project files into the container working directory
COPY . .

EXPOSE 8501

```

### 2. Build the Image

Open your terminal in the project root directory and execute the build command:

```bash
docker build -t talent-pipeline .

```

### 3. Run the Containerized Ecosystem

Depending on your execution requirements, choose one of the two container modes below:

#### Option A: Spin Up the Interactive Web UI Dashboard

This maps container port 8501 to your local host machine, allowing you to access the dashboard via your browser.

```bash
docker run -p 8501:8501 talent-pipeline streamlit run app.py

```

* Once running, open your browser and navigate to: **`http://localhost:8501`**

#### Option B: Execute the Headless CLI (Batch Processing)

This uses volume mounting (`-v`) to bind your local `data/` folder inside the container workspace. This allows the docker container to read your local datasets and write the output files back to your local host.

**On Linux/macOS:**

```bash
docker run -v $(pwd)/data:/app/data talent-pipeline python main.py --input data/candidates_dataset.jsonl --count 100

```

**On Windows (PowerShell):**

```bash
docker run -v ${PWD}/data:/app/data talent-pipeline python main.py --input data/candidates_dataset.jsonl --count 100

```

---

```

```
