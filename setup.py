import codecs

setup(name='googleappsauth',
      maintainer='Maximillian Dornseif',
      maintainer_email='md@hudora.de',
      version='1.0',
      description='googleappsauth authenticates Django Users against a Google Apps Domain',
      long_description=codecs.open('README.markdown', "r", "utf-8").read()
      license='BSD',
      classifiers=['Intended Audience :: Developers',
                   'Programming Language :: Python'],
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
