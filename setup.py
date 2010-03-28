import codecs
from setuptools import setup, find_packages

setup(name='googleappsauth',
      maintainer='Maximillian Dornseif',
      maintainer_email='md@hudora.de',
      version='1.01p4',
      description='googleappsauth authenticates Django Users against a Google Apps Domain',
      long_description=codecs.open('README.rst', "r", "utf-8").read(),
      license='BSD',
      url='http://github.com/hudora/django-googleappsauth',
      classifiers=['Intended Audience :: Developers',
                   'Programming Language :: Python'],
      packages = find_packages(),
      package_data = {
          # If any package contains *.txt or *.rst files, include them:
          #'': ['*.xml', '*.jrxml', '*.jar', '*.py', '*.sh'],
          #backend/lib/
          #backend/webapps/
      },
      install_requires = ['Django'],
      zip_safe = False,
)
