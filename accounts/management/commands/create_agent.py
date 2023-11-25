from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.game.models import Agent
from apps.wallet.models import Wallet

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a agents user'

    def add_arguments(self, parser):
        parser.add_argument('phone_number', type=str, help='Phone Number for the new user')
        parser.add_argument('email', type=str, help='Email for the new user')
        parser.add_argument('password', type=str, help='Password for the new user')

    def handle(self, *args, **options):
        phone_number = options['phone_number']
        email = options['email']
        password = options['password']

        User = get_user_model()

        try:
            user = User.objects.create_agent(phone_number=phone_number, email=email, password=password)
            Wallet.objects.create(user=user)
            Agent.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Successfully created user {phone_number} with user type'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {str(e)}'))
