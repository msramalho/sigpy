from setuptools import setup
import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='sigpy',
      version='1.0',
      description='Sigarra Python API based on Recursive Web Scraping Parser (wtf)',
      url='https://github.com/msramalho/sigpy',
      author='msramalho',
      license='MIT',
      packages=['sigpy'],
      install_requires=required,
      zip_safe=False)
