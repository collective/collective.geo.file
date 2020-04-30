Introduction
============

collective.geo.file provides a view for KML, KMZ (Keyhole Markup Language)
and GPX (GPS eXchange Format) files.
The view renders the file in a `openlayers`_ Map using the collective.geo
library.

The product does not introduce a content type but adds an additional
view to the Archetypes file and collection type.

When you upload a file with the
correct mimetype 'application/vnd.google-earth.kml+xml' (i.e with
the extension `*.kml`), 'application/vnd.google-earth.kmz' (extension
`*.kmz`)
or 'application/gpx+xml' (i.e. with the extension
`*.gpx`) the map view will be applied by default.

KML, KMZ and GPX files are displayed in the `KML Openlayers View` of
collections and Folders.


Documentation
=============

Full documentation for end users can be found in the "docs" folder.
It is also available online at https://collectivegeo.readthedocs.io/


Translations
============

This product has been translated into

- Spanish.

You can contribute for any message missing or other new languages, join us at 
`Plone Collective Team <https://www.transifex.com/plone/plone-collective/>`_ 
into *Transifex.net* service with all world Plone translators community.


Known Issues
============

If you assign coordinates to the file with the IGeoreferenceable Interface
you have to set the `viewletmanager`_ to 'Do not display map' otherwise
it will **REALLY** screw up your view. The coordinates assigned there
will display as the first layer on the 'Map View' of the file and
they will display in the 'KML File Map View' of a topic.


Tests status
============

This add-on is tested using Travis CI. The current status of the add-on is:

.. image:: https://img.shields.io/travis/collective/collective.geo.file/master.svg
    :target: https://travis-ci.org/collective/collective.geo.file

.. image:: http://img.shields.io/pypi/v/collective.geo.file.svg
   :target: https://pypi.org/project/collective.geo.file


Contribute
==========

Have an idea? Found a bug? Let us know by `opening a ticket`_.

- Issue Tracker: https://github.com/collective/collective.geo.file/issues
- Source Code: https://github.com/collective/collective.geo.file
- Documentation: https://collectivegeo.readthedocs.io/


License
=======

The project is licensed under the GPLv2.

.. _`openlayers`: https://openlayers.org/
.. _`viewletmanager`: https://docs.plone.org/develop/plone/views/viewlets.html
.. _`opening a ticket`: https://github.com/collective/collective.geo.bundle/issues
