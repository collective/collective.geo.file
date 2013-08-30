from setuptools import setup, find_packages
import os

version = '0.6'

setup(name='collective.geo.file',
      version=version,
      description="An openlayers view for KML, KMZ and GPX files",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: GIS",
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='GIS KML KMZ Openlayers GPX',
      author='Christian Ledermann',
      author_email='christian.ledermann@gmail.com',
      url='http://plone.org/products/collective.geo.file/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.geo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.geo.kml',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      #setup_requires=["PasteScript"],
      #paster_plugins=["ZopeSkel"],
      )
