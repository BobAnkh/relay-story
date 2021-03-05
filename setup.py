#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author       : BobAnkh
# @Github       : https://github.com/BobAnkh
# @Date         : 2021-02-24 23:38:33
# @LastEditTime : 2021-02-25 11:13:18
# @Description  :

import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

if os.getenv('TWINE_USERNAME') == '':
    USERNAME = input('PyPi username: ')
    os.environ['TWINE_USERNAME'] = USERNAME
if os.getenv('TWINE_PASSWORD') == '':
    PASSWORD = input('PyPi password: ')
    os.environ['TWINE_PASSWORD'] = PASSWORD

NAME = 'relaystory'
KEYWORDS = ['relay', 'story', 'framework', 'BobAnkh', 'multi-branch']
DESCRIPTION = 'A Framework for Multi-branch Relay Story'
about = {}
here = os.path.abspath(os.path.dirname(__file__))
project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
with open(os.path.join(here, project_slug, '__version__.py')) as f:
    exec(f.read(), about)
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        LONG_DESCRIPTION = '\n' + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION


class UploadCommand(Command):
    '''Support setup.py upload.'''

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        '''Prints things in bold.'''
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(
            sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(name=NAME,
      version=about['__version__'],
      keywords=KEYWORDS,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      license='Apache 2.0',
      url='https://github.com/BobAnkh/relay-story',
      author='BobAnkh',
      author_email='bobankhshen@gmail.com',
      packages=find_packages(),
      include_package_data=False,
      zip_safe=False,
      platforms=["any"],
      install_requires=[''],
      python_requires='>3',
      entry_points={
          'console_scripts': [
              'relaystory = relaystory.relaystory:main',
          ]
      },
      classifiers=[
          "Programming Language :: Python :: 3",
          "Environment :: Console",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent",
      ],
      cmdclass={
          'upload': UploadCommand,
      })
