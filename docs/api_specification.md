# Gridy API Endpoint Specification

This document provides detailed request/response payloads and routing instructions for frontend (React) and mobile (Flutter) developers integration.

---

## 1. Authentication & User Management

### 1.1 Register Account
* **Endpoint:** `POST /api/v1/auth/register/`
* **Headers:** `Content-Type: application/json`
* **Request Payload:**
  ```json
  {
    "username": "juan_resident",
    "password": "SecurePassword123!",
    "email": "juan@example.com",
    "role": "Resident",
    "full_name": "Juan Dela Cruz",
    "birth_date": "1994-05-12",
    "contact_number": "09171234567"
  }
  ```
* **Success Response (201 Created):**
  ```json
  {
    "username": "juan_resident",
    "email": "juan@example.com",
    "role": "Resident"
  }
  ```

### 1.2 Login (JWT Token)
* **Endpoint:** `POST /api/v1/auth/login/`
* **Headers:** `Content-Type: application/json`
* **Request Payload:**
  ```json
  {
    "username": "juan_resident",
    "password": "SecurePassword123!"
  }
  ```
* **Success Response (200 OK):**
  ```json
  {
    "access": "eyJhbGciOiJIUzI1NiIsIn...",
    "refresh": "eyJhbGciOiJIUzI1NiIsIn..."
  }
  ```

### 1.3 Get Logged-in User Profile
* **Endpoint:** `GET /api/v1/auth/me/`
* **Headers:** `Authorization: Bearer <access_token>`
* **Success Response (200 OK):**
  ```json
  {
    "id": 2,
    "username": "juan_resident",
    "email": "juan@example.com",
    "role": "Resident",
    "profile": {
      "full_name": "Juan Dela Cruz",
      "birth_date": "1994-05-12",
      "contact_number": "09171234567",
      "voter_status": false
    }
  }
  ```

### 1.4 Bulk Import Residents
* **Endpoint:** `POST /api/v1/auth/import-residents/`
* **Headers:** 
  * `Authorization: Bearer <access_token>` (Admin only)
  * `Content-Type: multipart/form-data`
* **Request Payload (Form-data):**
  * `file`: (Select `.csv` file)
* **CSV Format:**
  ```csv
  username,email,full_name,birth_date,contact_number,voter_status
  juan_dela_cruz,juan@example.com,Juan Dela Cruz,1995-10-15,09170000001,True
  maria_santos,,Maria Santos,1998-04-20,,False
  ```
* **Success Response (200 OK / 207 Multi-Status):**
  ```json
  {
    "imported": 2,
    "skipped_due_to_duplicate": 0,
    "errors": []
  }
  ```

---

## 2. Barangay Core Services & Queue

### 2.1 Request a Document
* **Endpoint:** `POST /api/v1/document-requests/`
* **Headers:** `Authorization: Bearer <access_token>`
* **Request Payload:**
  ```json
  {
    "document_type": "Barangay Clearance",
    "purpose": "Employment"
  }
  ```
* **Success Response (201 Created):**
  ```json
  {
    "id": 1,
    "user": 2,
    "document_type": "Barangay Clearance",
    "purpose": "Employment",
    "status": "PENDING",
    "created_at": "2026-07-29T16:00:00Z"
  }
  ```

### 2.2 Validate/Process Document (Official Only)
* **Endpoint:** `PATCH /api/v1/document-requests/<id>/validate/`
* **Headers:** `Authorization: Bearer <access_token>` (Admin only)
* **Request Payload:**
  ```json
  {
    "status": "APPROVED" 
  }
  ```
  *(Status options: `APPROVED`, `REJECTED`)*
* **Success Response (200 OK):**
  ```json
  {
    "id": 1,
    "status": "APPROVED"
  }
  ```
  *(Automatically triggers a push notification to the resident informing them of the status update).*

### 2.3 Generate Queue Ticket
* **Endpoint:** `POST /api/v1/tickets/`
* **Headers:** `Authorization: Bearer <access_token>`
* **Success Response (201 Created):**
  ```json
  {
    "id": 4,
    "ticket_number": "T004",
    "status": "WAITING",
    "created_at": "2026-07-29T16:05:00Z"
  }
  ```

### 2.4 Get Live Queue Positions
* **Endpoint:** `GET /api/v1/tickets/live-status/`
* **Headers:** `Authorization: Bearer <access_token>`
* **Success Response (200 OK):**
  ```json
  {
    "serving_ticket": "T001",
    "your_ticket": "T004",
    "tickets_waiting_ahead": 2
  }
  ```

### 2.5 Advance Queue to Next Ticket (Official Only)
* **Endpoint:** `POST /api/v1/tickets/next/`
* **Headers:** `Authorization: Bearer <access_token>` (Admin only)
* **Success Response (200 OK):**
  ```json
  {
    "detail": "Serving ticket T002"
  }
  ```
  *(Automatically triggers a push notification alerting the ticket holder that their turn is next).*

---

## 3. Incident Reports (Hazard Reporting)

### 3.1 Submit Incident Report (with attachment)
* **Endpoint:** `POST /api/v1/reports/`
* **Headers:**
  * `Authorization: Bearer <access_token>`
  * `Content-Type: multipart/form-data`
* **Request Payload (Form-data):**
  * `title`: "Broken Streetlight"
  * `description`: "Streetlight at Purok 4 is flashing and broken."
  * `location`: "Purok 4 near Chapel"
  * `image`: (Select binary photo attachment)
* **Success Response (201 Created):**
  ```json
  {
    "id": 12,
    "title": "Broken Streetlight",
    "description": "Streetlight at Purok 4 is flashing and broken.",
    "location": "Purok 4 near Chapel",
    "image_url": "https://res.cloudinary.com/demo/image/upload/v1234/report_broken_streetlight.jpg",
    "status": "PENDING"
  }
  ```

---

## 4. Notifications & Communications

### 4.1 Register Device token
* **Endpoint:** `POST /api/v1/devices/`
* **Headers:** `Authorization: Bearer <access_token>`
* **Request Payload:**
  ```json
  {
    "registration_id": "ExponentPushToken[fcm-token-string]"
  }
  ```
* **Success Response (201 Created):**
  ```json
  {
    "id": 1,
    "registration_id": "ExponentPushToken[fcm-token-string]"
  }
  ```
