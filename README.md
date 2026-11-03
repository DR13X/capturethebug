<p align="center">
  <img src="https://img.shields.io/badge/Capturethebug-VAPT%20Report%20Automation-0f0f14?style=for-the-badge&logo=shield&logoColor=ff3b5c" alt="Capturethebug"/>
</p>

<h1 align="center">🐛 Capturethebug</h1>

<p align="center">
  <strong>Web VAPT Report Automation Platform</strong><br/>
  Turn raw scanner noise into polished, evidence-backed, client-ready security reports — in seconds.
</p>

<p align="center">
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick%20Start-black?style=flat-square&logo=terminal" alt="Quick Start"/></a>
  <a href="#-features"><img src="https://img.shields.io/badge/Features-Phase%201%20MVP-success?style=flat-square" alt="Features"/></a>
  <a href="#-report-formats"><img src="https://img.shields.io/badge/Reports-HTML%20%7C%20PDF%20%7C%20DOCX%20%7C%20JSON%20%7C%20CSV-blue?style=flat-square" alt="Formats"/></a>
  <a href="#-license"><img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License"/></a>
  <a href="https://github.com/DR13X/capturethebug"><img src="https://img.shields.io/badge/GitHub-DR13X%2Fcapturethebug-181717?style=flat-square&logo=github" alt="GitHub"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-ready-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Typer%20%2B%20Rich-CLI-ff69b4?style=flat-square" alt="CLI"/>
  <img src="https://img.shields.io/badge/SQLite-default-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite"/>
  <img src="https://img.shields.io/badge/ZAP%20%7C%20Nuclei%20%7C%20Nmap-parsers-orange?style=flat-square" alt="Parsers"/>
</p>

---

## Why Capturethebug?

Penetration testers spend hours after every engagement copy-pasting scanner output into Word docs, normalizing severity, writing the same remediation text, and formatting executive summaries.

**Capturethebug does that work for you.**

It sits *after* your existing tools (OWASP ZAP, Nuclei, Nmap, …). You import their exports, it normalizes findings, deduplicates them, maps CWE/OWASP, attaches remediation guidance, tracks validation and retesting status, and produces professional multi-format reports ready for the client.

> **Design principle:** No active scanning by default. Scope is explicit. Findings start as *Needs Validation* and must be confirmed before they appear as confirmed vulnerabilities in client reports.

---

## Features

| Module | What it does |
|--------|----------------|
| **Import pipeline** | Parse ZAP (JSON/XML), Nuclei (JSON/JSONL), Nmap (XML) into a single data model |
| **Finding correlation** | Fingerprint-based deduplication across scanners |
| **Risk engine** | Severity from scanner + CVSS bands + CWE knowledge base |
| **Evidence store** | Sanitized requests, responses, notes, and references |
| **Remediation guidance** | Auto-filled from CWE map (XSS, SQLi, BAC, CSRF, SSRF, …) |
| **Report builder** | Executive summary + severity breakdown + technical findings |
| **Retesting workflow** | Needs Validation → Confirmed / False Positive / Fixed / Reopened |
| **Scope enforcement** | Assessments declare authorized target URLs |
| **Audit trail** | Every status change is recorded |
| **CLI** | Beautiful Typer + Rich interface (`ctb`) |
| **REST API** | FastAPI endpoints for CI/CD and automation |

---

## Quick Start

```bash
# 1. Clone & install
git clone https://github.com/DR13X/capturethebug.git
cd capturethebug
pip install -e ".[dev]"

# 2. Initialize local SQLite DB (~/.capturethebug/ctb.db)
ctb init

# 3. Create an authorized assessment
ctb assessment create \
  --name "Example Corp Web App" \
  --client "Example Corp" \
  --target https://example.com \
  --assessor "Your Name"

# 4. Import scanner results
ctb import nuclei samples/nuclei-sample.jsonl -a <ASSESSMENT_ID>
ctb import zap    samples/zap-sample.json     -a <ASSESSMENT_ID>

# 5. Review & validate
ctb findings -a <ASSESSMENT_ID>
ctb validate <FINDING_ID> --status confirmed

# 6. Generate client-ready reports
ctb report -a <ASSESSMENT_ID> --format all -o ./reports
```

**One-command demo:**

```bash
make demo
```

**API server:**

```bash
uvicorn capturethebug.api.app:app --reload --port 8000
# → http://localhost:8000/docs
```

---

## Report Formats

| Format | Use case |
|--------|----------|
| **HTML** | Interactive dark-themed report for browsers |
| **PDF** | Formal client deliverable (ReportLab) |
| **DOCX** | Editable Word document |
| **JSON** | Machine-readable / CI pipelines |
| **CSV** | Spreadsheet import / ticketing systems |

### Report structure

```
Web Application Security Assessment
├── 1. Executive Summary
│   └── Severity breakdown (Critical · High · Medium · Low · Info)
└── 2. Technical Findings
    └── For each finding:
        · Title + Severity badge
        · CWE · Status · Scanner
        · Affected endpoint
        · Description / Impact / Remediation
        · Evidence notes (sanitized)
```

---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Scanner Export │────▶│  Parser Layer    │────▶│  Normalized     │
│  ZAP / Nuclei   │     │  (fingerprint)   │     │  Finding Model  │
│  Nmap / …       │     └──────────────────┘     └────────┬────────┘
└─────────────────┘                                       │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Report Engine  │◀────│  Intelligence    │◀────│  SQLite Store   │
│  HTML PDF DOCX  │     │  Dedup · CWE map │     │  + Audit Log    │
│  JSON CSV       │     │  Risk ranking    │     └─────────────────┘
└─────────────────┘     └──────────────────┘
         ▲
         │
┌─────────────────┐
│  CLI  (ctb)     │
│  FastAPI        │
└─────────────────┘
```

### Project layout

```
capturethebug/
├── src/capturethebug/
│   ├── models/          # Pydantic models & enums
│   ├── parsers/         # ZAP, Nuclei, Nmap
│   ├── intelligence/    # Dedup, CWE/OWASP mapping, risk
│   ├── reporting/       # Multi-format generators
│   ├── db/              # SQLAlchemy schema + repository
│   ├── api/             # FastAPI application
│   └── cli/             # Typer CLI
├── templates/reports/   # Jinja2 HTML template
├── samples/             # Example scanner exports
└── tests/
```

---

## CLI Cheat Sheet

| Command | Description |
|---------|-------------|
| `ctb init` | Create / migrate the local database |
| `ctb assessment create -n …` | Start a new engagement |
| `ctb assessment list` | List all assessments |
| `ctb import <scanner> <file> -a <id>` | Import findings (`zap` \| `nuclei` \| `nmap`) |
| `ctb findings -a <id>` | List findings (filter by severity/status) |
| `ctb validate <id> --status confirmed` | Confirm / mark FP / fixed / reopened |
| `ctb report -a <id> --format all` | Generate reports |

---

## Supported Scanners (Phase 1)

| Scanner | Formats | Notes |
|---------|---------|-------|
| **OWASP ZAP** | JSON, XML | Alerts + instances + CWE |
| **Nuclei** | JSON, JSONL | Template ID, CVSS, classification |
| **Nmap** | XML | Open ports + vuln scripts |

More parsers (Burp Suite, Nessus) planned for Phase 2.

---

## Roadmap

| Phase | Focus |
|-------|--------|
| **1 — MVP** | ZAP + Nuclei + Nmap import, normalize, dedupe, severity, HTML/PDF/DOCX/JSON/CSV, CLI + API |
| **2 — Advanced** | Burp Suite, richer evidence store, full CVSS calculator, reusable templates, retesting dashboards |
| **3 — Platform** | Multi-project web UI, historical comparison, RBAC, PostgreSQL, CI/CD plugins |

---

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -v
ruff check src tests
make demo
```

---

## License

MIT © Capturethebug contributors

---

<p align="center">
  <sub>Built for pentesters who would rather spend time finding bugs than formatting reports.</sub><br/>
  <sub>Keep active scanning optional. Validate before you report.</sub>
</p>
