from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from gridy_auth.models import User
from gridy_services.models import DocumentRequest, QueueTicket

# Create your tests here.

class ServiceAPITests(APITestCase):
    def setUp(self):
        # Create an official (admin)
        self.official = User.objects.create_user(
            username="official_test",
            password="SecurePassword123!",
            email="admin@example.com",
            role=User.Role.ADMIN
        )
        # Create a resident
        self.resident = User.objects.create_user(
            username="resident_test",
            password="SecurePassword123!",
            email="resident@example.com",
            role=User.Role.RESIDENT
        )
    
    # Example 1: Resident successfully requests a document
    def test_resident_can_create_document_request(self):
        self.client.force_login(self.resident)
        url = reverse('document-request-list')
        payload =  {
            "document_type": "Barangay Clearance",
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DocumentRequest.objects.count(), 1)        
        
    def test_resident_validated_blocked(self):
        self.client.force_login(self.resident)
        doc_req = DocumentRequest.objects.create(
            user=self.resident,
            document_type="Barangay Clearance",
        )
        url = reverse('document-request-validate', args=[doc_req.id])
        payload = {
            "status": "APPROVED"
        }
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        doc_req.refresh_from_db()
        self.assertEqual(doc_req.status, DocumentRequest.Status.PENDING) 

    def test_official_can_validate_document_request(self):
        self.client.force_login(self.official)
        doc_req = DocumentRequest.objects.create(
            user=self.resident,
            document_type="Barangay Clearance",
        )
        url = reverse("document-request-validate", args=[doc_req.id])
        payload = {
            "status": "APPROVED"
        }
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DocumentRequest.objects.get(user=self.resident).status, "APPROVED")
        

    def test_resident_can_create_queue_ticket(self):
        self.client.force_login(self.resident)
        url = reverse('ticket-list')
        payload = {
            "service_type": "DOCUMENT"
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QueueTicket.objects.count(), 1)
        self.assertEqual(QueueTicket.objects.first().ticket_number, 'T001')    
        
    def test_resident_cannot_advance_queue(self):
        self.client.force_login(self.resident)
        url = reverse('ticket-next-ticket')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_official_can_advance(self):
        self.client.force_login(self.official)
        url = reverse('ticket-next-ticket')
        ticket = QueueTicket.objects.create(
            status="WAITING",
            ticket_number="T001",
            service_type="DOCUMENT"
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "SERVING")


    