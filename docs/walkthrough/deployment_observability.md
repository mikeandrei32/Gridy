# Containerization & Observability Architecture

This guide details the Docker containerization architecture and the internal observability monitoring endpoints used in the Gridy project.

---

## 1. 3-Tier Container Topology (Docker Compose)

In accordance with **ADR 009** (*Stack Simplification & Defended Capstone Proposal Alignment*), the container architecture strictly adheres to the defended 3-tier specification:

* **`gridy_db` (PostgreSQL 15)**: Relational database storing citizen records, clearances, queue tickets, announcements, and audit trails.
* **`gridy_backend` (Django DRF via Gunicorn)**: RESTful API service exposing business logic, role-based authorization, and PDF clearance generation.
* **`gridy_frontend` (React + Vite via Nginx)**: Production administrative and citizen web portal served statically through Nginx on port 80.

To launch the entire system locally:
`docker compose up --build`

---

## 2. Decommissioning of Prometheus & Grafana

During initial prototyping, experimental Prometheus and Grafana monitoring containers were introduced. However:
1. **Contractual Scope Mismatch**: The defended Capstone manuscript (Table II) explicitly contracts a clean 3-tier architecture. Prometheus and Grafana were unapproved additions.
2. **Hardware Constraints**: Partner LGU hardware (Barangay Ibabang Dupay and Barangay Daungan) operate on standard office workstations where complex distributed monitoring agents consume excessive RAM.

Per **ADR 009**, Prometheus and Grafana were fully decommissioned, reducing system memory footprint by over 60%.

---

## 3. Native Observability: Structured Health Check Endpoint

In place of heavy external scraping daemons, Gridy exposes a lightweight, enterprise-standard health monitoring route:

* **Endpoint**: `GET /api/v1/health/`
* **Diagnostic Checks**:
  * **Database Latency**: Executes a live SQL probe against PostgreSQL, measuring query round-trip time in milliseconds.
  * **Cache / Memory Status**: Verifies local caching responsiveness.
  * **Service Readiness**: Reports overall HTTP 200 operational readiness without Celery or Redis dependencies.