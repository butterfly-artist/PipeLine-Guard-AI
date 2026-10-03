# PipeGuard AI — Data Quality & Pipeline Intelligence

> **From raw data to evidence-backed data-quality intelligence.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Challenge](https://img.shields.io/badge/MLH-Best_Open--Source_AI-blue.svg)](#hackathon-positioning)
[![Model](https://img.shields.io/badge/Model-Gemma_Open--Weight-red.svg)](#ai-role)

---

## 1. Project Identity

* **Project Name**: PipeGuard AI
* **Tagline**: From raw data to evidence-backed data-quality intelligence.
* **Challenge**: Best Open-Source AI Project (Model-Powered Tool)
* **Domain**: Data Engineering + AI
* **Primary Target Users**: Data Engineers, Analytics Engineers, ML Engineers, Data Platform Engineers, and Developers working with data pipelines.

---

## 2. Abstract

**PipeGuard AI** is a domain-agnostic data-quality and pipeline-intelligence tool that combines deterministic data profiling with an open-weight Gemma model to understand data quality issues, diagnose pipeline failures, analyze downstream impact, and recommend remediation.

Instead of treating an LLM as a generic chatbot, PipeGuard first extracts measurable evidence from datasets, schemas, relationships, and pipeline logs. This structured context is then provided to the open-weight AI model, which performs higher-level reasoning over the evidence.

The system can operate on different data domains such as e-commerce, real estate, finance, logistics, or other structured datasets without requiring a domain-specific model. It produces an evidence-backed diagnosis containing **root cause, impact analysis, remediation recommendations, and reusable data-quality rules**.

---

## 3. The Problem

Modern data pipelines often fail for reasons such as:
* Schema mismatches
* Missing values & duplicate records
* Invalid data types & broken references
* Inconsistent formats & invalid business values
* Lifecycle violations & pipeline transformation failures

Traditional DQ tools are good at deterministic validation. LLMs are good at interpreting unstructured context. **PipeGuard combines the two** to answer:
* **Why did it fail?**
* **What data caused the failure?**
* **What downstream assets are affected?**
* **What should the engineer do next?**
* **What rule should be introduced so the same failure doesn't happen again?**

---

## 4. Core Concept

```text
DETERMINISTIC COMPUTATION + OPEN-WEIGHT AI REASONING = DATA QUALITY INTELLIGENCE
```

Rather than feeding raw datasets directly into an LLM, PipeGuard extracts deterministic facts first:

```text
Dataset ──► Profiler ──► Facts ──► DQ Findings ──► Context Engine ──► Gemma (Open-Weight AI) ──► Reasoning ──► Diagnosis
```

---

## 5. Architectural Separation of Concerns

### Deterministic System (Python Backend)
* Row counts, column counts, and memory usage
* Data types, null percentages, duplicate detection, and cardinality
* Statistical distributions & pattern detection (regex/formatting)
* Referential integrity checks & schema validation
* Rule execution & failure count extraction

### Gemma Model (Open-Weight Reasoning Engine)
* Semantic interpretation of data anomalies
* Root-cause reasoning over pipeline failures
* Downstream impact assessment
* Actionable remediation recommendations
* Generation of reusable Data-Quality rules (YAML/JSON)
* Incident summarization and evidence grounding

---

## 6. Domain-Agnostic Design

PipeGuard does not hardcode domain knowledge (e.g., e-commerce vs. real estate vs. finance). Instead, it operates generically on:
```text
Dataset ──► Schema ──► Columns ──► Relationships ──► Constraints ──► Pipeline Context ──► DQ Results
```

Whether processing order transactions or real estate properties, PipeGuard uses the same underlying deterministic-profiling and AI-reasoning pipeline.

---

## 7. System Architecture

```text
                         ┌───────────────────┐
                         │       USER        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   REACT FRONTEND  │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    FASTAPI API    │
                         └─────────┬─────────┘
                                   │
             ┌─────────────────────┼────────────────────┐
             │                     │                    │
             ▼                     ▼                    ▼
      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
      │   INGESTOR  │      │  PROFILER   │      │ LOG PARSER  │
      └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  ▼
                         ┌───────────────────┐
                         │   SCHEMA ENGINE   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    DQ ENGINE      │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │  CONTEXT ENGINE   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │      GEMMA        │
                         │   OPEN-WEIGHT AI  │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ DIAGNOSIS ENGINE  │
                         └─────────┬─────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
               Root Cause       Impact       Remediation
                                                   │
                                                   ▼
                                            Quality Rules
```

---

## 8. Workflow

1. **Data Ingestion**: Multi-format support (`CSV`, `JSON`, `Parquet`).
2. **Data Profiler**: Dataset & column-level statistics, pattern analysis, relationship detection.
3. **Schema Engine**: Authoritative schema verification or suggested candidate schema generation.
4. **DQ Rule Engine**: Executable rule validation (`NOT_NULL`, `UNIQUE`, `RANGE`, `REFERENTIAL_INTEGRITY`).
5. **Context Engine**: Compiles deterministic findings, schema constraints, and pipeline logs into a compact AI context.
6. **Gemma Reasoning Engine**: Generates structured, evidence-grounded diagnosis.
7. **Actionable Outputs**: Root Cause, Impact Graph, Remediation Plan, and Reusable Quality Rules.
8. **Human Feedback Loop**: Validation interface for continuous evaluation and prompt refinement.

---

## 9. Inputs & Outputs

### Supported Inputs
* **Required**: Dataset (`CSV`, `JSON`, `Parquet`)
* **Optional**: Schema / Data Contract (`JSON`), Pipeline Logs (`.log`), DQ Rules (`YAML`/`JSON`), Data Dictionary, Lineage Information.

### Structured AI Output Contract
```json
{
  "severity": "HIGH",
  "root_cause": "payment_total fails reconciliation against corresponding order total for 2.4% of records.",
  "affected_entities": ["sample_payments.csv", "sample_orders.csv"],
  "affected_columns": ["payment_total", "order_amount"],
  "evidence": [
    {
      "source": "dq_result",
      "reference": "DQ-PAY-001",
      "observation": "17 payment records failed reconciliation against order total"
    }
  ],
  "impact": [
    {
      "asset": "gold_revenue_dashboard",
      "severity": "HIGH",
      "reason": "Inconsistent order payment values propagate to financial reporting dashboards."
    }
  ],
  "remediation": [
    {
      "action": "Quarantine failed records and re-process with corrected payment totals.",
      "priority": "HIGH"
    }
  ],
  "quality_rules": [
    {
      "name": "payment_order_reconciliation",
      "type": "RECONCILIATION",
      "column": "payment_total",
      "severity": "CRITICAL"
    }
  ]
}
```

---

## 10. Repository Folder Structure

```text
pipeLine-guard-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes (analyze, profile, rules, health)
│   │   ├── ai/           # Gemma client, context builder, diagnosis schema
│   │   ├── core/         # Config and logging utilities
│   │   ├── ingestion/    # Data loaders (CSV, JSON, Parquet)
│   │   ├── pipeline/     # Log parsing and lineage tracking
│   │   ├── profiling/    # Data profiler, statistics, patterns, schema detector
│   │   ├── quality/      # Rule engine, rules definition, validators
│   │   ├── services/     # Analysis and remediation orchestration services
│   │   └── main.py       # FastAPI application entrypoint
│   ├── tests/            # Backend unit & integration tests
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── components/   # UploadPanel, ProfileSummary, DiagnosisCard, EvidencePanel, ImpactGraph, RemediationPanel, QualityRules
│   │   ├── hooks/        # useAnalysis custom hook
│   │   ├── pages/        # Dashboard page
│   │   ├── services/     # API service client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── examples/
│   ├── cartflow/         # E-commerce sample dataset, schema, and logs
│   └── synthetic/        # Domain-agnostic synthetic sample datasets
│
├── prompts/              # Standardized LLM prompt templates
├── docs/                 # Architecture, AI design, DQ framework, evaluation docs
├── screenshots/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── LICENSE
└── README.md
```

---

## 11. Feature Roadmap (Scope Control)

### MVP (Must Have)
- [x] Multi-format ingestion (`CSV`, `JSON`, `Parquet`)
- [x] Automatic data profiling (Schema, Nulls, Duplicates, Statistics, Patterns)
- [x] Executable DQ Rule Engine (`NOT_NULL`, `UNIQUE`, `TYPE`, `RANGE`, `FORMAT`, `REFERENTIAL`)
- [x] Pipeline Context & Log parsing
- [x] Gemma Open-Weight AI diagnosis (Root cause, Downstream impact, Remediation, Rule generation)
- [x] Evidence grounding (linking AI claims directly to data facts)

### V2 Features
- [ ] Data lineage graph visualization
- [ ] Streaming event stream analysis
- [ ] Historical incident comparison
- [ ] Automated rule export to Great Expectations / Soda / dbt

---

## 12. Documentation Index

Detailed project specifications can be found in the [`docs/`](docs/) directory:
* [`docs/architecture.md`](docs/architecture.md): Deep dive into system architecture and data flow.
* [`docs/ai-design.md`](docs/ai-design.md): Details on Gemma integration, context optimization, and schema validation.
* [`docs/dq-framework.md`](docs/dq-framework.md): Data quality rule engine specifications and evidence extraction.
* [`docs/evaluation.md`](docs/evaluation.md): Ground truth dataset evaluation strategy and metrics.
* [`docs/demo.md`](docs/demo.md): Interactive 2-minute demonstration sequence.

---

## 13. Hackathon Quickstart

### 1. Run Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Run Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```

### 3. Run Automated Tests
```bash
python -m pytest backend/tests
```

### 4. Interactive Live Demo
Click **⚡ Run CartFlow Demo** on the frontend UI or execute `GET http://localhost:8000/api/demo`.

---

## 14. License

This project is open-source and released under the [MIT License](LICENSE).
