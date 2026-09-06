# 12 Agile Sprint Roadmap (Capstone 2)

## 1. Iterative Development Cycle
Following the Agile Scrum methodology, system engineering progressed across discrete two-week sprints:

*   **Sprint 1: Architecture & Auth Base:** Initialize Git repositories, configure PostgreSQL, Django REST Framework, JWT authentication, and user profile models.
*   **Sprint 2: Core API & Admin Dashboard:** Construct React UI skeleton. Develop Django models/APIs for Announcements, Schedules, and service categories.
*   **Sprint 3: Mobile App Base:** Initialize Flutter mobile client. Implement resident authentication, bulletin viewing, and digital document application forms.
*   **Sprint 4: Media & Issue Reporting:** Integrate mobile camera capture. Configure Cloudinary storage pipeline in Django. Implement end-to-end incident reporting with geo-tagging.
*   **Sprint 5: Queueing & Real-Time Sync:** Construct React Live Queue dashboard. Implement mobile QR ticket generation and WebSocket queue broadcasts.
*   **Sprint 6: Notification Infrastructure:** Integrate Firebase Cloud Messaging (FCM) for background alerts, emergency hotlines directory, and initial deployment readiness.
*   **Sprint 7: Citizen Desktop Web Portal:** Build responsive desktop citizen portal (`CitizenLayout`) supporting self-service clearance applications, web incident reporting, live queue tracking, and secret dual-portal role switching (`Shift + \`).
*   **Sprint 8: Real-World Clearance Operations & Treasury Auditing:** Implement hybrid walk-in clearance model with nullable user foreign key, Official Receipt (O.R.) fee auditing on legal PDF certificates, executive revenue KPIs, and bulk RBI census CSV import.
*   **Sprint 9: Multi-Tenant Hardening & System Observability:** Eliminate cross-tenant action leaks in queue workflows, establish structured health monitoring (`/api/health/`), and document system baselines in Architecture Decision Records (ADRs 001–008).