from setuptools import setup

setup(
    name='storj_accounts',
    version='0.0.1',
    author='Storj Labs',
    author_email='hello@storj.io',
    packages=['accounts'],
    scripts=[],
    url='https://github.com/storj/accounts',
    license='MIT',
    description='Web service for managing bandwidth on shared Metadisk nodes.',
    long_description=open('README.md').read(),
    install_requires=[],
    extras_require={
        'test': [
            'tox'
        ]
    }
)
