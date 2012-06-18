    collective.geo.file provides a view for KML files (Keyhole Markup Language)
    and collections.
    The view renders the file (or files returned by the collection) in a
    openlayers Map using the collective.geo library.

    The product does not introduce a content type but adds an additional
    view to the Archetypes file and collection type.

    When you upload a KML file with the
    correct mimetype 'application/vnd.google-earth.kml+xml' the map view
    will be applied by default. When the mimetype detected by plone is
    something else (like 'text/xml') you have to choose 'Map view' manually
    in the display menue of the file.

    For Collections an additional view is added that displays all KML files
    returned by the query as layers. Choose 'KML File Map View' from the
    display menue of the topic.
