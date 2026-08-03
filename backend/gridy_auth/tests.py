from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from gridy_auth.models import User

# Create your tests here.

class AuthAPITests(APITestCase):
    def setUp(self):
        #create a test resident user
        self.username = "resident_test"
        self.password = "SecurePassword123!"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="resident@example.com",
            role=User.Role.RESIDENT
        )

    def test_user_registration_success(self):
        url = reverse('auth_register')
        payload = {
            "username": "new_resident",
            "email": "new@example.com",
            "password": "ValidPassword123!",
            "full_name": "Test Resident",
            "birth_date": "2000-01-01"
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username="new_resident").count(), 1)

    def test_user_registration_weak_password(self):
        url = reverse('auth_register')
        payload = {
            "username": "weak_resident",
            "email": "weak@example.com",
            "password": "123",
            "full_name": "Weak Password Test Resident",
            "birth_date": "2000-01-01"
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_user_login_success(self):
        url = reverse('auth_login')
        payload  = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_profile_endpoint_requires_auth(self):
        # Hardcoding path to catch routing bugs
        url = "/api/v1/auth/me/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_endpoint_success(self):
        #  1. Login the user to obtain a token
        login_url = reverse('auth_login')
        login_payload = {
            "username": self.username,
            "password": self.password
        }
        login_response = self.client.post(login_url, login_payload, format='json')
        token = login_response.data['access']

        # 2. Add JWT token to Auth headers
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # 3. Request the user profile
        url = "/api/v1/auth/me/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.username)
           
    def test_import_residents_requires_auth(self):
        url = reverse('import_residents')
        response = self.client.post(url, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_import_residents_blocked_for_resident(self):
        # Log in as a resident
        self.client.force_login(self.user)
        url = reverse('import_residents')
        response = self.client.post(url, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_import_residents_success(self):
        # Create an official (admin)
        official = User.objects.create_user(
            username="official_test_import",
            password="SecurePassword123!",
            role=User.Role.ADMIN
        )
        self.client.force_login(official)

        # Mock CSV data inside memory using BytesIO
        import io
        csv_data = (
            "username,email,full_name,birth_date,contact_number,voter_status\n"
            "imported1,imported1@example.com,Imported One,1995-10-15,09170000001,True\n"
            "imported2,,Imported Two,1988-02-20,,False\n"
        )
        csv_file = io.BytesIO(csv_data.encode('utf-8'))
        csv_file.name = 'residents.csv'

        url = reverse('import_residents')
        response = self.client.post(url, {'file': csv_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['imported'], 2)
        self.assertEqual(response.data['skipped_due_to_duplicate'], 0)
        self.assertEqual(len(response.data['errors']), 0)

        # Verify database records were created properly
        self.assertTrue(User.objects.filter(username="imported1").exists())
        user1 = User.objects.get(username="imported1")
        self.assertEqual(user1.profile.full_name, "Imported One")
        self.assertEqual(user1.profile.birth_date.strftime("%Y-%m-%d"), "1995-10-15")
        self.assertTrue(user1.profile.voter_status)

        # Verify password auto-generation (birthdate format YYYYMMDD)
        self.assertTrue(user1.check_password("19951015"))
        
    def test_import_residents_validation_error(self):
        official = User.objects.create_user(
            username="official_test_import_err",
            password="SecurePassword123!",
            role=User.Role.ADMIN
        )
        self.client.force_login(official)

        # Mock CSV containing rows with missing fields and bad date format
        import io 
        csv_data = (
            "username,email,full_name,birth_date,contact_number,voter_status\n"  # <-- Comma after email
            "badrow1,bad1@example.com,,1995-10-14,,True\n" # missing full_name
            "badrow2,,Bad Date,10-15-1995,,False\n" # bad date format (MM-DD-YYYY)
            "imported3,,Imported Three,2001-09-09,,False\n" # valid
        )
        csv_file = io.BytesIO(csv_data.encode('utf-8'))
        csv_file.name = 'residents_err.csv'  # <-- Assign directly to the attribute

        url = reverse('import_residents')
        response = self.client.post(url, {'file': csv_file}, format='multipart')

        # 207 Multi-Status expected due to validation errors in rows 1 and 2
        self.assertEqual(response.status_code, status.HTTP_207_MULTI_STATUS)
        self.assertEqual(response.data['imported'], 1)
        self.assertEqual(len(response.data['errors']), 2)
        self.assertTrue(User.objects.filter(username="imported3").exists())
