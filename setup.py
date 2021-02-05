from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'pfdorun',
    version          = '2.2.0,
    description      = 'The pf-pfdorun plugin is a general purpose "swiss army" knife DS plugin that can be used to execute some CLI type commands on input directory trees.',
    long_description = readme,
    author           = 'Rudolph Pienaar',
    author_email     = 'dev@babyMRI.org',
    url              = 'http://wiki',
    packages         = ['pfdorun'],
    install_requires = ['chrisapp~=1.1.6'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.8',
    entry_points     = {
        'console_scripts': [
            'pfdorun = pfdorun.__main__:main'
            ]
        }
)
