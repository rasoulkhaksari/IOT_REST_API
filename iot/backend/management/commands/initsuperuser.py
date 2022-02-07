from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.create_superuser(os.environ["SUPERUSER_USERNAME"], os.environ["SUPERUSER_EMAIL"], os.environ["SUPERUSER_PASSWORD"])
