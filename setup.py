import codecs
import os
import re

from setuptools import Command, find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

version = "0.0.0"
changes = os.path.join(here, "CHANGES.rst")
match = r'^#*\s*(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)$'
with codecs.open(changes, encoding='utf-8') as changes:
    for line in changes:
        res = re.match(match, line)
        if res:
            version = res.group("version")
            break

# Get the long description
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get version
with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changelog = f.read()


class VersionCommand(Command):
    description = "print library version"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


setup(
    name='py-contract',
    version=version,
    description="py-contract is a tool that helps you to keep two the communication"
                "between parts of your microservice architecture on the same page",
    long_description=long_description,
    url='https://github.com/felipevolpone/contract',
    author='Felipe Volpone',
    author_email='felipevolpone@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='contract api rest pact',
    packages=find_packages(exclude=['docs', 'tests*']),
    cmdclass={
        "version": VersionCommand,
    },
)
