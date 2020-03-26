from django.contrib.auth.models import User


def print_users_in_tenant():
    print([x.username for x in User.objects.all()])


def print_emails_of_users_in_tenant():
    print([x.email for x in User.objects.all()])
