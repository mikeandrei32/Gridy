# 05 Database Schema (PostgreSQL)

## 1. RDBMS Strategy
PostgreSQL serves as the enterprise relational database to enforce strict referential integrity through foreign keys, check constraints, unique indexes, and multi-tenant partitioning by `barangay_id`. Composite database indexes are configured across high-velocity transactional tables (`status`, `created_at`, and `barangay_id`) to optimize real-time polling and analytical aggregations.

---

## 2. Table Schemas

### 2.1 Table: `auth_barangay`
Anchors multi-tenant jurisdiction and official identity assets for each Local Government Unit.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | PRIMARY KEY | Unique Barangay ID |
| `name` | `VARCHAR(255)` | UNIQUE, NOT NULL | Official Barangay Name (e.g., 'Barangay Guadalupe') |
| `logo` | `VARCHAR(100)` | NULL | Barangay crest/seal image path |
| `city_seal` | `VARCHAR(100)` | NULL | Municipal/City seal image path |
| `captain_name` | `VARCHAR(255)` | NULL | Incumbent Punong Barangay (Barangay Captain) |
| `office_contact` | `VARCHAR(255)` | NULL | Official office contact information |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW(), NOT NULL | Registration timestamp |

---

### 2.2 Table: `auth_user`
Extends Django's `AbstractUser` to support role-based multi-tenant user accounts.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | PRIMARY KEY | Unique user account ID |
| `username` | `VARCHAR(150)` | UNIQUE, NOT NULL | Unique login identifier |
| `email` | `VARCHAR(254)` | NOT NULL | User contact and notification address |
| `password` | `VARCHAR(128)` | NOT NULL | PBKDF2 with SHA-256 hashed password |
| `role` | `VARCHAR(50)` | NOT NULL | `'ADMIN'`, `'RESIDENT'`, `'DILG_ADMIN'`, or `'FIELD_OFFICIAL'` |
| `barangay_id` | `INTEGER` | FK (`auth_barangay`), NULL, ON DELETE CASCADE | Multi-tenant assignment (null for DILG Admins) |
| `email_alerts` | `BOOLEAN` | DEFAULT TRUE, NOT NULL | Daily queue and document email subscription |
| `push_alerts` | `BOOLEAN` | DEFAULT FALSE, NOT NULL | Real-time Firebase FCM notification subscription |
| `is_active` | `BOOLEAN` | DEFAULT TRUE, NOT NULL | Account active flag |

---

### 2.3 Table: `auth_resident`
Stores identity details and residential verification records for registered constituents.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | PRIMARY KEY | Unique profile ID |
| `user_id` | `INTEGER` | UNIQUE, FK (`auth_user`), ON DELETE CASCADE | Associated user account |
| `full_name` | `VARCHAR(255)` | NOT NULL | Legal full name |
| `birth_date` | `DATE` | NOT NULL | Date of birth (used for youth/senior demographic calculations) |
| `voter_status` | `BOOLEAN` | DEFAULT FALSE, NOT NULL | Registered voter flag |
| `contact_number` | `VARCHAR(20)` | NULL | Phone or mobile number |
| `purok` | `VARCHAR(100)` | NULL | Named Purok or Zone of residence |
| `is_verified` | `BOOLEAN` | DEFAULT FALSE, NOT NULL | Official identity and residency verification barrier |
| `guardian_id` | `INTEGER` | FK (`auth_resident`), NULL, ON DELETE SET NULL | Guardian reference for residents under 18 |

---

### 2.4 Table: `services_documentrequest`
Tracks citizen document applications and walk-in legal clearance issuances.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | PRIMARY KEY | Unique request control ID |
| `user_id` | `INTEGER` | FK (`auth_user`), NULL, ON DELETE CASCADE | Requester account (null for walk-in transactions) |
| `barangay_id` | `INTEGER` | FK (`auth_barangay`), NULL, ON DELETE CASCADE | Tenant anchor (required for walk-in issuances) |
| `is_walkin` | `BOOLEAN` | DEFAULT FALSE, NOT NULL, INDEXED | Walk-in / physical visit indicator |
| `walkin_name` | `VARCHAR(255)` | NULL | Legal name of walk-in citizen |
| `walkin_purok` | `VARCHAR(100)` | NULL | Purok address of walk-in citizen |
| `document_type`| `VARCHAR(100)` | NOT NULL | Type (e.g., 'Barangay Clearance', 'Indigency Certificate') |
| `purpose` | `TEXT` | NULL | Purpose of clearance |
| `urgency_tag` | `VARCHAR(20)` | DEFAULT `'REGULAR'`, NOT NULL | `'REGULAR'` or `'URGENT'` |
| `status` | `VARCHAR(20)` | DEFAULT `'PENDING'`, NOT NULL | `'PENDING'`, `'PROCESSING'`, `'READY_FOR_PICKUP'`, `'RELEASED'`, `'REJECTED'` |
| `admin_notes` | `TEXT` | NULL | Administrative instructions or verification remarks |
| `or_number` | `VARCHAR(50)` | NULL | Official Receipt Number issued by Barangay Treasurer |
| `fee_amount` | `NUMERIC(8,2)` | DEFAULT 0.00, NOT NULL | Statutory clearance fee in PHP |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW(), NOT NULL | Application timestamp |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW(), NOT NULL | Last status update timestamp |

*Indexes: `(user_id, status)`, `(barangay_id, status)`, `(status)`.*

---

### 2.5 Table: `services_queueticket`
Manages hybrid physical and digital queue progression.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | PRIMARY KEY | Unique ticket ID |
| `ticket_number`| `VARCHAR(20)` | NOT NULL | Serialized display ticket (e.g., 'T001') |
| `user_id` | `INTEGER` | FK (`auth_user`), NULL, ON DELETE SET NULL | Digital citizen account (null for walk-in desk tickets) |
| `barangay_id` | `INTEGER` | FK (`auth_barangay`), NULL, ON DELETE CASCADE | Multi-tenant queue boundary |
| `service_type`| `VARCHAR(100)` | NOT NULL | Desk service department (e.g., 'DOCUMENT', 'TREASURY') |
| `walkin_name` | `VARCHAR(255)` | NULL | Name of walk-in visitor |
| `priority_status`| `VARCHAR(20)` | DEFAULT `'regular'`, NOT NULL | `'regular'` or `'priority'` (Senior/PWD/Pregnant) |
| `is_priority` | `BOOLEAN` | DEFAULT FALSE, NOT NULL | Fast-track queue priority flag |
| `notes` | `TEXT` | NULL | Special desk notes |
| `status` | `VARCHAR(20)` | DEFAULT `'WAITING'`, NOT NULL | `'WAITING'`, `'SERVING'`, `'COMPLETED'`, or `'CANCELLED'` |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW(), NOT NULL | Ticket issuance timestamp |

---

### 2.6 Table: `reports_issuereport`
Maintains community-reported incidents, infrastructure defects, and hazard reports.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | PRIMARY KEY | Unique report ID |
| `reporter_id` | `INTEGER` | FK (`auth_user`), ON DELETE CASCADE | Resident user who filed the report |
| `title` | `VARCHAR(200)` | NOT NULL | Concise incident summary |
| `description` | `TEXT` | NOT NULL | Detailed narrative description |
| `location` | `VARCHAR(255)` | NOT NULL | Landmark, purok, or physical location |
| `image_url` | `VARCHAR(512)` | NULL | Secure CDN link returned from Cloudinary |
| `category` | `VARCHAR(50)` | DEFAULT `'OTHER'`, NOT NULL | `'PEACE_AND_ORDER'`, `'PUBLIC_HEALTH'`, `'INFRASTRUCTURE'`, `'ENVIRONMENT'`, `'OTHER'` |
| `urgency` | `VARCHAR(20)` | DEFAULT `'MINOR'`, NOT NULL | `'MINOR'`, `'MODERATE'`, `'HAZARD'`, `'EMERGENCY'` |
| `status` | `VARCHAR(20)` | DEFAULT `'PENDING'`, NOT NULL | `'PENDING'`, `'IN_PROGRESS'`, `'RESOLVED'`, `'DISMISSED'` |
| `incident_datetime` | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW(), NOT NULL | Time of incident occurrence |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW(), NOT NULL | Submission timestamp |

---

### 2.7 Table: `audit_auditlog`
Maintains a tamper-evident audit trail of administrative actions for governance accountability.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | PRIMARY KEY | Unique audit log ID |
| `user_id` | `INTEGER` | FK (`auth_user`), NULL, ON DELETE SET NULL | Official who executed the action |
| `action_type` | `VARCHAR(50)` | NOT NULL | Categorical action identifier (e.g., 'DOCUMENT_ACTION', 'QUEUE_ACTION') |
| `description` | `TEXT` | NOT NULL | Human-readable explanation of the state change |
| `ip_address` | `INET` | NULL | Client IP address at time of request |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW(), NOT NULL | Immutable log timestamp |

---

### 2.8 Table: `communications_announcement`
Stores official community bulletins and emergency broadcasts.

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `SERIAL` | PRIMARY KEY | Unique announcement ID |
| `barangay_id` | `INTEGER` | FK (`auth_barangay`), ON DELETE CASCADE | Originating Barangay |
| `title` | `VARCHAR(200)` | NOT NULL | Announcement title |
| `content` | `TEXT` | NOT NULL | Announcement markdown content |
| `category` | `VARCHAR(30)` | NOT NULL | `'AID'`, `'MEDICAL'`, `'EVENT'`, `'GENERAL'` |
| `scheduled_date`| `TIMESTAMP WITH TIME ZONE` | NOT NULL | Scheduled display timestamp |
| `created_by_id` | `INTEGER` | FK (`auth_user`), ON DELETE CASCADE | Authoring official |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | DEFAULT NOW(), NOT NULL | Publication timestamp |