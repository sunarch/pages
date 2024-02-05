# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Setup"""

# library
import ast
import re
from re import Pattern

# requirements
from setuptools import setup, find_packages

PROGRAM_NAME: str = 'sunarch-pages'
VERSION_MAJOR: int = 0
VERSION_MINOR: int = 1
VERSION_PATCH: int = 0
DEVELOPMENT_STATUS: int = 4
MIN_PYTHON_VERSION: str = '3.9'


def name() -> str:
    """Construct package name with required prefix"""
    return f'lektor-{PROGRAM_NAME}'


def version() -> str:
    """Construct version string"""
    return '.'.join(map(str, [VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH]))


def description(parse_from_source: bool = False) -> str:
    """Read description from class attribute or construct here"""

    if not parse_from_source:
        return f'{PROGRAM_NAME} - Personal website SSG plugin'

    _description_re: Pattern = re.compile(r'description\s+=\s+(?P<description>.*)')

    with open('lektor_proglangs.py', 'rb') as f:
        return str(ast.literal_eval(_description_re.search(
            f.read().decode('UTF-8')).group(1)))


def readme() -> str:
    """Read README from file"""
    with open('README.md', 'r', encoding='UTF-8') as fh_readme:
        return fh_readme.read()


def development_status() -> str:
    """Choose development status"""

    status_values: dict[int, str] = {
        1: 'Development Status :: 1 - Planning',
        2: 'Development Status :: 2 - Pre-Alpha',
        3: 'Development Status :: 3 - Alpha',
        4: 'Development Status :: 4 - Beta',
        5: 'Development Status :: 5 - Production/Stable',
        6: 'Development Status :: 6 - Mature',
        7: 'Development Status :: 7 - Inactive'
    }

    if DEVELOPMENT_STATUS not in status_values:
        return status_values[1]

    return status_values[DEVELOPMENT_STATUS]


def requirements() -> str:
    """Read requirements from file"""
    with open('requirements.txt', 'r', encoding='UTF-8') as fh_requirements:
        return fh_requirements.read()


def python_requires() -> str:
    """Construct Python requirement string"""
    return f'>={MIN_PYTHON_VERSION}'


def main_module_name() -> str:
    """Convert program name to the main module name"""
    return name().replace('-', '_')


def plugin_class_name() -> str:
    """Convert program name to plugin class name"""
    parts: list[str] = PROGRAM_NAME.split('-')
    pascal_case: str = ''.join(map(lambda x: x.capitalize(), parts))
    return f'{pascal_case}Plugin'


setup(
    # [metadata]
    name=name(),
    version=version(),
    description=description(),
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://codeberg.org/sunarch/pages',
    project_urls={
        'Bug Tracker': 'https://codeberg.org/sunarch/pages/issues'
    },
    author='András Németh (sunarch)',
    author_email='sunarch@protonmail.com',
    maintainer='András Németh (sunarch)',
    maintainer_email='sunarch@protonmail.com',
    classifiers=[
        development_status(),
        'Environment :: Plugins',
        'Framework :: Lektor',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Typing :: Typed'
    ],
    license='Mozilla Public License 2.0 (MPL 2.0)',
    keywords='sunarch,pages,Lektor plugin',
    platforms='Any',

    # [options]
    install_requires=requirements(),
    python_requires=python_requires(),
    packages=find_packages(),
    py_modules=[
        main_module_name()
    ],

    # [options.entry_points]
    entry_points={
        'lektor.plugins': [
            f'{PROGRAM_NAME} = {main_module_name()}:{plugin_class_name()}',
        ]
    }
)
