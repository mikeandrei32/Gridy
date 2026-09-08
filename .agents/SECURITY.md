# Gridy - Data Privacy & Security Policy

This document defines the mandatory data protection protocols, security baselines, and architectural access boundaries enforced across Gridy.

---

## 1. Compliance with Republic Act No. 10173 (Data Privacy Act of 2012)

Barangay operations handle highly sensitive Personally Identifiable Information (PII) including resident full names, government ID numbers, birthdates, civil statuses, monthly household incomes, and exact home addresses.

### Core Data Privacy Principles Enforced in Gridy
1. **Transparency & Consent:** Resident personal data collected through census imports (RBI) or digital registration is processed strictly for official barangay certification and frontline governance.
2. **Purpose Limitation:** Resident demographic data collected for document clearances (e.g. Certificate of Indigency) cannot be repurposed or exposed across unrelated modules.
3. **Data Proportionality & Minimization:** API endpoints must return only the fields required for the active screen. Sensitive fields like `password`, internal salt, and raw session tokens are excluded from all serializer output schemas.
4. **Sanitized Error Responses:** Views must never expose raw database exceptions, SQL queries, or internal stack traces in client responses.

---

## 2. Four-Tier Role-Based Access Control (RBAC) Hierarchy

The system defines four distinct user authorization tiers:

| Tier | Role | Scope & Permissions | Gated Restrictions |
| :--- | :--- | :--- | :--- |
| **Tier 1** | `DILG_ADMIN` | Macro-level multi-tenant supervision; cross-barangay auditing. | Cannot modify local barangay operational tickets. |
| **Tier 2** | `ADMIN` | Full tenant authority (Punong Barangay, Secretary, Treasurer). Document approval, queue advancement, treasury fee collection. | Scoped strictly to `request.user.barangay`. Cannot access other barangays. |
| **Tier 3** | `FIELD_OFFICIAL` | Field operations (Barangay Tanods). Physical ticket advancement, clearance anti-forgery validation, incident inspection. | **Strictly blocked** from creating resident document requests, filing resident tickets, or approving clearances. |
| **Tier 4** | `RESIDENT` | Citizen self-service portal. Requisitioning clearances, monitoring tickets, reporting community incidents. | Requires verified status (`is_verified=True`) for official clearances. Scoped strictly to own records. |

---

## 3. Multi-Tenant Queryset Isolation Protocol

To prevent horizontal privilege escalation and cross-barangay data leaks:

1. **Mandatory Queryset Overrides:** Every DRF `ModelViewSet` must override `get_queryset()`:
   ```python
   def get_queryset(self):
       user = self.request.user
       if not user or not user.is_authenticated:
           return Model.objects.none()
       if user.role == User.Role.DILG_ADMIN:
           return Model.objects.all().order_by('-created_at')
       if user.role in [User.Role.ADMIN, User.Role.FIELD_OFFICIAL]:
           return Model.objects.filter(barangay=user.barangay).order_by('-created_at')
       return Model.objects.filter(user=user).order_by('-created_at')
   ```
2. **Tenant Parameter Injection:** Desk actions (e.g., walk-in clearance creation, ticket generation) must bind directly to `request.user.barangay`, never trusting client-supplied barangay IDs.

---

## 4. Creation-State Parameter Overrides

Clients must never be able to elevate privilege or pre-approve records during submission:
* Intercept parameters in ViewSet `perform_create()`:
  * Force `status = PENDING`.
  * Strip administrative notes, approval flags, and assigned personnel.
  * Force applicant binding: `user = self.request.user` (or explicit walk-in flags if created by an authorized official).

---

## 5. Session Security & Boundary Handling

1. **Short-Lived Access Tokens:** JWT access tokens expire in 15 minutes.
2. **HttpOnly Rotating Refresh Cookies:** Refresh tokens must reside within server-backed `HttpOnly; SameSite=Lax` cookies, protected from JavaScript XSS attacks.
3. **Token Rotation:** Every token refresh cycle revokes the prior refresh token and issues a new cryptographic pair to prevent replay attacks.
4. **Graceful Logout Invalidation:** Session cookies are cleared safely upon sign-out without throwing 400 Bad Request if the cookie was already absent.

---

## 6. Dual-Portal UI Segregation (Physical & Visual Security)

To prevent unauthorized tampering when residents or officials use communal devices and public barangay kiosks:
* **Citizen Portal by Default:** Web and mobile applications launch into Citizen Resident mode by default.
* **Hidden Authority Barriers:** Switching to Barangay Authority Command requires deliberate administrative action:
  * **Web Portal:** Hidden `Shift + \` key combination.
  * **Mobile Client:** Haptic-verified long-press gesture on the `GridyLogo` icon.
* **Role Verification Gates:** Official credentials attempting login through the resident portal are rejected, and vice-versa.

---

## 7. Audit Trails & Non-Repudiation

Every administrative action—including clearance approval, status change, fee assessment, O.R. recording, and census import—generates an immutable record in `gridy_audit.AuditLog` capturing:
* User ID & role
* Timestamp
* Target object & action type
* Client IP address and User-Agent
