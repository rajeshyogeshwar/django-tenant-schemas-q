# django
from django.db import connection

# local
from django_q.conf import Conf, logger
from tenant_schemas.utils import schema_context
from django_q.tasks import schedule, async_task, result, \
    result_group, fetch, fetch_group, count_group, delete_group, \
    delete_cached, queue_size


class QUtilities(object):

    @staticmethod
    def add_async_task(func, *args, **kwargs):
        if "schema_name" not in kwargs:
            kwargs.update({"schema_name": connection.schema_name})
        return async_task(func, *args, **kwargs)

    @staticmethod
    def create_schedule(func, *args, **kwargs):
        schema_name = kwargs.get("schema_name", connection.schema_name)
        if schema_name:
            with schema_context(schema_name):
                return schedule(func, *args, **kwargs)
        else:
            logger.error("No schema name was provided")
            return None

    @staticmethod
    def get_result(task_id, wait=0, cached=Conf.CACHED):
        schema_name = connection.schema_name
        with schema_context(schema_name):
            return result(task_id, wait, cached)

    @staticmethod
    def get_result_group(group_id, failures=False, wait=0, count=None, cached=Conf.CACHED):
        schema_name = connection.schema_name
        with schema_context(schema_name):
            return result_group(group_id, failures=False, wait=0, count=None, cached=Conf.CACHED)

    @staticmethod
    def fetch_task(task_id, wait=0, cached=Conf.CACHED):
        schema_name = connection.schema_name
        with schema_context(schema_name):
            return fetch(task_id, wait, cached)

    @staticmethod
    def fetch_task_group(group_id, failures=True, wait=0, count=None, cached=Conf.CACHED):
        schema_name = connection.schema_name
        with schema_context(schema_name):
            return fetch_group(group_id, failures, wait, count, cached=cached)

    @staticmethod
    def get_group_count(group_id, failures=False, cached=Conf.CACHED):
        schema_name = connection.schema_name
        with schema_context(schema_name):
            return count_group(group_id, failures, cached)

    @staticmethod
    def delete_task_group(group_id, tasks=False, cached=Conf.CACHED):
        schema_name = connection.schema_name
        with schema_context(schema_name):
            return delete_group(group_id, tasks, cached)

    @staticmethod
    def delete_task_from_cache(task_id, broker=None):
        return delete_cached(task_id, broker=broker)

    @staticmethod
    def get_queue_size(broker=None):
        return queue_size(broker)
