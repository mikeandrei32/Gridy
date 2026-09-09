from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from gridy_auth.models import User, Barangay, Resident
from gridy_communications.models import Announcement, ActivitySchedule, EmergencyHotline
from gridy_services.models import DocumentRequest, QueueTicket


class Command(BaseCommand):
    help = "Seed approved partner barangays (Ibabang Dupay & Daungan) with authentic users, announcements, and services."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding approved partner barangays..."))

        # ---------------------------------------------------------------------
        # 1. Partner Barangays Provisioning
        # ---------------------------------------------------------------------
        dupay, _ = Barangay.objects.get_or_create(
            name="Barangay Ibabang Dupay",
            defaults={
                "captain_name": "Hon. Alberto M. Rodil",
                "office_contact": "Ibabang Dupay Barangay Hall, Lucena City | (042) 710-2345",
            }
        )
        self.stdout.write(self.style.SUCCESS(f"Provisioned: {dupay.name}"))

        daungan, _ = Barangay.objects.get_or_create(
            name="Barangay Daungan",
            defaults={
                "captain_name": "Hon. Bernardo C. Portes",
                "office_contact": "Daungan Barangay Hall, Pagbilao, Quezon | (042) 731-1234",
            }
        )
        self.stdout.write(self.style.SUCCESS(f"Provisioned: {daungan.name}"))

        # ---------------------------------------------------------------------
        # 2. Users & Resident Profiles
        # ---------------------------------------------------------------------
        # A. Ibabang Dupay Users
        admin_dupay, created = User.objects.get_or_create(
            username="admin_dupay",
            defaults={
                "email": "captain.dupay@gridy.local",
                "first_name": "Alberto",
                "last_name": "Rodil",
                "role": User.Role.ADMIN,
                "barangay": dupay,
                "is_staff": True,
            }
        )
        if created:
            admin_dupay.set_password("Password123!")
            admin_dupay.save()

        tanod_dupay, created = User.objects.get_or_create(
            username="tanod_dupay",
            defaults={
                "email": "tanod.dupay@gridy.local",
                "first_name": "Rogelio",
                "last_name": "Alcala",
                "role": User.Role.FIELD_OFFICIAL,
                "barangay": dupay,
            }
        )
        if created:
            tanod_dupay.set_password("Password123!")
            tanod_dupay.save()

        resident_dupay, created = User.objects.get_or_create(
            username="resident_dupay",
            defaults={
                "email": "resident.dupay@gridy.local",
                "first_name": "Maria",
                "last_name": "Santos",
                "role": User.Role.RESIDENT,
                "barangay": dupay,
            }
        )
        if created:
            resident_dupay.set_password("Password123!")
            resident_dupay.save()
            Resident.objects.get_or_create(
                user=resident_dupay,
                defaults={
                    "full_name": "Maria Santos",
                    "birth_date": date(1996, 4, 18),
                    "voter_status": True,
                    "contact_number": "09181234567",
                    "purok": "Purok 3 - Sampaguita",
                    "is_verified": True,
                }
            )

        # B. Daungan Users
        admin_daungan, created = User.objects.get_or_create(
            username="admin_daungan",
            defaults={
                "email": "captain.daungan@gridy.local",
                "first_name": "Bernardo",
                "last_name": "Portes",
                "role": User.Role.ADMIN,
                "barangay": daungan,
                "is_staff": True,
            }
        )
        if created:
            admin_daungan.set_password("Password123!")
            admin_daungan.save()

        resident_daungan, created = User.objects.get_or_create(
            username="resident_daungan",
            defaults={
                "email": "resident.daungan@gridy.local",
                "first_name": "Danilo",
                "last_name": "Villanueva",
                "role": User.Role.RESIDENT,
                "barangay": daungan,
            }
        )
        if created:
            resident_daungan.set_password("Password123!")
            resident_daungan.save()
            Resident.objects.get_or_create(
                user=resident_daungan,
                defaults={
                    "full_name": "Danilo Villanueva",
                    "birth_date": date(1988, 11, 24),
                    "voter_status": True,
                    "contact_number": "09209876543",
                    "purok": "Purok Baybayin",
                    "is_verified": True,
                }
            )

        self.stdout.write(self.style.SUCCESS("Provisioned administrative and resident users."))

        # ---------------------------------------------------------------------
        # 3. Community Announcements
        # ---------------------------------------------------------------------
        Announcement.objects.get_or_create(
            title="Annual Barangay Assembly & Financial Transparency Report",
            defaults={
                "content": "Notice is hereby given to all residents of Barangay Ibabang Dupay for the First Semester General Assembly. Financial reports and upcoming infrastructure projects will be presented.",
                "is_pinned": True,
                "created_by": admin_dupay,
            }
        )

        Announcement.objects.get_or_create(
            title="Fisherfolk Registration & Coastal Welfare Drive",
            defaults={
                "content": "Barangay Daungan, in coordination with the Pagbilao Municipal Agriculture Office, invites all local fishermen for the annual registration and banca safety tagging.",
                "is_pinned": True,
                "created_by": admin_daungan,
            }
        )

        # ---------------------------------------------------------------------
        # 4. Activity Schedules
        # ---------------------------------------------------------------------
        ActivitySchedule.objects.get_or_create(
            title="Free Anti-Rabies Vaccination for Domestic Pets",
            defaults={
                "description": "Lucena City Veterinary Office will conduct a mass rabies vaccination drive at the Ibabang Dupay Covered Court.",
                "event_datetime": timezone.now() + timedelta(days=5),
                "location": "Ibabang Dupay Multi-Purpose Covered Court",
                "created_by": admin_dupay,
            }
        )

        ActivitySchedule.objects.get_or_create(
            title="Coastal Resource Management & Mangrove Planting",
            defaults={
                "description": "Join the youth council and volunteer fisherfolk in planting 500 mangrove saplings along the coastal shoreline.",
                "event_datetime": timezone.now() + timedelta(days=7),
                "location": "Daungan Coastal Shoreline Zone",
                "created_by": admin_daungan,
            }
        )

        # ---------------------------------------------------------------------
        # 5. Authentic Document Requests (with LGU statutory fees)
        # ---------------------------------------------------------------------
        DocumentRequest.objects.get_or_create(
            user=resident_dupay,
            document_type="Barangay Clearance",
            defaults={
                "barangay": dupay,
                "purpose": "Local Employment Requirement",
                "urgency_tag": DocumentRequest.UrgencyTag.REGULAR,
                "status": DocumentRequest.Status.READY_FOR_PICKUP,
                "fee_amount": 50.00,
                "or_number": "OR-2026-0891",
                "admin_notes": "Requirements verified; applicant is a bona fide resident.",
            }
        )

        DocumentRequest.objects.get_or_create(
            user=resident_daungan,
            document_type="Certificate of Indigency",
            defaults={
                "barangay": daungan,
                "purpose": "Hospital Medical Assistance",
                "urgency_tag": DocumentRequest.UrgencyTag.URGENT,
                "status": DocumentRequest.Status.RELEASED,
                "fee_amount": 0.00,
                "or_number": "EXEMPT",
                "admin_notes": "Verified indigent household by Barangay Social Worker.",
            }
        )

        # ---------------------------------------------------------------------
        # 6. Live Queue Tickets
        # ---------------------------------------------------------------------
        QueueTicket.objects.get_or_create(
            ticket_number="T001",
            defaults={
                "user": resident_dupay,
                "barangay": dupay,
                "service_type": "Document Pickup",
                "status": QueueTicket.Status.SERVING,
                "priority_status": QueueTicket.Priority.REGULAR,
            }
        )

        QueueTicket.objects.get_or_create(
            ticket_number="T002",
            defaults={
                "user": resident_daungan,
                "barangay": daungan,
                "service_type": "Indigency Assessment",
                "status": QueueTicket.Status.WAITING,
                "priority_status": QueueTicket.Priority.REGULAR,
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded all partner barangays and services."))