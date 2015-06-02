from setuptools import setup, find_packages
from os import path

# Read the README to use as the description
readme = path.join(path.abspath(path.dirname(__file__)), 'README.rst')
with open(readme) as f:
    readme = f.read()

setup(
        name='pyramid_wiring',
        version='0.1.0.dev1',
        description='Pyramid integration for the wiring library',
        long_description=readme,
        license='MIT',
        url='https://github.com/veeti/pyramid_wiring',
        author='Veeti Paananen',
        author_email='veeti.paananen@rojekti.fi',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Framework :: Pyramid',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
        ],
        keywords='pyramid wiring dependency injection',

        packages=find_packages(),
        install_requires=[
            'pyramid >= 1.4.0',
            'wiring >= 0.2.1',
        ],
        extras_require={
            'test': [
                'pytest',
                'webtest',
            ],
        },
)
