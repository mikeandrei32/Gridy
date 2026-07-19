# 03 Frontend Mobile Implementation (Flutter)
## 1. Technology Stack
*   **Core:** Flutter (Dart) for natively compiled cross-platform apps [cite: 4, 11].
*   **State Management:** BLoC (Business Logic Component) for separating presentation from API logic.
*   **Hardware Packages:** `camera` or `image_picker` for issue attachments, `qr_code_scanner` for queue slips [cite: 11].

## 2. UI/UX Workflows
*   **Resident Issue Reporting:** Implements a multi-step form where residents can type descriptions, select geographic context, and use the device camera to attach evidence images of barangay issues (e.g., broken streetlights) [cite: 2, 11].
*   **Hybrid Queue Scanning:** Integrates a barcode/QR scanner. Residents scan their physical slip, triggering an API call that subscribes them to live status updates on their screen [cite: 11].
*   **Official Mobile View:** A role-based toggle enabling barangay officials to access a simplified dashboard for urgent monitoring and quick status updates while in the field [cite: 11].
