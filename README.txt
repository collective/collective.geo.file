Introduction
============

    collective.geo.file provides a view for KML (Keyhole Markup Language)
    and GPX (GPS eXchange Format) files.
    The view renders the file in a openlayers Map using the collective.geo
    library.

    The product does not introduce a content type but adds an additional
    view to the Archetypes file and collection type.

    When you upload a KML file with the
    correct mimetype 'application/vnd.google-earth.kml+xml' (i.e with
    the extension *.kml) or 'application/gpx+xml' (i.e. with the extension
    *.gpx) the map view will be applied by default.

    For Collections an additional view is added that displays all KML and GPX files
    returned by the query as a layer. Choose 'KML File Map View' from the
    display menue of the topic.




Known Issues
============

    If you assign coordinates to the file with the IGeoreferenceable Interface
    you have to set the viewletmanager to 'Do not display map' otherwise
    it will _REALLY_ screw up your view. The coordinates assigned there
    will display as the first layer on the 'Map View' of the file and
    they will display in the 'KML File Map View' of a topic.
