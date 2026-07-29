# Gridy - Barangay Management & Resident Engagement System

Gridy is a comprehensive, all-in-one municipal management platform designed to streamline Barangay administration and enhance resident engagement. This repository houses the backend core APIs built with Django and Django REST Framework (DRF), complete with Role-Based Access Control (RBAC), multi-device push notification services, and automated data logging.

---

## 🛠️ Technology Stack

* **Framework:** Django 5.x & Django REST Framework (DRF)
* **Authentication:** JSON Web Tokens (SimpleJWT)
* **Database:** PostgreSQL (production-ready) / SQLite (development)
* **Media Hosting:** Cloudinary Integration (Multipart image parsing)
* **Push Notifications:** Firebase Cloud Messaging (FCM) via Firebase Admin SDK
* **Testing:** Django APITestCase (automated unit & integration testing)

---

## 📁 System Architecture (Backend Apps)

The system is structured as modular, decoupled Django applications:

1. **`gridy_auth` (Identity & RBAC):**
   * Custom `User` model supporting Roles (`ADMIN`, `RESIDENT`).
   * Auto-linked `Resident` profile table containing voter information and birth details.
   * Secure registration, login, and authenticated `/me/` details.
   * **Bulk Resident CSV Import:** Allows Barangay admins to upload resident spreadsheets to populate directories in bulk, auto-generating default passwords based on birthdates.
2. **`gridy_services` (Barangay Core Services):**
   * **Document Requests:** Handles residents' requests for certificates (Barangay Clearance, Indigency) and secures status validations (Approved/Rejected) exclusively to Barangay Officials.
   * **Hybrid Queuing System:** Generates auto-sequenced queue tickets (`T001`, `T002`, etc.) and manages live queue positions.
3. **`gridy_reports` (Incident Reporting):**
   * Exposes CRUD endpoints for hazard/broken infrastructure reporting.
   * Configured with multipart parsing to compress and stream attachments directly to Cloudinary.
4. **`gridy_communications` (Community Board & Alerts):**
   * Board announcements supporting priority pinning.
   * Community activities and event schedules.
   * Handles device token registrations (`FCMDevice`) and FCM notifications dispatching.

---

## ⚙️ Environment Configuration

Copy `backend/.env.example` to `backend/.env` and supply the required configurations:

```env
# Django Core Settings
DEBUG=True
SECRET_KEY=your-django-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key

# Cloudinary Integration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Firebase Push Alerts (FCM)
FIREBASE_SERVICE_ACCOUNT_JSON=relative/path/to/firebase-key.json
```

---

## 🚀 Quick Start Setup

Ensure you have Python 3.10+ installed.

### 1. Initialize Virtual Environment
```bash
# Run from Gridy root directory
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Project Dependencies
```bash
cd backend/
pip install -r requirements.txt
```

### 3. Setup Database & Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run Development Server
```bash
python manage.py runserver
```
The API browsable UI will be available at: [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)

---

## 🧪 Testing and Quality Assurance

The codebase includes an automated unit and integration test suite verifying endpoints, authorization boundaries, date validations, and transaction rollbacks.

To run the complete test suite:
```bash
# With venv activated inside backend/
python manage.py test
```

---

## 📄 Key Endpoints Reference

### 🔐 Authentication
* `POST /api/v1/auth/register/` - Create a resident profile.
* `POST /api/v1/auth/login/` - Authenticate and fetch access/refresh JWT tokens.
* `GET /api/v1/auth/me/` - Fetch currently logged-in account details.
* `POST /api/v1/auth/import-residents/` - (Admin only) Upload CSV spreadsheet to batch import residents.

### 📝 Services & Queue
* `POST /api/v1/document-requests/` - Request certificates.
* `PATCH /api/v1/document-requests/<id>/validate/` - (Admin only) Approve/Reject certificate requests.
* `POST /api/v1/tickets/` - Get queue ticket position (auto-generates ticket number).
* `GET /api/v1/tickets/live-status/` - Fetch live queue positions.
* `POST /api/v1/tickets/next/` - (Admin only) Advance queue to next active ticket.

### 📢 Communications & Incident Reporting
* `POST /api/v1/reports/` - Submit hazard reports with photo uploads.
* `POST /api/v1/announcements/` - (Admin only) Broadcast official board announcements.
* `POST /api/v1/devices/` - Register FCM device token for push notifications.
