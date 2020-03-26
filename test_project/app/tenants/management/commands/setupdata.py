from django.contrib.auth.models import User
from django.core.management import call_command
from django.utils.translation import gettext as _
from django.core.management.base import BaseCommand
from tenant_schemas.utils import schema_context, get_tenant_model


class Command(BaseCommand):

    help = _('Sets up test data with two schemas and a user per schema')

    def handle(self, *args, **kwargs):

        model_class = get_tenant_model()

        model_class.objects.get_or_create(domain_url='testproject.localhost', schema_name='public', name='Public')

        model_class.objects.get_or_create(
            domain_url='testone.testproject.localhost',
            schema_name='testone', name='Test One')

        model_class.objects.create(
            domain_url='testtwo.testproject.localhost',
            schema_name='testtwo', name='Test Two')

        call_command('migrate_schemas', '--shared')
        call_command('migrate_schemas', '--tenant')

        with schema_context('testone'):
            User.objects.get_or_create(first_name='Subject', last_name='One',
                                       username='subjectone', email='subjectone@mailinator.com')

        with schema_context('testtwo'):
            User.objects.get_or_create(first_name='Subject', last_name='Two',
                                       username='subjecttwo', email='subjecttwo@mailinator.com')
