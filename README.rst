Introduction
============

collective.geo.file provides a view for KML, KMZ (Keyhole Markup Language)
and GPX (GPS eXchange Format) files.
The view renders the file in a openlayers Map using the collective.geo
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
collections and Folders





Known Issues
============

If you assign coordinates to the file with the IGeoreferenceable Interface
you have to set the viewletmanager to 'Do not display map' otherwise
it will **REALLY** screw up your view. The coordinates assigned there
will display as the first layer on the 'Map View' of the file and
they will display in the 'KML File Map View' of a topic.
