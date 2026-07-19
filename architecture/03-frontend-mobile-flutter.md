# 03 Frontend Mobile Implementation (Flutter)

## 1. Technology Stack
*   **Core:** Flutter SDK (Dart) for natively compiled, cross-platform performance.
*   **State Management:** **BLoC (Business Logic Component)** to separate the UI presentation layer from repositories and network requests.
*   **Networking:** `Dio` client configured with interceptors for token auto-injection.
*   **Hardware / Plugins:** 
    *   `image_picker` & `flutter_image_compress` for capturing and optimizing upload images.
    *   `mobile_scanner` (or `qr_code_scanner`) for physical ticket validation.
    *   `firebase_messaging` & `flutter_local_notifications` for real-time FCM alert overlays.

---

## 2. Directory Architecture (Clean Architecture)
The Flutter mobile application code is organized as follows:
```text
lib/
├── main.dart               # App entry point, initializes Firebase & app theme
├── blocs/                  # BLoC state managers (e.g., auth_bloc, queue_bloc, report_bloc)
├── models/                 # Data entities (e.g., resident_profile.dart, queue_ticket.dart)
├── repositories/           # Abstract and concrete API repositories (e.g., api_repository.dart)
├── services/               # Device-level services (FCM listener setup, HTTP clients)
└── views/
    ├── screens/            # Full-page widgets (LoginScreen, HomeScreen, IssueReportScreen)
    └── widgets/            # Custom reusable buttons, input fields, queue ticket cards
```

---

## 3. Core Mobile Workflows

### 3.1 BLoC State Management Pattern
For queue tracking, the BLoC pattern orchestrates flow:
*   **Events:** `StartQueueTracking(String ticketNum)`, `RefreshQueueStatus()`, `StopQueueTracking()`
*   **States:** `QueueTrackerInitial`, `QueueTrackerLoading`, `QueueTrackerActive(QueueStatus)`, `QueueTrackerError(String message)`

When a user scans a ticket QR code, `StartQueueTracking` is dispatched. The BLoC switches to `QueueTrackerLoading`, calls the repository, transitions to `QueueTrackerActive` on success, and schedules a periodic periodic refresh timer.

### 3.2 Image-Backed Issue Submission (Compression)
To handle slow mobile uploads and database boundaries, the `IssueReportScreen` compresses images locally before they hit the Django REST endpoint.
*   **Capture:** Resident takes a high-res image (often 5MB to 12MB).
*   **Compression:** The app reads the file, utilizes `flutter_image_compress` to compress it down to a target file size **< 2MB** and quality of **80%**, converting it to JPEG.
*   **Multipart Upload:** The compressed file is loaded into a `MultipartFile` and sent via Dio.

### 3.3 FCM Push Notification Interception
FCM handles background notifications natively. For foreground application states (when the resident is actively looking at the app), we configure a listener:
```dart
FirebaseMessaging.onMessage.listen((RemoteMessage message) {
  // Extract notification details
  String title = message.notification?.title ?? "Queue Alert";
  String body = message.notification?.body ?? "";
  
  // Show foreground heads-up overlay banner via flutter_local_notifications
  LocalNotificationService.displayNotification(title, body);
});
```

---

## 4. Screens & View Interfaces
*   **Announcement Feed:** A stream-built card interface showing chronological barangay announcements with filter categories.
*   **Document Request Form:** Interactive dropdown fields selecting document types, with an urgency toggle.
*   **Queue Status Tracker:** Displays a digital ticket model showing the number of people waiting ahead of the resident, powered by the BLoC state.
*   **Issue Reporting Wizard:** Step-by-step form with map location pins and camera previews.
