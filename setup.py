import codecs
from setuptools import setup, find_packages

setup(name='googleappsauth',
      maintainer='Maximillian Dornseif',
      maintainer_email='md@hudora.de',
      version='1.02',
      description='googleappsauth authenticates Django Users against a Google Apps Domain',
      long_description=codecs.open('README.rst', "r", "utf-8").read(),
      license='BSD',
      url='http://github.com/hudora/django-googleappsauth#readme',
      classifiers=['Intended Audience :: Developers',
                   'Programming Language :: Python'],
      packages = find_packages(),
      install_requires = ['Django'],
      zip_safe = False,
)
