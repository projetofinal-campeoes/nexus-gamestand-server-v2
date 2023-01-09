from users.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create admin users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username", type=str, help="Define the name of the user admin."
        )
        parser.add_argument(
            "--password", type=str, help="Define the password of the user admin."
        )
        parser.add_argument(
            "--email", type=str, help="Define the email of the user admin."
        )
        parser.add_argument(
            "--steam_user", type=str, help="Define the steam_user of the user admin."
        )

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        password = kwargs["password"]
        email = kwargs["email"]
        steam_user = kwargs["steam_user"]

        if not username:
            username = "admin"

        if not password:
            password = "admin1234"

        if not steam_user:
            steam_user = "admin"

        if not email:
            email = f"{username}@example.com"

        if User.objects.filter(username=username):
            raise CommandError(f"Username `{username}` already taken.")

        if User.objects.filter(email=email):
            raise CommandError(f"Email `{email}` already taken.")

        User.objects.create_superuser(
            username=username,
            password=password,
            email=email,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Admin `{username}` successfully created!")
        )
