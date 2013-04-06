from distutils.core import setup


setup(
    name='tincture',
    version='0.0.0',
    description='Django and SQLAlchemy all mixed up.',
    license='MIT',
    author='Joe Friedl',
    author_email='joe@joefriedl.net',
    packages=['tincture'],
    install_requires=[
        'Django==1.4',
        'SQLAlchemy==0.7.8',
    ]
)
