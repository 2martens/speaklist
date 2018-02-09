# -*- coding: utf-8 -*-

#   Copyright 2018 Jim Martens
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('twomartens/speaklist/speaklist.py').read(),
    re.M
).group(1)

with open("README.rst", "rb") as f:
    long_desc = f.read().decode()
setup(
    name="twomartens.speaklist",
    description="Helps with the management of a speaklist.",
    long_description=long_desc,
    long_description_content_type="text/x-rst; charset=UTF-8",
    author="Jim Martens",
    author_email="github@2martens.de",
    url="https://github.com/2martens/speaklist",
    version=version,
    namespace_packages=["twomartens"],
    packages=["twomartens.speaklist"],
    entry_points={
        "console_scripts": ['tm-speaklist = twomartens.speaklist.speaklist:main_console']
    },
    package_data={},
    python_requires="~=3.5",
    install_requires=[],
    license="Apache License 2.0",
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Console",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

)

