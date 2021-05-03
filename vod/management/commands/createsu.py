from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
from vod_auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email="shivendu@iitbhilai.ac.in").exists():
            User.objects.create_superuser(
                "shivendu@iitbhilai.ac.in", "TJ#(Dkp9U@")
            print("Created new superuser")
        else:
            print("Superuser already exists")
