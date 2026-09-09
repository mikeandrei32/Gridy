# Gridy - System Architecture

## 1. High-Level Architecture
Gridy follows a decoupled client-server architecture:
- **Frontend Client**: React Single Page Application (SPA) built with Vite and styled with Tailwind CSS, featuring dual-portal role segregation for Officials and Citizens.
- **Backend API**: Django REST Framework (DRF) serving JSON payloads and OpenAPI contracts.
- **Mobile Client**: Cross-platform Flutter mobile application providing feature parity for residents and field officials.

## 2. Infrastructure & Containerization
The system runs on a streamlined 3-tier Docker Compose architecture:
- **`gridy_backend`**: Django application server running Python 3.12 / DRF with native daemon background threads (`@async_task`).
- **`gridy_db`**: PostgreSQL 15 relational database for persistent, ACID-compliant data storage.
- **`gridy_frontend`**: Nginx web server serving compiled Vite production assets on port 80 and proxying API traffic.

## 3. Core Technologies
- **Language**: Python 3.12+, TypeScript, Dart
- **Frameworks**: Django 6.0+, DRF, React 19, Flutter 3.x
- **Database**: PostgreSQL 15
- **Task Management**: Python Daemon Threads (eliminates Celery & Redis overhead)
- **Real-Time Synchronization**: HTTP Interval Polling (3-second cadence)
- **State Management**: React Hooks, Context API
- **API Communication**: Axios with interceptors for JWT injection and silent 401 refresh

## 4. Security Architecture
- **Authentication**: JWT (JSON Web Tokens) with short-lived access tokens and HttpOnly rotating refresh cookies.
- **Data Isolation**: Multi-tenant-like data filtering overriding `get_queryset()` to ensure residents only see their own records.
- **Validation**: Strict serializer validation enforcing default creation states (e.g., stripping malicious admin parameters during record creation).

## 5. Third-Party Integrations
- **Firebase Admin SDK**: Used for dispatching Firebase Cloud Messaging (FCM) Push Notifications to mobile/web clients asynchronously.
