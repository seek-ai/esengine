# coding: utf-8

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = "Elasticsearch ODM inspired on MongoEngine"


setup(
    name='esengine',
    version="0.0.5",
    url='https://github.com/catholabs/esengine',
    license='MIT',
    author="Catholabs",
    author_email="catholabs@catho.com",
    description='Elasticsearch ODM inspired on MongoEngine',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    extras_require={
        "es0": ["elasticsearch<1.0.0"],
        "es1": ["elasticsearch>=1.0.0,<2.0.0"],
        "es2": ["elasticsearch>=2.0.0,<3.0.0"]
    },
    tests_require=[
        "pytest==2.8.3",
        "pytest-cov==2.2.0",
        "flake8==2.5.0",
        "pep8-naming==0.3.3",
        "flake8-debugger==1.4.0",
        "flake8-print==2.0.1",
        "flake8-todo==0.4",
        "radon==1.2.2"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ]
)
