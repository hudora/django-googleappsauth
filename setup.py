from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name='hudoratools',
      maintainer='Maximillian Dornseif',
      maintainer_email='md@hudora.de',
      version='0.25',
      url='https://cybernetics.hudora.biz/nonpublic/eggs/',
      description='hudoratools',
      long_description="Django support tools for internal use at HUDORA.",
      license='BSD',
      #classifiers=['Intended Audience :: Developers',
      #             'Programming Language :: Python'],
      
      packages = find_packages(),
      package_data = {
          # If any package contains *.txt or *.rst files, include them:
          #'': ['*.xml', '*.jrxml', '*.jar', '*.py', '*.sh'],
          #backend/lib/
          #backend/webapps/
      },
      install_requires = [],
      zip_safe = False,
)
