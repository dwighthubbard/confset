#!/usr/bin/python
"""
Package configuration for confset module and utility
"""
from distutils.core import setup
#noinspection PyStatementEffect
"""
 Copyright (c) 2012-2014 Dwight Hubbard. All rights reserved.
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License. See accompanying LICENSE file.
"""

setup(
    name="confset",
    version="0.0.35",
    author="Dwight Hubbard",
    author_email="d@d-h.us",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: System :: Power (UPS)',
    ],
    url="http://computing.dwighthubbard.info",
    license="Apache 2.0",
    packages=["confset"],
    scripts=['bin/confset'],
    long_description=open('README.rst').read(),
    description="A simple script to change or update package configurations",
    requires=['configobj'],
)
