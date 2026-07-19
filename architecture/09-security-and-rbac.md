# 09 Security & Role-Based Access Control (RBAC)
## 1. Authentication mechanism
*   Utilizes **JSON Web Tokens (JWT)** via `djangorestframework-simplejwt` [cite: 4, 6].
*   Access tokens have a short lifespan (e.g., 15 minutes), requiring silent refresh via Refresh tokens to minimize risk of token theft [cite: 6].

## 2. Authorization (RBAC) implementation
*   **Django Level:** Custom permission classes (e.g., `IsBarangayOfficial`) are applied to sensitive views. For instance, `PATCH /api/v1/queue/advance/` will return a `403 Forbidden` if a resident's token attempts to access it [cite: 6].
*   **React Level:** Route guarding prevents residents from accessing the Admin Dashboard URLs.
*   **Flutter Level:** The UI dynamically renders the "Official Dashboard" button only if the decoded JWT contains `"role": "ADMIN"` [cite: 11].

## 3. Data Privacy
*   All traffic is encrypted over HTTPS.
*   Sensitive resident data (birthdates, exact addresses) are shielded behind authentication walls and only accessible to authorized officials [cite: 6].
