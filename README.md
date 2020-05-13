
# Django Tenant Schemas Q

  

Django Tenant Schemas Q is a custom implementation for Django-Q cluster for projects that make use Django Tenant Schemas package to achieve multi-tenancy in their Django projects with Postgres as database service. Using this package, developer can setup a Django project to be multi-tenant and setup Django-Q cluster to work per tenant/schema basis. This package works with any other broker apart from Django ORM.

  

# Why the need for this package?

  

Although there is package *tenant-schemas-celery* supporting celery for multi-tenancy, I was quite intrigued by the *django-q* project and was exploring the possibility of making *django-q* work with *django-tenant-schemas*.

  

# Installation

  

pip install django-tenant-schemas-q

  

This should install *django-tenant-schemas* and *django-q*.

  

# How to set this up?

As a developer I often find that setting up projects, packages and getting configurations right is sometimes a relatively tough job. In order to make this work nicely, just follow the steps below.

  

- Refer to settings required by *django_tenant_schemas* mentioned [here](https://django-tenant-schemas.readthedocs.io/en/latest/install.html)

- Setup *django_tenant_schemas* as per the instructions in the above mentioned link. This will take care of setting up of *django_tenant_schemas*.

- Add *django_q* to TENANT_APPS setting. This will setup models like Task, Schedule on every tenant post migrations.

- Follow it up with setting up the Django-Q cluster that needs to be run in order to process tasks and run our scheduler.

- While setting up configuration for cluster, **make use of any other broker supported by Django-Q apart from Django ORM.**

- Finally add a setting **SCHEMAS_TO_BE_EXCLUDED_BY_SCHEDULER** in your settings file. The value for this setting is a list of schema that you wish to exclude from scheduler, If not specified, scheduler will exclude a schema by name *public* by default.

  

# How will this work

Assuming you have followed the instructions perfectly, you should now have settings looking like

  

SHARED_APPS = ['tenant_schemas', 'app_containing_tenant_model ', 'any_other_app_needed']

TENANT_APPS = ['django_q', 'standard_django_apps', 'any_other_app_needed']

INSTALLED_APPS = ['tenant_schemas', 'app_containing_tenant_model', 'django_q', 'standard_django_apps', 'any_other_app_needed']

TENANT_MODEL = 'app_name.ModelName'

SCHEMAS_TO_BE_EXCLUDED_BY_SCHEDULER = ['public']

Q_CLUSTER = {} # Configuration for Q Cluster

  

What these settings will do is simple. It will simply create *Task & Schedule* models per schema. Django-Q uses these modules to store the tasks and schedules. With these models now setup on per schema/tenant basis the things become a bit cleaner.

  

To run the cluster, use the command `python manage.py mscluster`

Once the command is fired, the cluster will start and accept the tasks and schedules.

  

Now, given that are schedules are tasks that are executed as per the frequency having them per schema/tenant basis is something that I wanted to achieve. This would give me ability to configure same tasks with different times and the system will work as expected.

  
# How to use it

To allow adding a task or schedule with database schema awareness, package contains utilities to make it is seamless.

Add the line `from django_tenant_schemas_q.utils import QUtilities` to the line from where you wish to add a `task` or a `schedule`

To add an async task you can use

    QUtilities.add_async_task(func_name_as_string, *args, **kwargs)
 You can add `sync=True` in kwargs to run the task synchronously.

To create a new schedule you can use

    QUtilities.create_schedule(func_name_as_string, *args, **kwargs)
 
To get a result of a single task

    QUtilities.get_result(task_id, wait=0, cached=Conf.CACHED)
 
To get a result of a group

    QUtilities.get_result_group(group_id, failures=False, wait=0, count=None, cached=Conf.CACHED)
 
To fetch a single task

    QUtilities.fetch_task(task_id, wait=0, cached=Conf.CACHED)

To fetch a group of tasks

    QUtilities.fetch_task_group(group_id, failures=True, wait=0, count=None, cached=Conf.CACHED)

To get count of groups

    QUtilities.get_group_count(group_id, failures=False, cached=Conf.CACHED)
 
 To delete a group of tasks

    QUtilities.delete_task_group(group_id, tasks=False, cached=Conf.CACHED)

To delete a task from cache

    QUtilities.delete_task_from_cache(task_id, broker=None)
 
To get the size of the queue

     QUtilities.get_queue_size(broker=None)
  
To add multiple async tasks using Iter

    QUtilities.add_async_tasks_from_iter(func, args_iter, **kwargs)
 For this use `Iter` from `django_tenant_schemas_q.custom` module.

To create a chain of tasks using Chain

    QUtilities.create_async_tasks_chain(chain, group=None, cached=Conf.CACHED, sync=Conf.SYNC, broker=None)
 For this use `Chain` from `django_tenant_schemas_q.custom` module.


# Test the project

There is a test django project in the repository. 
- Clone the repository
- Run `docker-compose -f test-compose.yml build`
- Run `docker-compose -f test-compose.yml up -d`
- Run `docker-compose -f test-compose.yml run backend python manage.py setupdata`
- Run `docker-compose -f test-compose.yml run backend python manage.py test --keepdb`


Full credit to authors https://github.com/Koed00 of Django-Q and https://github.com/bernardopires of Django-Tenant-Schemas for two wonderful packages.