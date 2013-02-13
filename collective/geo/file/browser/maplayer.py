#
from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.maplayers import MapLayer
from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.file.interfaces import IGisFile
from collective.geo.file.config import MIMETYPES


def is_georeferenced(context):
    try:
        geo = IGeoManager(context)
        if geo.isGeoreferenceable():
            if geo.getCoordinates()[0]:
                return True
    except TypeError:
        # catch TypeError: ('Could not adapt', <ATFile ...>, <Interfa...oManager>)
        pass
    return False

class KMLMapLayer(MapLayer):
    """
    a layer for one level sub objects.
    """

    def __init__(self, context):
        self.context = context

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'
        if is_georeferenced(self.context):
            load_end = u"""
              eventListeners: { 'loadend': function(event) {
                                 var extent = this.getDataExtent()
                                 this.map.zoomToExtent(extent);
                                }
                            },
            """
        else:
            load_end = ""
        #XXX FIXME
        load_end = ""
        return u"""
        function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@kml-document",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true}),
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    visibility: true,
                    %s
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                } """ % (self.context.Title().replace("'", "&apos;"),
                        context_url, load_end)





class KMLFileMapLayer(MapLayer):
    """
    a layer for a KML/KMZ/GPX File.
    """

    def __init__(self, context, kmlfile, zoom_here=False):
        self.context = context
        self.kmlfile = kmlfile
        self.zoom_here = zoom_here

    @property
    def jsfactory(self):
        context_url = self.kmlfile.absolute_url()
        mimetype = self.kmlfile.content_type
        if not context_url.endswith('/'):
            context_url += '/'
        format_str = ''
        if not (is_georeferenced(self.kmlfile)
            and (self.context == self.kmlfile
            or self.zoom_here)):
            load_end = u"""
              eventListeners: { 'loadend': function(event) {
                                 var extent = this.getDataExtent()
                                 this.map.zoomToExtent(extent);
                                }
                            },
            """
        else:
            load_end = ""

        #XXX we have to find smthng better for this
        #load_end = u''

        if mimetype == 'application/vnd.google-earth.kml+xml':
            format_str = u"""new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})"""
        elif mimetype == 'application/vnd.google-earth.kmz':
            format_str = u"""new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})"""
            context_url += '@@filekmz_view.kml'
        elif mimetype == 'application/gpx+xml':
            format_str = u"""new OpenLayers.Format.GPX({
                                    extractWaypoints: true,
                                    extractRoutes: true,
                                    extractAttributes: true})"""
        if format_str:
            layer_str = u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s",
                      format: %s
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    %s
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (self.kmlfile.Title().replace("'", "&apos;"),
                            context_url, format_str, load_end)
        else:
            layer_str = ''
        return layer_str






class KMLFileMapLayers(MapLayers):
    '''
    create all layers for this view.
    the file itself as a layer +
    the layer defined by the annotations (if any)
    '''

    def layers(self):
        layers = super(KMLFileMapLayers, self).layers()
        if is_georeferenced(self.context):
            layers.append(KMLMapLayer(self.context))
        layers.append(KMLFileMapLayer(self.context,self.context, zoom_here=True))
        return layers

class KMLFileTopicMapLayers(MapLayers):
    '''
    create all layers for this view.
    the layer defined by the annotations +
    all kml files as layers
    '''


    def layers(self):
        layers = super(KMLFileTopicMapLayers, self).layers()
        layers.append(KMLMapLayer(self.context))
        query = {'object_provides': IGisFile.__identifier__}
        for brain in self.context.queryCatalog(**query):
            object = brain.getObject()
            if object.content_type in MIMETYPES:
                layers.append(KMLFileMapLayer(self.context,object))
        if layers:
            layers[-1].zoom_here = True
        return layers
