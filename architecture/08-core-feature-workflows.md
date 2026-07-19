# 08 Core Feature Workflows

## 1. Hybrid Queue Monitoring Workflow
This workflow coordinates physical ticketing at the barangay hall with digital, real-time status updates on the resident's mobile application.

```mermaid
sequenceDiagram
    autonumber
    actor Resident
    actor Admin
    participant Flutter as Flutter Mobile App
    participant Django as Django DRF Backend
    participant DB as PostgreSQL Database
    participant FCM as Firebase Cloud Messaging

    Note over Resident, Django: Step 1: Resident gets physical slip at Hall (e.g., A-125)
    Resident->>Flutter: Open QR Scanner & Scan physical slip
    Flutter->>Django: POST /api/v1/queue/ticket/ { "ticket_number": "A-125" }
    Django->>DB: Save ticket link to Resident Profile
    Django-->>Flutter: 201 Created (linked successfully)
    
    loop Real-Time Polling
        Flutter->>Django: GET /api/v1/queue/live-status/
        Django->>DB: Fetch current serving ticket
        DB-->>Django: Current ticket is A-124
        Django-->>Flutter: Return live-status (waiting...)
    end
    
    Admin->>Django: POST /api/v1/queue/next/ (Advance queue)
    Django->>DB: Update A-125 status to "ONGOING"
    Django->>FCM: Trigger push notification payload
    FCM->>Flutter: Push Notification: "Please proceed to Counter 1"
    Flutter->>Resident: Display notification alert & update screen
```

---

## 2. Image-Backed Issue Reporting Workflow
This workflow manages camera capture, local device image compression, streaming to the backend, and hosting media in cloud storage.

```mermaid
sequenceDiagram
    autonumber
    actor Resident
    actor Admin
    participant Flutter as Flutter Mobile App
    participant Django as Django DRF Backend
    participant Cloudinary as Cloudinary CDN
    participant DB as PostgreSQL Database
    participant React as React Admin Dashboard

    Resident->>Flutter: Capture photo of local issue
    Flutter->>Flutter: Compress image to < 2MB limit
    Flutter->>Django: POST /api/v1/reports/submit/ (multipart/form-data)
    Django->>Cloudinary: Stream binary upload
    Cloudinary-->>Django: Return secure asset URL
    Django->>DB: Insert issue report (title, description, image_url)
    DB-->>Django: Confirm save
    Django-->>Flutter: 201 Created
    
    Admin->>React: Open reports tab
    React->>Django: GET /api/v1/reports/
    Django->>DB: Fetch active reports
    DB-->>Django: Return reports list
    Django-->>React: Return JSON (with Cloudinary image_url)
    React-->>Admin: Render report details with image preview
```
