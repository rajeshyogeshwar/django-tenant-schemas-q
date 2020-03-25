from django.test import TestCase
from django.contrib.auth.models import User
from django_tenant_schemas_q.utils import QUtilities
from tenant_schemas.utils import get_tenant_model, schema_context

class BaseSetup(TestCase):
    
    def setUp(self):

        model_class = get_tenant_model()
        public = model_class.objects.create(domain_url='testproject.localhost', schema_name='public', name='Public')
        tone = model_class.objects.create(domain_url='testone.testproject.localhost', schema_name='testone', name='Test One')
        ttwo = model_class.objects.create(domain_url='testtwo.testproject.localhost', schema_name='testtwo', name='Test Two')

        with schema_context('testone'):
            User.objects.create(first_name='Subject', last_name='One', username='subjectone', email='subjectone@mailinator.com')

        with schema_context('testtwo'):
            User.objects.create(first_name='Subject', last_name='Two', username='subjecttwo', email='subjecttwo@mailinator.com')

    def test_async_task(self):
        
        with schema_context('testone'):
            QUtilities.add_async_task('print_users_in_tenant')

        with schema_context('testtwo'):
            QUtilities.add_async_task('print_users_in_tenant')