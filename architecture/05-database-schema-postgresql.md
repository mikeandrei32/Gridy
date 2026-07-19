# 05 Database Schema (PostgreSQL)
## 1. RDBMS Strategy
PostgreSQL is utilized for its robust relational data integrity and support for complex queries [cite: 4, 10].

## 2. Detailed Table Implementation
*   **`users_user`**: `id` (PK), `username`, `password`, `role` (Choices: ADMIN, RESIDENT).
*   **`residents_resident`**: `resident_id` (PK), `user_id` (FK -> users_user), `full_name`, `birth_date`, `voter_status`, `contact_number` [cite: 10].
*   **`communications_announcement`**: `id` (PK), `title`, `category` (Choices: AID, MEDICAL, EVENT, GENERAL), `content`, `scheduled_date` [cite: 10].
*   **`services_queue`**: `ticket_id` (PK), `resident_id` (FK, nullable), `service_type`, `priority` (REGULAR, SENIOR/PWD), `status` (WAITING, SERVED), `created_at` [cite: 10].
*   **`reports_issue`**: `report_id` (PK), `resident_id` (FK), `title`, `description`, `location`, `image_url` (VARCHAR, storing Cloudinary link), `status` (PENDING, RESOLVED) [cite: 10].
*   **`services_documentrequest`**: `request_id` (PK), `resident_id` (FK), `document_type`, `status`, `urgency_tag` [cite: 10].
