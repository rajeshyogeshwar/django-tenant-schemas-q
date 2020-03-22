import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='Django Tenant Schemas Q',
    version='0.0.1',
    author='Rajesh Yogeshwar',
    author_email='rajesh.yogeshwar@gmail.com',
    description='An integration package for Django-Q with Django Tenant Schemas',
    long_description=long_description,
    url='https://github.com/rajeshyogeshwar/django-tenant-schemas-q',
    packages=setuptools.find_packages(),
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
