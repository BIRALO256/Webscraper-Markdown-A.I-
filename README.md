
# Tender Scraper & AI Extraction

## Overview
This service scrapes public tenders, converts content to markdown, and uses an LLM to extract structured data.

├── .env.example               # Template for environment variables (API keys, DB URIs)
├── .gitignore                 # Exclude venv, .env, logs, etc.
├── Dockerfile                 # Defines container build (Python, dependencies)
├── docker-compose.yml         # Orchestrates services: app, database, scheduler
├── pyproject.toml             # Project metadata & dependencies (for uv)
├── uv.lock                    # Lockfile for reproducible installs
├── README.md                  # High-level overview and setup instructions
├── .github/
│   └── workflows/             # CI/CD pipelines (lint, tests, build)
│       └── python-app.yml
│
├── service/                   # Main application code
│   ├── __init__.py
│   │
│   ├── config.py              # Loads .env settings into Config object
│   ├── main.py                # FastAPI entrypoint; mounts routes & startup hooks
│   └── scheduler.py           # Defines periodic scraping jobs (APScheduler)
│   
├── scraper/                   # Web scraping logic
│   ├── __init__.py
│   ├── playwright_scraper.py  # Handles browser-based scraping (login, JS)
│   └── html_scraper.py        # Lightweight requests+BeautifulSoup scrapers
│
├── processor/                 # Data transformation & AI extraction
│   ├── __init__.py
│   ├── markdownifier.py       # Converts raw HTML to Markdown
│   ├── llm_extractor.py       # Sends markdown to LLM and parses JSON output
│   └── pdf_parser.py          # Extracts text from PDF using pdfplumber
│
├── storage/                   # Persistence layer
│   ├── __init__.py
│   ├── firestore_client.py    # Firebase Firestore integration
│   ├── postgres_client.py     # Optional PostgreSQL/Elasticsearch indexing
│   └── exporter.py            # CSV/Excel export utilities
│
└── tests/                     # Unit and integration tests
    ├── conftest.py            # Test fixtures (e.g., mock LLM, fake data)
    ├── test_playwright.py     # Tests for playwright_scraper
    ├── test_html_scraper.py   # Tests for html_scraper
    ├── test_markdownifier.py  # Tests for markdown conversion
    ├── test_llm_extractor.py  # Tests for LLM-based extraction
    └── test_exporter.py       # Tests for CSV/Excel export


 ##Key Design Decisions:

.env.example: Never commit secrets. Use environment variables for API keys and database URIs.

Containerization (Docker): Guarantees consistent runtime environments across dev, staging, and prod.

service/: Houses the FastAPI app and scheduler for periodic jobs (e.g., scraping every hour or daily).

scraper/** vs ****processor/**: Clear separation between data retrieval and data transformation/AI processing.

Scheduler: Uses APScheduler in service/scheduler.py to trigger scraping tasks on a configurable interval.

Storage: Flexible clients (Firestore for real-time, Postgres/ES for search) plus export utilities for CSV/Excel.

Testing: Comprehensive unit tests, with fixtures to mock external calls (LLM, browser, HTTP).

CI/CD: Workflow file runs lint (Ruff), formatting, unit tests, and container build on each push.