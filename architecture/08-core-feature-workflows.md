# 08 Core Feature Workflows
## 1. Hybrid Queue Monitoring Workflow
1.  **Generation:** Resident receives a physical queue slip (e.g., A-125) at the barangay hall [cite: 8].
2.  **Digitization:** Resident opens the Flutter app and scans the slip's QR code [cite: 8, 11].
3.  **Polling/WebSockets:** Flutter app begins listening to the `/api/v1/queue/live-status/` endpoint for updates [cite: 8].
4.  **Advancement:** Admin clicks "Next Queue" on the React dashboard [cite: 8].
5.  **Notification:** Django updates the database, shifting A-125 to "Ongoing", and fires an FCM notification to the resident: "Please proceed to Counter 1" [cite: 8].

## 2. Image-Backed Issue Reporting Workflow
1.  **Capture:** Resident uses Flutter app to take a photo of a barangay issue [cite: 8, 11].
2.  **Submission:** Flutter compresses the image (e.g., max 2MB) and sends it as `multipart/form-data` [cite: 8].
3.  **Storage:** Django receives the request, uploads the image to Cloudinary, and saves the text data + image URL to PostgreSQL [cite: 8].
4.  **Dashboard Alert:** The React dashboard updates its analytics, displaying the new report and rendering the image via the Cloudinary URL [cite: 8].
