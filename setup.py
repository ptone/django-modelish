import codecs
import re
from os import path
from setuptools import setup


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path).read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-modelish',
    version=find_version('modelish', '__init__.py'),
    description='A simple markup and processor to make initial models.py less tedious',
    long_description=read('README.rst'),
    author='Preston Holmes',
    author_email='preston@ptone.com',
    license='BSD',
    url='http://github.com/ptone/django-modelish',
    packages=[
        'modelish',
    ],
    package_data={'':['*.yml']},
    include_package_data=True,
    install_requires=['pyyaml'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'modelish = modelish.cli:main',
        ],
    }
)
