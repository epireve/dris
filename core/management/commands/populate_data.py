from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random
from core.models import DisasterReport, AidRequest, Shelter, VolunteerProfile

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Populate database with sample disaster data for Malaysian states in December"
    )

    def handle(self, *args, **options):
        self.stdout.write("Starting data population...")

        # Create users
        self.create_users()

        # Create shelters
        self.create_shelters()

        # Create disaster reports
        self.create_disaster_reports()

        # Create aid requests
        self.create_aid_requests()

        self.stdout.write(
            self.style.SUCCESS("Successfully populated database with sample data!")
        )

    def create_users(self):
        """Create sample users for different roles"""
        self.stdout.write("Creating users...")

        # Citizens
        citizens_data = [
            ("ahmad_shah", "ahmad@example.com", "Ahmad Shah"),
            ("siti_aminah", "siti@example.com", "Siti Aminah"),
            ("lee_wei_ming", "lee@example.com", "Lee Wei Ming"),
            ("priya_devi", "priya@example.com", "Priya Devi"),
            ("robert_tan", "robert@example.com", "Robert Tan"),
            ("fatimah_ali", "fatimah@example.com", "Fatimah Ali"),
            ("chen_mei_ling", "chen@example.com", "Chen Mei Ling"),
            ("rajesh_kumar", "rajesh@example.com", "Rajesh Kumar"),
            ("nurul_huda", "nurul@example.com", "Nurul Huda"),
            ("david_wong", "david@example.com", "David Wong"),
        ]

        self.citizens = []
        for username, email, full_name in citizens_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": "CITIZEN",
                    "first_name": full_name.split()[0],
                    "last_name": " ".join(full_name.split()[1:]),
                },
            )
            if created:
                user.set_password("password123")
                user.save()
            self.citizens.append(user)

        # Volunteers
        volunteers_data = [
            ("volunteer_amir", "amir.vol@example.com", "Amir Volunteer"),
            ("volunteer_lisa", "lisa.vol@example.com", "Lisa Volunteer"),
            ("volunteer_raj", "raj.vol@example.com", "Raj Volunteer"),
            ("volunteer_mary", "mary.vol@example.com", "Mary Volunteer"),
            ("volunteer_hassan", "hassan.vol@example.com", "Hassan Volunteer"),
        ]

        self.volunteers = []
        for username, email, full_name in volunteers_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": "VOLUNTEER",
                    "first_name": full_name.split()[0],
                    "last_name": " ".join(full_name.split()[1:]),
                },
            )
            if created:
                user.set_password("password123")
                user.save()
            self.volunteers.append(user)

        # Authorities
        authorities_data = [
            ("authority_selangor", "auth.selangor@example.com", "Selangor Authority"),
            ("authority_pahang", "auth.pahang@example.com", "Pahang Authority"),
            (
                "authority_terengganu",
                "auth.terengganu@example.com",
                "Terengganu Authority",
            ),
        ]

        self.authorities = []
        for username, email, full_name in authorities_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": "AUTHORITY",
                    "first_name": full_name.split()[0],
                    "last_name": " ".join(full_name.split()[1:]),
                },
            )
            if created:
                user.set_password("password123")
                user.save()
            self.authorities.append(user)

    def create_shelters(self):
        """Create sample shelters"""
        self.stdout.write("Creating shelters...")

        shelters_data = [
            ("Dewan Orang Ramai Klang", "Klang, Selangor", 200, 150),
            ("Sekolah Kebangsaan Kuantan", "Kuantan, Pahang", 150, 120),
            ("Masjid Al-Hidayah", "Kuala Terengganu, Terengganu", 100, 80),
            ("Balai Raya Seremban", "Seremban, Negeri Sembilan", 180, 160),
            ("Pusat Komuniti Shah Alam", "Shah Alam, Selangor", 250, 200),
            ("Dewan Serbaguna Bentong", "Bentong, Pahang", 120, 100),
            ("Sekolah Menengah Dungun", "Dungun, Terengganu", 130, 110),
            ("Balai Bomba Port Dickson", "Port Dickson, Negeri Sembilan", 90, 75),
        ]

        for name, location, capacity, availability in shelters_data:
            Shelter.objects.get_or_create(
                name=name,
                defaults={
                    "location": location,
                    "capacity": capacity,
                    "availability": availability,
                    "contact_info": "+60123456789",
                    "is_active": True,
                },
            )

    def create_disaster_reports(self):
        """Create sample disaster reports for December flood scenarios"""
        self.stdout.write("Creating disaster reports...")

        # December flood scenarios in Malaysian states
        disaster_scenarios = [
            # Selangor
            (
                "FLOOD",
                "Severe flooding in Klang due to heavy monsoon rains. Water level reached 2 meters in residential areas.",
                3.045891,
                101.444840,
                "HIGH",
                self.citizens[0],
            ),
            (
                "FLOOD",
                "Flash flood in Shah Alam affecting Seksyen 7 and surrounding areas.",
                3.073628,
                101.518652,
                "MEDIUM",
                self.citizens[1],
            ),
            (
                "LANDSLIDE",
                "Minor landslide on Genting Highlands road due to continuous rain.",
                3.421227,
                101.793600,
                "LOW",
                self.citizens[2],
            ),
            # Pahang
            (
                "FLOOD",
                "Major flooding in Kuantan city center. Several buildings evacuated.",
                3.808011,
                103.326447,
                "CRITICAL",
                self.citizens[3],
            ),
            (
                "FLOOD",
                "Temerloh district experiencing severe flooding. Emergency shelters activated.",
                3.450819,
                102.417527,
                "HIGH",
                self.citizens[4],
            ),
            (
                "FLOOD",
                "Pekan town flooded due to river overflow. Roads impassable.",
                3.487959,
                103.396187,
                "HIGH",
                self.citizens[5],
            ),
            # Terengganu
            (
                "FLOOD",
                "Kuala Terengganu facing worst flood in 5 years. Coastal areas severely affected.",
                5.328394,
                103.137115,
                "CRITICAL",
                self.citizens[6],
            ),
            (
                "FLOOD",
                "Kemaman district underwater. Multiple kampungs evacuated.",
                4.240508,
                103.425789,
                "HIGH",
                self.citizens[7],
            ),
            (
                "FLOOD",
                "Dungun experiencing flash floods. Main roads closed to traffic.",
                4.755178,
                103.414963,
                "MEDIUM",
                self.citizens[8],
            ),
            # Negeri Sembilan
            (
                "FLOOD",
                "Seremban hit by unexpected flash flood. Shopping complexes affected.",
                2.729468,
                101.939621,
                "MEDIUM",
                self.citizens[9],
            ),
        ]

        # Create reports with December dates
        base_date = datetime(2024, 12, 1, tzinfo=timezone.get_current_timezone())

        for i, (disaster_type, description, lat, lng, severity, reporter) in enumerate(
            disaster_scenarios
        ):
            # Spread reports across December
            report_date = base_date + timedelta(
                days=random.randint(0, 30), hours=random.randint(0, 23)
            )

            report = DisasterReport.objects.create(
                reporter=reporter,
                disaster_type=disaster_type,
                description=description,
                latitude=lat,
                longitude=lng,
                severity=severity,
                status=random.choice(["NEW", "VERIFIED", "IN_PROGRESS"]),
            )

            # Update timestamps to December
            report.timestamp = report_date
            report.last_updated = report_date + timedelta(hours=random.randint(1, 48))
            report.save()

    def create_aid_requests(self):
        """Create sample aid requests"""
        self.stdout.write("Creating aid requests...")

        # Get disaster reports to link aid requests
        disaster_reports = list(DisasterReport.objects.all())

        aid_scenarios = [
            (
                "FOOD",
                "Urgent need for food supplies for 50 families affected by flood.",
                50,
                "HIGH",
                "Taman Klang Utama, Block A-D",
            ),
            (
                "WATER",
                "Clean drinking water needed for flood victims in evacuation center.",
                200,
                "URGENT",
                "Dewan Orang Ramai Klang",
            ),
            (
                "MEDICAL",
                "Medical assistance required for elderly flood victims.",
                15,
                "URGENT",
                "Pusat Kesihatan Klang",
            ),
            (
                "SHELTER",
                "Temporary shelter needed for displaced families.",
                30,
                "HIGH",
                "Sekolah Kebangsaan Kuantan",
            ),
            (
                "RESCUE",
                "Rescue operation needed for stranded residents.",
                8,
                "URGENT",
                "Kampung Sungai Pahang",
            ),
            (
                "FOOD",
                "Emergency food rations for isolated village.",
                100,
                "HIGH",
                "Kampung Baru Kemaman",
            ),
            (
                "WATER",
                "Water purification tablets needed urgently.",
                500,
                "MEDIUM",
                "Kuala Terengganu flood area",
            ),
            (
                "MEDICAL",
                "First aid supplies and medicine required.",
                25,
                "HIGH",
                "Klinik Kesihatan Dungun",
            ),
            (
                "SHELTER",
                "Additional bedding and blankets for shelter.",
                80,
                "MEDIUM",
                "Balai Raya Seremban",
            ),
            (
                "FOOD",
                "Hot meals for rescue workers and volunteers.",
                40,
                "MEDIUM",
                "Pusat Operasi Bencana Shah Alam",
            ),
        ]

        base_date = datetime(2024, 12, 1, tzinfo=timezone.get_current_timezone())

        for i, (aid_type, description, quantity, priority, location) in enumerate(
            aid_scenarios
        ):
            # Random date in December
            request_date = base_date + timedelta(
                days=random.randint(1, 30), hours=random.randint(0, 23)
            )

            # Link to random disaster report
            disaster_report = (
                random.choice(disaster_reports) if disaster_reports else None
            )

            # Random requester
            requester = random.choice(self.citizens)

            aid_request = AidRequest.objects.create(
                requester=requester,
                disaster_report=disaster_report,
                aid_type=aid_type,
                description=description,
                quantity=quantity,
                priority=priority,
                location_details=location,
                status=random.choice(["PENDING", "APPROVED", "IN_PROGRESS"]),
                assigned_to=(
                    random.choice(self.volunteers)
                    if random.choice([True, False])
                    else None
                ),
            )

            # Update timestamps
            aid_request.timestamp = request_date
            aid_request.last_updated = request_date + timedelta(
                hours=random.randint(1, 24)
            )
            aid_request.save()
