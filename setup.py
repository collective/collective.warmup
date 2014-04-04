from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.warmup',
      version=version,
      description="Collective Warmup",
      long_description=(
          open("README.rst").read() + "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read()
      ),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
      ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'lxml'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      warmup = collective.warmup.commands:warmup

      [z3c.autoinclude.plugin]
      target = plone
      """
      )
