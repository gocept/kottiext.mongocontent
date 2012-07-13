from setuptools import setup, find_packages
import os

version = '0.1'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='kottiext.mongocontent',
      version=version,
      description="Content types for kotti using mongoDB storage",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='bsd',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['kottiext'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'kotti',
          'mongoalchemy'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
