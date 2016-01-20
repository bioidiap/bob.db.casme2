#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

# Define package version
version = open("version.txt").read().rstrip()

from bob.extension.utils import load_requirements
install_requires = load_requirements()

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    name='bob.db.casme2',
    version=version,
    description='CASME2  Database Access API for Bob',
    url='https://pypi.python.org/pypi/bob.db.casme2',
    license='GPLv3',
    author='Abdullahi Adamu',
    author_email='research.abdullah@gmail.com',
    keywords='micro-expressions, bob, bob.db, CASME2',
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires = install_requires,

    entry_points = {
      # bob database declaration
      'bob.db': [
        'casme2 = bob.db.casme2.driver:Interface',
      ],
    },

    classifiers = [
      'Framework :: Bob',
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Intended Audience :: Education',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.7',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Database :: Front-Ends',
    ],
)
