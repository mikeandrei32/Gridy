# 02 Frontend Web Implementation (ReactJS)

## 1. Technology Stack
*   **Core:** ReactJS (Vite) for modern, fast HMR tooling.
*   **State Management:** **Zustand** for lightweight global store management (e.g., active queue status, dashboard analytics).
*   **Styling:** Tailwind CSS for design system token enforcement.
*   **API Client:** Axios with dynamic request/response interceptors.
*   **Querying/Polling:** TanStack Query (`@tanstack/react-query`) with SWR capabilities for interval-based status fetching.

---

## 2. Directory & Directory Architecture
The React codebase conforms to a modular layout:
```text
src/
├── assets/             # Global image assets and CSS themes
├── components/
│   ├── common/         # Reusable inputs, buttons, tables
│   ├── layout/         # Sidebar, Navbar, and admin shell
│   ├── queue/          # Active tickets list and queue control widgets
│   └── documents/      # Request logs and document validation modals
├── hooks/              # Custom React hooks (e.g., useQueuePolling)
├── services/           # Axios instance configuration and API request definitions
├── store/              # Zustand global state declarations (authStore, queueStore)
└── views/              # Pages (Login, Dashboard, Documents, Reports)
```

---

## 3. Core Frontend Workflows

### 3.1 Silent Token Refresh Interceptor
To maintain the login session without frustrating officials, Axios implements a response interceptor. When an API call fails with a `401 Unauthorized` status code, the interceptor intercepts the error, fires a call to `/api/v1/auth/token/refresh/`, updates the access token, and retries the original request.

```javascript
// Example interceptor logic structure
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const newAccessToken = await refreshAuthToken(); // POSTs to auth/token/refresh/
      axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
      return axiosInstance(originalRequest);
    }
    return Promise.reject(error);
  }
);
```

### 3.2 Real-time Dashboard Polling
The React dashboard monitors active queue ticket statuses using TanStack Query. It triggers a query to `/api/v1/queue/live-status/` every 5 seconds (`refetchInterval: 5000`) to guarantee that counters update dynamically when the mobile app registers new slips.

---

## 4. Key Component Modules
*   **Dashboard Module:** Displays high-level counters (registered residents, active pending reports) and aggregates incoming urgent flags.
*   **Queue Management View:** Displays the waitlist queue table, priority tags, and triggers the `POST /api/v1/queue/next/` call.
*   **Document Processing View:** Displays pending documents with a filterable tabular interface, offering a validation popup modal to input validation remarks.
*   **Schedule & Announcements View:** Admin form interface to compose announcements and trigger schedule calendars.
