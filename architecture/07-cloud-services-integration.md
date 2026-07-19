# 07 Cloud Services & Third-Party Integrations
## 1. Media Storage: Cloudinary
*   **Implementation:** Django uses the `cloudinary` and `dj3-cloudinary-storage` packages. When a resident submits an issue report with an image, Django streams the file directly to Cloudinary via their API, receives a secure URL in response, and stores *only the URL* in the PostgreSQL database [cite: 4, 12]. This prevents database bloat.

## 2. Push Notifications: Firebase Cloud Messaging (FCM)
*   **Implementation:** The Flutter app initializes FCM on startup to retrieve a device token. This token is saved to the user's profile in Django. When an Admin updates a document status or advances the queue, Django uses the `firebase-admin` Python SDK to send a push payload directly to the resident's specific device token [cite: 4, 12].
