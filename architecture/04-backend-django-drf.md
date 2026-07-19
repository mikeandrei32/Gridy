# 04 Backend Architecture (Django DRF)
## 1. Core Framework
*   **Backend:** Django coupled with Django REST Framework (DRF) acts as the API Gateway [cite: 4, 12].

## 2. Modular App Implementation
*   `gridy_auth`: Custom User model extending `AbstractUser`. Handles JWT authentication and Role-Based Access Control (RBAC) [cite: 12].
*   `gridy_services`: Contains logic for Document Requests (CRUD, urgency tagging, status updates) and Live Queue Management (advancing queues, tracking wait times) [cite: 12].
*   `gridy_reports`: Manages the Issue Reporting pipeline. Responsible for receiving `multipart/form-data`, validating image extensions, and passing the file to the cloud storage provider [cite: 12].
*   `gridy_communications`: Handles Schedule events and Announcements, utilizing dynamic service categorization (e.g., separating human vaccination programs from standard events) [cite: 12].
