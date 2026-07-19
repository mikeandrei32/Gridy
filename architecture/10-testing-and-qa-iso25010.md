# 10 Testing Protocols & Quality Assurance

## 1. QA Methodology: Black-Box Testing
The system is subjected to strict functional validation via Black-Box Testing. Developers and QA evaluators verify system outputs based on inputs without inspecting internal logic. 

Test cases are written using the following structured template:

| Test ID | Feature Area | User Story | Test Steps | Expected Output | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Queue Sync | As a resident, I want to scan a physical ticket QR code to track my queue live on my phone. | 1. Open QR scanner in Flutter.<br>2. Focus camera on ticket QR.<br>3. Scanner reads code and POSTs. | Flutter app redirects to live tracker screen displaying waiting status. | *[Pending]* |
| **TC-02** | Issue Upload | As a resident, I want to submit a report with a camera photo. | 1. Select Camera attachment.<br>2. Snap photo (e.g. 5MB file).<br>3. Verify compression occurs.<br>4. Tap submit. | App compresses file to <2MB. Django streams to Cloudinary and saves URL in PostgreSQL. | *[Pending]* |

---

## 2. ISO/IEC 25010 Quality Evaluation
The Gridy system is evaluated under three specific quality characteristics of the ISO/IEC 25010 model:

### 2.1 Functional Suitability
Evaluates whether the software functions meet stated goals.
*   *Validation Metric:* Verify that every core feature (Announcements, Hybrid Queue, Issue reports, Document requests, Notifications) successfully processes requests under standard loads without throwing 500 Server Errors.

### 2.2 Usability
Evaluates how easy, intuitive, and learnable the web and mobile interfaces are.
*   *Validation Metric:* Administered via a **5-point Likert Scale survey** distributed to a minimum of **50 target respondents** (both residents and barangay officials) located at the primary study sites (Barangay Ibabang Dupay, Lucena City; Barangay Daungan, Pagbilao, Quezon).
*   *Calculation:* The results are interpreted using the weighted mean of responses across four sub-characteristics:
    1.  *Learnability:* Easy to understand for first-time or older users.
    2.  *Operability:* Navigation is simple and text is clear.
    3.  *User Interface Aesthetics:* Colors and layouts are visually appealing.
    4.  *Accessibility:* Adaptable across web screens and mobile devices.

### 2.3 Reliability
Evaluates the system's capacity to maintain performance levels and avoid system crashes.
*   *Validation Metric:* Concurrent document requests and queue ticket registration API calls are executed to ensure database connection pooling and thread handling function stably without service interruption.

---

## 3. Manual Testing Validation Steps
*   **Validation of Document State Transition:** Admin processes request status updates on React $\rightarrow$ State switches from `PENDING` to `APPROVED` or `REJECTED` $\rightarrow$ Webhook/notification service triggers FCM callback $\rightarrow$ Resident app screen updates automatically without manual app refresh.
