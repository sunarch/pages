import ast
import io
import re

from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r'description\s+=\s+(?P<description>.*)')

with open('lektor_proglangs.py', 'rb') as f:
    description = str(ast.literal_eval(_description_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    author='András Németh',
    author_email='sunarch@protonmail.com',
    description=description,
    keywords='Lektor plugin',
    license='MPL-2.0',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-proglangs',
    packages=find_packages(),
    py_modules=[
        'lektor_proglangs',
        'proglangs',
        'proglangs_age',
        'proglangs_comparison',
        'proglangs_rankings'
    ],
    # url='[link to your repository]',
    version='0.1',
    classifiers=[
        'Framework :: Lektor',
        'Environment :: Plugins',
    ],
    entry_points={
        'lektor.plugins': [
            'proglangs = lektor_proglangs:ProglangsPlugin',
        ]
    }
)
