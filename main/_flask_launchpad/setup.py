from setuptools import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='Flask-Launchpad',
    version='0.6.5',
    url='https://github.com/CheeseCake87/Flask-Launchpad',
    license='MIT',
    author='David Carmichael',
    author_email='carmichaelits@gmail.com',
    description='A small auto importer for blueprints and apis + some extras',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['flask_launchpad'],
    zip_safe=True,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask', 'toml'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)
