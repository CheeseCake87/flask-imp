"""
Flask-Launchpad v1(alt)
-------------

Enabling auto importing of blueprints and apis to allow you to use swarm of routes!
"""
from setuptools import setup


setup(
    name='Flask-Launchpad',
    version='1.0',
    url='https://uilix.com/flask-launchpad',
    license='MIT',
    author='David Carmichael | UiliX Ltd (UK, Scotland)',
    author_email='hello@uilix.com',
    description='A small auto importer for blueprints and apis',
    long_description=__doc__,
    py_modules=['flask_sqlite3'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
