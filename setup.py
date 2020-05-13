import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='django_tenant_schemas_q',
    version='1.0.0',
    author='Rajesh Yogeshwar',
    author_email='rajesh.yogeshwar@gmail.com',
    include_package_data=True,
    description='An integration package for Django-Q with Django Tenant Schemas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rajeshyogeshwar/django-tenant-schemas-q',
    license='MIT',
    packages=setuptools.find_packages(exclude=["test_project", "test-compose.yml"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "django-tenant-schemas>=1.10.0",
        "django-q>=1.2.1"
    ]
)
