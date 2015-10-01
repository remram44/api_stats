import io
import os
from setuptools import setup


# pip workaround
os.chdir(os.path.abspath(os.path.dirname(__file__)))


with io.open('README.rst', encoding='utf-8') as fp:
    description = fp.read()

setup(name='api_stats',
      version='0.3',
      packages=['api_stats'],
      entry_points={'console_scripts': [
          'api_stats = api_stats:main']},
      description="Record historical statistics from an API that only offers "
                  "current numbers.",
      install_requires=['requests'],
      author="Remi Rampin",
      author_email='remirampin@gmail.com',
      maintainer="Remi Rampin",
      maintainer_email='remirampin@gmail.com',
      url='https://github.com/remram44/api_stats',
      long_description=description,
      license='BSD',
      keywords=['api', 'log', 'record', 'stats', 'statistics', 'graph'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Topic :: Internet',
          'Topic :: Utilities'])
