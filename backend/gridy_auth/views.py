from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
)

import csv
import io
from datetime import datetime
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser
from gridy_auth.permissions import IsBarangayOfficial
from gridy_auth.models import User, Resident
from gridy_auth.serializers import UserSerializer

# Create your views here.

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status.HTTP_200_OK)


class ResidentImportView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBarangayOfficial]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"detail": "No file was uploaded"},
            status=status.HTTP_400_BAD_REQUEST    
        )
        if not file_obj.name.endswith('.csv') :
            return Response({"detail": "File is not a CSV."},
            status=status.HTTP_400_BAD_REQUEST    
        )

        try:
            # Decode file content
            decoded_file = file_obj.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
        except Exception as e:
            return Response({"detail": f"Error reading file: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST    
        )
        imported_count = 0
        skipped_count = 0
        errors = []

        try:
            with transaction.atomic():
                for row_idx, row in enumerate(reader, start=1):
                    username = row.get('username')
                    email = row.get('email', '')
                    full_name = row.get('full_name')
                    birth_date_str = row.get('birth_date')
                    contact_number = row.get('contact_number', '')
                    voter_status_str = row.get('voter_status', 'False')
                    
                    # Validation checks
                    if not username or not full_name or not birth_date_str:
                        errors.append(f"Row {row_idx}: Missing required files ('username', 'full_name', 'birth_date').")
                        continue

                    try:
                        # Parse birth date to validate YYYY-MM-DD format
                        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        errors.append(f"Row {row_idx}: Invalid date format for '{birth_date_str}'. Expected YYYY-MM-DD.")
                        continue

                    if User.objects.filter(username=username).exists():
                        skipped_count += 1
                        continue

                    # Clean voter status
                    voter_status = voter_status_str.strip().lower() in ['true', '1', 'yes']

                    # Initial password is birth_date formatted as YYYYMMDD
                    initial_password = birth_date.strftime('%Y%m%d')

                    # Create user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=initial_password,
                        role=User.Role.RESIDENT
                    )

                    # Create resident profile
                    Resident.objects.create(
                        user=user,
                        full_name=full_name,
                        birth_date=birth_date,
                        voter_status=voter_status,
                        contact_number=contact_number,
                    )
                    imported_count += 1
        except Exception as e:
            return Response({"detail": f"Database transaction error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        response_data = {
            "imported": imported_count,
            "skipped_due_to_duplicate": skipped_count,
            "errors": errors
        }

        if errors:
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
        return Response(response_data, status=status.HTTP_200_OK)

    