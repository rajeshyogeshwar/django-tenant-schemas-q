import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_mscluster():
    call_command('mscluster', run_once=True)
