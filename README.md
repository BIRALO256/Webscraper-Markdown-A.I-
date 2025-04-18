
# Tender Scraper & AI Extraction

## Overview
This is a demo project where I’m practicing and learning how to combine web scraping, data transformation, and AI-powered extraction.

The service scrapes public tender data, converts raw web content into Markdown, and uses a Language Model (LLM) to extract structured JSON data for further processing.


├── .env.example               # Template for environment variables (API keys, DB URIs)
├── .gitignore                 # Specifies files to be ignored by Git (e.g., venv, .env, logs)
├── Dockerfile                 # Defines container build (Python base image, dependencies)
├── docker-compose.yml         # Orchestrates multi-service setup (app, database, scheduler)
├── pyproject.toml             # Python project metadata and dependencies (uses uv)
├── uv.lock                    # Lockfile to ensure reproducible builds
├── README.md                  # Project overview and setup guide

├── .github/
│   └── workflows/             # GitHub Actions CI/CD pipelines
│       └── python-app.yml     # Workflow for linting, testing, and building the app

├── service/                   # Main FastAPI application logic
│   ├── __init__.py
│   ├── config.py              # Loads and manages environment configurations
│   ├── main.py                # FastAPI entry point: routes, startup hooks
│   └── scheduler.py           # Periodic scraping job definitions (APScheduler)

├── scraper/                   # Web scraping layer
│   ├── __init__.py
│   ├── playwright_scraper.py  # Browser-based scraper for dynamic pages (using Playwright)
│   └── html_scraper.py        # Lightweight scraper using Requests + BeautifulSoup

├── processor/                 # Data transformation & AI extraction
│   ├── __init__.py
│   ├── markdownifier.py       # Converts scraped HTML to Markdown
│   ├── llm_extractor.py       # Sends Markdown to LLM (e.g., OpenAI) and parses structured output
│   └── pdf_parser.py          # Extracts text from PDF documents via pdfplumber

├── storage/                   # Data persistence and export layer
│   ├── __init__.py
│   ├── firestore_client.py    # Firebase Firestore integration
│   ├── postgres_client.py     # PostgreSQL or Elasticsearch data storage
│   └── exporter.py            # CSV/Excel export utilities

└── tests/                     # Unit and integration tests
    ├── conftest.py            # Shared test fixtures (mock LLM, sample data)
    ├── test_playwright.py     # Playwright scraper tests
    ├── test_html_scraper.py   # HTML scraper tests
    ├── test_markdownifier.py  # Markdown conversion tests
    ├── test_llm_extractor.py  # LLM-based extraction tests
    └── test_exporter.py       # Exporter utility tests


 ##Key Design Decisions:

.env.example: Never commit secrets. Use environment variables for API keys and database URIs.

Containerization (Docker): Guarantees consistent runtime environments across dev, staging, and prod.

service/: Houses the FastAPI app and scheduler for periodic jobs (e.g., scraping every hour or daily).

scraper/** vs ****processor/**: Clear separation between data retrieval and data transformation/AI processing.

Scheduler: Uses APScheduler in service/scheduler.py to trigger scraping tasks on a configurable interval.

Storage: Flexible clients (Firestore for real-time, Postgres/ES for search) plus export utilities for CSV/Excel.

Testing: Comprehensive unit tests, with fixtures to mock external calls (LLM, browser, HTTP).

CI/CD: Workflow file runs lint (Ruff), formatting, unit tests, and container build on each push.