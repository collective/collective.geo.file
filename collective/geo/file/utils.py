from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from collective.geo.file.interfaces import IGisFile

def set_mapview(context, event):
    mimetype = context.content_type
    reindex = False
    if mimetype in ['application/vnd.google-earth.kml+xml',
                    'application/vnd.google-earth.kmz',
                    'application/gpx+xml']:
        if not IGisFile.providedBy(context):
            alsoProvides(context, IGisFile)
            reindex = True
        if 'filekml_view' in [l[0] for l in context.getAvailableLayouts()]:
            context.setLayout('filekml_view')
    else:
        if IGisFile.providedBy(context):
            noLongerProvides(context, IGisFile)
            reindex = True
        # reset to default view
        context.setLayout(context.getDefaultLayout())

    # we need to reindex the object, because ObjectEditedEvent is fired
    # after reindexing
    if reindex:
        context.reindexObject()
