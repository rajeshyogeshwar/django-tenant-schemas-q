# django
from django.db import connection

# local
from django_q.conf import Conf, logger
from tenant_schemas.utils import schema_context
from django_q.tasks import schedule, async_task, result


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
