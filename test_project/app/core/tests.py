# Standard
import random

# Django
from django.test import TransactionTestCase

# Packages
from django_q.brokers import get_broker
from tenant_schemas.utils import schema_context
from django_tenant_schemas_q.custom import Chain
from django_tenant_schemas_q.utils import QUtilities


class BaseSetup(TransactionTestCase):

    def setUp(self):
        print('Setting up tests')

    def test_async_task(self):
        with schema_context('testone'):
            task_id = QUtilities.add_async_task('core.tasks.print_users_in_tenant')
            print(QUtilities.fetch_task(task_id))

        with schema_context('testtwo'):
            task_id = QUtilities.add_async_task('core.tasks.print_users_in_tenant')
            print(QUtilities.fetch_task(task_id))

    def test_iter(self):

        broker = get_broker()
        broker.purge_queue()
        broker.cache.clear()

        numbers = [random.randrange(1, 30) * 0.75 for i in range(1, 5)]
        with schema_context('testone'):
            task_1 = QUtilities.add_async_tasks_from_iter('math.floor', numbers, sync=True)
            result = QUtilities.get_result(task_1)
            print(numbers, result)
            assert result is not None
            broker.cache.clear()

    def test_chain(self):

        broker = get_broker()
        broker.purge_queue()
        broker.cache.clear()

        with schema_context('testone'):

            chain = Chain(sync=True)
            chain.append('math.pow', 12, 2)
            chain.append('math.floor', 12.93)

            assert chain.length() == 2
            chain.run()

            result = chain.result(wait=1000)
            print(result)
            assert chain.current() == chain.length()
            assert len(result) == chain.length()

            task = chain.fetch()
            print(len(task))
            assert len(task) == chain.length()
            broker.cache.clear()
