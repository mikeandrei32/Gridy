# 06 API Endpoint Contracts
## 1. RESTful Design
All endpoints enforce JWT Bearer token authorization [cite: 9].

## 2. Key Endpoints
*   **POST `/api/v1/auth/login/`**
    *   *Payload:* `{ "username": "...", "password": "..." }`
    *   *Response:* `{ "access": "...", "refresh": "...", "role": "ADMIN" }` [cite: 9].
*   **GET `/api/v1/queue/live-status/?category=clearance`**
    *   *Response:* `{ "current_ticket": "A-124", "total_waiting": 18, "avg_wait_mins": 12 }` [cite: 9].
*   **POST `/api/v1/reports/submit/` (Content-Type: multipart/form-data)**
    *   *Payload:* `title`, `description`, `location`, `image_attachment` (File) [cite: 9].
    *   *Response:* `201 Created`, `{ "reference_id": "BRGY-2026", "image_url": "https://res.cloudinary.com/..." }` [cite: 9].
*   **PATCH `/api/v1/documents/<id>/validate/`**
    *   *Payload:* `{ "status": "APPROVED", "admin_notes": "..." }`
    *   *Response:* `200 OK` (Triggers backend notification service) [cite: 9].
