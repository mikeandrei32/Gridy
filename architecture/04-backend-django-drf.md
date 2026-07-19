# 04 Backend Architecture (Django DRF)

## 1. Core Framework
Django acts as the core API service, leveraging Django REST Framework (DRF) to serialize relational models into RESTful JSON streams.

---

## 2. Directory Architecture
The backend uses Django's modular app strategy to separate feature domains:

```text
backend/
├── manage.py                   # Django management utility
├── config/                     # Project configuration directory
│   ├── __init__.py
│   ├── settings.py             # Database settings, middleware, and installed apps
│   ├── urls.py                 # Global URL dispatcher routing to app APIs
│   └── wsgi.py / asgi.py
├── gridy_auth/                 # Custom AbstractUser auth and RBAC JWT logic
├── gridy_services/             # Document request pipelines and queue logic
├── gridy_reports/              # Issue reports, multipart handlers, Cloudinary bridges
└── gridy_communications/        # Announcements and activity schedules
```

---

## 3. Configuration & Third-Party Services

### 3.1 Media Storage: Cloudinary Pipeline
Django routes resident issue media directly to Cloudinary. It relies on the `dj3-cloudinary-storage` package to intercept default file fields in Django:
*   **Django Setting:** `DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'`
*   **Result:** When an `ImageField` is saved, the binary is automatically streamed to the Cloudinary CDN. The model stores only the resulting secure URL string, preventing local disk filling.

### 3.2 Firebase Admin SDK (Push Alerts)
To trigger FCM alerts, the server instantiates the `firebase_admin` SDK during startup using the credentials specified in environment settings:
```python
# Initialized in settings.py / apps.py
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate(os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON'))
firebase_admin.initialize_app(cred)
```

---

## 4. RBAC & Security Implementation

### 4.1 SimpleJWT Configurations
Access tokens are configured with a 15-minute lifespan, while refresh tokens remain valid for 7 days to support the silent refresh flow.

### 4.2 Custom Permission Classes
To secure endpoints, we implement custom permission classes matching user roles:
```python
from rest_framework.permissions import BasePermission

class IsBarangayOfficial(BasePermission):
    """
    Allows access only to users with the 'ADMIN' role.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'ADMIN'
        )
```
This permission class is then declared on sensitive viewsets (e.g., `QueueViewSet` for advancing tickets, `DocumentRequestViewSet` for approving validation state changes).
