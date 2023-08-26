from setuptools import setup, find_packages

setup(name='openness',
      version='0.1',
      description='app',
      url='https://github.com/Ari-maker/tiaportal-app',
      author='Ari Tenhunen',
      author_email='ari.tenhunen@siemens.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'clr-loader',
          'Flask',
          'flaskwebgui',
          'pythonnet',
          'requests',
          'et-xmlfile'
      ],
      zip_safe=False)