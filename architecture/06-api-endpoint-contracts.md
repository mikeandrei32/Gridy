# 06 API Endpoint Contracts

## 1. RESTful Design
All endpoints enforce authorization using JWT Bearer tokens in the HTTP `Authorization` headers, except for the login and token refresh endpoints.

`Authorization: Bearer <access_token>`

---

## 2. API Endpoints

### 2.1 Authentication Module

#### POST `/api/v1/auth/login/`
*   **Description:** Authenticate users and return access/refresh tokens.
*   **Payload (JSON):**
    ```json
    {
      "username": "resident_username",
      "password": "securepassword"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "access": "eyJhbGciOi...",
      "refresh": "eyJhbGciOi...",
      "role": "RESIDENT"
    }
    ```

#### POST `/api/v1/auth/token/refresh/`
*   **Description:** Refresh an expired access token using a valid refresh token.
*   **Payload (JSON):**
    ```json
    {
      "refresh": "eyJhbGciOi..."
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "access": "eyJhbGciOi..."
    }
    ```

---

### 2.2 Communications Module

#### GET `/api/v1/announcements/`
*   **Description:** Retrieve announcements. Filterable by category query param (`AID`, `MEDICAL`, `EVENT`, `GENERAL`).
*   **Response (200 OK):**
    ```json
    [
      {
        "id": 1,
        "title": "Barangay General Assembly",
        "category": "GENERAL",
        "content": "Join us on Saturday at the basketball court.",
        "scheduled_date": "2026-07-25T09:00:00Z"
      }
    ]
    ```

#### POST `/api/v1/announcements/`
*   **Description:** Post a new announcement (Admin role authorization required).
*   **Payload (JSON):**
    ```json
    {
      "title": "Medical Mission 2026",
      "category": "MEDICAL",
      "content": "Free dental checkup and basic medicines.",
      "scheduled_date": "2026-08-01T08:00:00Z"
    }
    ```
*   **Response (201 Created):**
    ```json
    {
      "id": 2,
      "title": "Medical Mission 2026",
      "category": "MEDICAL",
      "content": "Free dental checkup and basic medicines.",
      "scheduled_date": "2026-08-01T08:00:00Z"
    }
    ```

---

### 2.3 Queue Management Module

#### GET `/api/v1/queue/live-status/`
*   **Description:** Poll real-time status of the current ticket serving state.
*   **Response (200 OK):**
    ```json
    {
      "current_ticket": "A-124",
      "total_waiting": 18,
      "avg_wait_mins": 12
    }
    ```

#### POST `/api/v1/queue/ticket/`
*   **Description:** Register a printed queue ticket to link to a resident's mobile phone (triggers QR scan action).
*   **Payload (JSON):**
    ```json
    {
      "ticket_number": "A-125",
      "service_type": "document_request"
    }
    ```
*   **Response (201 Created):**
    ```json
    {
      "ticket_id": 435,
      "ticket_number": "A-125",
      "status": "WAITING",
      "created_at": "2026-07-19T22:32:00Z"
    }
    ```

#### POST `/api/v1/queue/next/`
*   **Description:** Move the queue forward to the next ticket (Admin role authorization required). Triggers push notification to the resident.
*   **Response (200 OK):**
    ```json
    {
      "current_ticket": "A-125",
      "remaining_waiting": 17
    }
    ```

---

### 2.4 Document Request Module

#### GET `/api/v1/documents/`
*   **Description:** Get document request history.
    *   *Resident:* Returns only the logged-in resident's requests.
    *   *Admin:* Returns all resident requests in the barangay.
*   **Response (200 OK):**
    ```json
    [
      {
        "request_id": 12,
        "document_type": "Barangay Clearance",
        "status": "PENDING",
        "urgency_tag": "REGULAR",
        "requester_name": "Juan Dela Cruz"
      }
    ]
    ```

#### POST `/api/v1/documents/`
*   **Description:** Request a new official document (Resident only).
*   **Payload (JSON):**
    ```json
    {
      "document_type": "Certificate of Indigency",
      "urgency_tag": "URGENT"
    }
    ```
*   **Response (201 Created):**
    ```json
    {
      "request_id": 13,
      "document_type": "Certificate of Indigency",
      "status": "PENDING",
      "urgency_tag": "URGENT"
    }
    ```

#### PATCH `/api/v1/documents/<id>/validate/`
*   **Description:** Validate, approve, reject, or release a request (Admin only). Triggers notification to resident.
*   **Payload (JSON):**
    ```json
    {
      "status": "APPROVED",
      "admin_notes": "Please pick up this document on Friday."
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "request_id": 13,
      "status": "APPROVED",
      "admin_notes": "Please pick up this document on Friday."
    }
    ```

---

### 2.5 Issue Reports Module

#### POST `/api/v1/reports/submit/`
*   **Description:** Submit an issue report with image data (`multipart/form-data` payload format).
*   **Payload (Multipart Form):**
    *   `title` (text)
    *   `description` (text)
    *   `location` (text)
    *   `image_attachment` (binary file)
*   **Response (201 Created):**
    ```json
    {
      "report_id": 98,
      "title": "Broken Streetlight Main Road",
      "status": "PENDING",
      "image_url": "https://res.cloudinary.com/gridy/image/upload/v1234/report_98.jpg"
    }
    ```
