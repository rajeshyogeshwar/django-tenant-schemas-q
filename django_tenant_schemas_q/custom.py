# local
from django_tenant_schemas_q.utils import QUtilities

from django_q.conf import Conf
from django_q.brokers import get_broker


class Iter(object):
    """
    An async task with iterable arguments customised for django_tenant_schemas_q
    """

    def __init__(
        self,
        func=None,
        args=None,
        kwargs=None,
        cached=Conf.CACHED,
        sync=Conf.SYNC,
        broker=None,
    ):
        self.func = func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.id = ""
        self.broker = broker or get_broker()
        self.cached = cached
        self.sync = sync
        self.started = False

    def append(self, *args):
        """
        add arguments to the set
        """
        self.args.append(args)
        if self.started:
            self.started = False
        return self.length()

    def run(self):
        """
        Start queueing the tasks to the worker cluster
        :return: the task id
        """
        self.kwargs["cached"] = self.cached
        self.kwargs["sync"] = self.sync
        self.kwargs["broker"] = self.broker
        self.id = QUtilities.add_async_tasks_from_iter(self.func, self.args, **self.kwargs)
        self.started = True
        return self.id

    def result(self, wait=0):
        """
        return the full list of results.
        :param int wait: how many milliseconds to wait for a result
        :return: an unsorted list of results
        """
        if self.started:
            return QUtilities.get_result(self.id, wait=wait, cached=self.cached)

    def fetch(self, wait=0):
        """
        get the task result objects.
        :param int wait: how many milliseconds to wait for a result
        :return: an unsorted list of task objects
        """
        if self.started:
            return QUtilities.fetch_task(self.id, wait=wait, cached=self.cached)

    def length(self):
        """
        get the length of the arguments list
        :return int: length of the argument list
        """
        return len(self.args)


class Chain(object):
    """
    A sequential chain of tasks
    """

    def __init__(self,
                 chain=None,
                 group=None,
                 cached=Conf.CACHED,
                 sync=Conf.SYNC):

        self.chain = chain or []
        self.group = group or ""
        self.broker = get_broker()
        self.cached = cached
        self.sync = sync
        self.started = False

    def append(self, func, *args, **kwargs):
        """
        add a task to the chain
        takes the same parameters as async_task()
        """
        self.chain.append((func, args, kwargs))
        # remove existing results
        if self.started:
            QUtilities.delete_task_group(self.group)
            self.started = False
        return self.length()

    def run(self):
        """
        Start queueing the chain to the worker cluster
        :return: the chain's group id
        """
        self.group = QUtilities.create_async_tasks_chain(
            chain=self.chain[:],
            group=self.group,
            cached=self.cached,
            sync=self.sync,
            broker=self.broker,
        )
        self.started = True
        return self.group

    def result(self, wait=0):
        """
        return the full list of results from the chain when it finishes. blocks until timeout.
        :param int wait: how many milliseconds to wait for a result
        :return: an unsorted list of results
        """
        if self.started:
            return QUtilities.get_result_group(
                self.group, wait=wait, count=self.length(), cached=self.cached
            )

    def fetch(self, failures=True, wait=0):
        """
        get the task result objects from the chain when it finishes. blocks until timeout.
        :param failures: include failed tasks
        :param int wait: how many milliseconds to wait for a result
        :return: an unsorted list of task objects
        """
        if self.started:
            return QUtilities.fetch_task_group(
                self.group,
                failures=failures,
                wait=wait,
                count=self.length(),
                cached=self.cached,
            )

    def current(self):
        """
        get the index of the currently executing chain element
        :return int: current chain index
        """
        if not self.started:
            return None
        return QUtilities.get_group_count(self.group, cached=self.cached)

    def length(self):
        """
        get the length of the chain
        :return int: length of the chain
        """
        return len(self.chain)


class AsyncTask(object):
    """
    an async task
    """

    def __init__(self, func, *args, **kwargs):
        self.id = ""
        self.started = False
        self.func = func
        self.args = args
        self.kwargs = kwargs

    @property
    def broker(self):
        return self._get_option("broker", None)

    @broker.setter
    def broker(self, value):
        self._set_option("broker", value)

    @property
    def sync(self):
        return self._get_option("sync", None)

    @sync.setter
    def sync(self, value):
        self._set_option("sync", value)

    @property
    def save(self):
        return self._get_option("save", None)

    @save.setter
    def save(self, value):
        self._set_option("save", value)

    @property
    def hook(self):
        return self._get_option("hook", None)

    @hook.setter
    def hook(self, value):
        self._set_option("hook", value)

    @property
    def group(self):
        return self._get_option("group", None)

    @group.setter
    def group(self, value):
        self._set_option("group", value)

    @property
    def cached(self):
        return self._get_option("cached", Conf.CACHED)

    @cached.setter
    def cached(self, value):
        self._set_option("cached", value)

    def _set_option(self, key, value):
        if "q_options" in self.kwargs:
            self.kwargs["q_options"][key] = value
        else:
            self.kwargs[key] = value
        self.started = False

    def _get_option(self, key, default=None):
        if "q_options" in self.kwargs:
            return self.kwargs["q_options"].get(key, default)
        else:
            return self.kwargs.get(key, default)

    def run(self):
        self.id = async_task(self.func, *self.args, **self.kwargs)
        self.started = True
        return self.id

    def result(self, wait=0):

        if self.started:
            return QUtilities.get_result(self.id, wait=wait, cached=self.cached)

    def fetch(self, wait=0):

        if self.started:
            return QUtilities.fetch_task(self.id, wait=wait, cached=self.cached)

    def result_group(self, failures=False, wait=0, count=None):

        if self.started and self.group:
            return QUtilities.get_result_group(
                self.group,
                failures=failures,
                wait=wait,
                count=count,
                cached=self.cached,
            )

    def fetch_group(self, failures=True, wait=0, count=None):

        if self.started and self.group:
            return QUtilities.fetch_task_group(
                self.group,
                failures=failures,
                wait=wait,
                count=count,
                cached=self.cached,
            )
