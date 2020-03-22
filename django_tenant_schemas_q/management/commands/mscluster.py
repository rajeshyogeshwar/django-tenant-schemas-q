from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from django_tenant_schemas_q.cluster import MultiTenantCluster


class Command(BaseCommand):
    # Translators: help text for mscluster management command
    help = _(
        "Starts a customised Django Q Cluster designed to work with Django Tenant Schemas.")

    def add_arguments(self, parser):
        parser.add_argument(
            '--run-once',
            action='store_true',
            dest='run_once',
            default=False,
            help='Run once and then stop.',
        )

    def handle(self, *args, **options):
        q = MultiTenantCluster()
        q.start()
        if options.get('run_once', False):
            q.stop()
