# Capstone Defense & Technical Evaluation Playbook

**Project:** Gridy (Barangay Information and Service Management System)  
**Document Purpose:** Presentation script, live demonstration flow, and panel technical defense strategy.

---

## 1. Live Demonstration Script & Flow

To demonstrate the full breadth of Gridy without confusing the panel, structure your live demonstration into three distinct acts:


### Act 1: The Citizen Self-Service Experience
1. **Landing & Identity:** Open the browser at `/login`. Highlight the resident-first experience. Log in as a resident (e.g., `mariasantos`).
2. **Clearance Request:** Navigate to **Documents** (`/portal/documents`). Submit a new request for a *Barangay Clearance* for "Local Employment". Show the instant `PENDING` badge.
3. **Live Queue Slip:** Navigate to **Queue** (`/portal/queue`). Generate a remote queue ticket. Point out the live serving number and estimated wait calculation.
4. **Community Incident Reporting:** Navigate to **Report Incident** (`/portal/issues`). Attach an image showing a fallen electrical wire or broken streetlight. Submit the report.

### Act 2: Transition to Executive Desk via Demarcation Shortcut
1. **Secret Trigger:** Press `Shift + \` on your keyboard.
2. **Key Talking Point to Panel:** *"Notice that our public portal completely cloaks administrative interfaces to protect against brute-force attacks and reduce constituent cognitive load. However, for authorized personnel, our demarcation gateway validates administrative claims."*
3. **Command Dashboard Overview:** Enter the Executive Desk (`/admin/dashboard`). Showcase the 4 top metrics:
   - Total Registered Residents
   - Pending Requests
   - Active Incident Reports
   - **Clearance Collections (PHP)**
4. **Document Triage & Treasury Verification:** Navigate to **Documents** (`/admin/documents`). Select Maria Santos's pending request. Enter the Official Receipt Number (`OR-2026-001`) and Fee (`50.00`). Click **Release**.
5. **Legal PDF Certificate:** Open the generated PDF certificate. Point out the official barangay header, QR control ID, and the **Official Assessment & Treasury Slip** box.

### Act 3: Physical Walk-in Constituent & RBI Census Import
1. **Walk-in Handling:** While still in Document Management, click **Record Walk-in**. Enter "Pedro Penduko", named Purok "Purok 3", and fee "50.00".
2. **Talking Point:** *"In real Philippine barangays, senior citizens and underprivileged constituents visit the hall in person. Gridy accommodates them through our Hybrid Nullable Tenant model without creating phantom database accounts."*
3. **Bulk Census Digestion:** Navigate to **Residents Directory** (`/admin/residents`). Click **Import RBI CSV**. Demonstrate uploading an official census spreadsheet. Show how all 28 residents are auto-assigned to the official's barangay and pre-verified.

---

## 2. Technical Defense & Panel QA Playbook

Anticipate these common panel questions with our pre-architected justifications:

### Question 1: "How do you comply with the Data Privacy Act of 2012 (RA 10173) in a multi-tenant environment?"
* **Answer:** *"All data access is horizontally partitioned by tenant ID at the database query layer per ADR 004. Viewsets override `get_queryset()` to enforce `request.user.barangay`. Cross-tenant querying is physically prevented in SQL. Furthermore, PII is protected via HttpOnly, SameSite=Lax JWT cookie sessions per ADR 002, completely immune to XSS token theft."*

### Question 2: "How does the system prevent financial fraud or unrecorded fee collections?"
* **Answer:** *"Per ADR 007 and Commission on Audit (COA) guidelines, certificates cannot be transitioned to `RELEASED` without an official serialized Official Receipt (O.R.) Number and Fee amount. The server embeds this assessment slip directly into the PDF certificate and aggregates total revenue using Django ORM database-level sums (`Sum('fee_amount')`), creating a tamper-evident audit trail between physical treasury receipt booklets and digital clearance releases."*

### Question 3: "What happens if an ordinary resident discovers the `/admin` URL or tries pressing `Shift + \`?"
* **Answer:** *"The React application enforces role-based barriers using `ProtectedRoute`. Even if a resident triggers `Shift + \`, the gateway evaluates the decoded JWT claims. If the user does not possess `ADMIN` or `DILG_ADMIN` roles, access is rejected. On the backend, every administrative ViewSet overrides `get_permissions()` using `IsBarangayOfficial`, returning a `403 Forbidden` regardless of client-side tampering."*

---

## 3. Live Demo Fallback Checklist
- [ ] Database seeded with realistic names, Purok labels, and hotlines.
- [ ] Admin user credential verified (`admin@example.com`).
- [ ] Sample resident credential verified (`mariasantos`).
- [ ] Downloadable `residents_template.csv` verified in local directory for the CSV upload demonstration.