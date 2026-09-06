# 02 Frontend Web Implementation (ReactJS & TypeScript)

## 1. Technology Stack
*   **Core:** React 19 with TypeScript, bundled using **Vite** for rapid hot module replacement.
*   **Styling:** Tailwind CSS with utility-first responsive tokens and full dark/light theme switching.
*   **State & Authentication:** React Context (`AuthContext`, `ThemeContext`) with HTTP cookie session sync.
*   **API Client:** Axios instance with automated Bearer authorization headers and centralized error dispatch.
*   **Icons & Motion:** Lucide React icons with smooth micro-animations.

---

## 2. Directory Architecture
The frontend follows a domain-driven, role-segregated layout:

```text
frontend/src/
├── components/
│   ├── citizen/             # Citizen portal components (CitizenLayout, navbars)
│   ├── common/              # Universal UI (buttons, badges, inputs, skeleton loaders)
│   ├── documents/           # Clearance tables, validation modal, walk-in creation
│   ├── issues/              # Incident reporting cards, triage badges
│   ├── layout/              # Admin shell (Sidebar, Navbar, MobileDrawer)
│   └── queue/               # Queue ticket displays and counter widgets
├── context/                 # AuthContext, ThemeContext
├── pages/
│   ├── admin/               # Executive Desk views (Dashboard, Queue, Documents, Reports)
│   ├── citizen/             # Citizen Self-Service views (Documents, Queue, Bulletin, Issues)
│   └── community/           # Residents directory, RBI census CSV import
├── routes/                  # ProtectedRoute, AppRoutes, role gatekeepers
└── services/                # Axios API service integrations

```

---

## 3. Dual-Portal Architectural Pattern

Per **ADR 008**, the application separates public constituent self-service from executive LGU administration:

### 3.1 Citizen Self-Service Desktop Portal (`/portal/*`)
Mounted under `CitizenLayout`, providing a distraction-free, resident-first experience:
*   **`/portal/documents` (`CitizenDocuments.tsx`):** Self-service clearance applications with instant status tracking and downloadable legal PDF slips.
*   **`/portal/queue` (`CitizenQueue.tsx`):** Live queue ticket tracker showing active serving numbers and average wait times.
*   **`/portal/bulletin` (`CitizenBulletin.tsx`):** Community announcements feed and scheduled events calendar.
*   **`/portal/issues` (`CitizenIssues.tsx`):** Public incident reporting with client-side image attachment and geo-location notes.

### 3.2 Executive Desk Portal (`/admin/*`)
Mounted under `AdminLayout`, guarded by `ProtectedRoute` requiring `ADMIN` or `DILG_ADMIN` roles:
*   **`/admin/dashboard` (`Dashboard.tsx`):** Executive overview with gross clearance revenue collection, resident demographics, and incident scenario charts.
*   **`/admin/documents` (`DocumentsManagement.tsx`):** Clearance triage, treasury O.R. fee assignment, and walk-in legal issuance.
*   **`/admin/residents` (`ResidentsManagement.tsx`):** Registry of Barangay Inhabitants directory with bulk RBI CSV import modal and template download.
*   **`/admin/queue`, `/admin/reports`, `/admin/hotlines`, `/admin/settings`.

### 3.3 Secret Demarcation Gateway (`Shift + \`)
To allow evaluators and developers to switch between citizen and official views without disrupting presentation flow, pressing `Shift + \` triggers a hidden modal. The gateway verifies session permissions before permitting navigation into administrative routes.

---

## 4. Key Operational Components

### 4.1 Treasury Auditing in ReviewDocumentModal
Officials process clearances via `ReviewDocumentModal.tsx`. Prior to transitioning a document to `RELEASED`, the modal requires input of the **Official Receipt (O.R.) Number** and **Fee Amount in PHP**, directly embedding them into the database and server-side PDF generator.

### 4.2 Bulk RBI Census CSV Import
Located in `ResidentsManagement.tsx`, this component accepts local registry CSV files, performs client-side header validation, provides a downloadable template (`residents_template.csv`), and transmits records to `/api/v1/auth/import-residents/`.