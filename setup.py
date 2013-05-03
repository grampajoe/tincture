from distutils.core import setup


setup(
    name='tincture',
    version='0.1.0',
    description='Django and SQLAlchemy all mixed up.',
    keywords='orm framework django sqlalchemy',
    url='https://github.com/grampajoe/tincture',
    license='MIT',
    author='Joe Friedl',
    author_email='joe@joefriedl.net',
    packages=['tincture'],
    install_requires=open('requirements.txt').readlines(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
