#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click',
    'tabulate',
    'pysondb',
    'string-color',
    'pyfiglet'
]

setup(
    name='task-master-cli',
    version='0.1.0',
    description="Todo CLI",
    long_description=readme,
    author="Melk de Sousa",
    url='https://github.com/melkdesousa/task-master-cli',
    packages=find_packages(include=['app']),
    entry_points={
        'console_scripts': [
            'task-master=app.main:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords=['task', 'todo', 'cli', 'click'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ]
)
