#
import logging

from Products.CMFCore.utils import getToolByName
from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.maplayers import MapLayer
from collective.geo.kml.browser.kmlopenlayersview import KMLMapLayers
from collective.geo.contentlocations.interfaces import IGeoManager
from collective.geo.file.interfaces import IGisFile
from collective.geo.file.config import MIMETYPES

try:
    from plone.app.querystring import queryparser
except ImportError:
    pass

logger = logging.getLogger('collective.geo.file')

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
        style_str =u''
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
            #style_str ='style: {strokeColor: "green", strokeWidth: 2, strokeOpacity: 0.5},'
        if format_str:
            layer_str = u"""function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s",
                      format: %s
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    %s
                    %s
                    projection: new OpenLayers.Projection("EPSG:4326")
                  });
                }""" % (self.kmlfile.Title().replace("'", "&apos;"),
                            context_url, format_str, style_str, load_end)
        else:
            layer_str = ''
        return layer_str






class KMLFileMapLayers(KMLMapLayers):
    '''
    create all layers for this view.
    the file itself as a layer +
    the layer defined by the annotations (if any)
    '''

    def layers(self):
        layers = super(KMLFileMapLayers, self).layers()
        layers.append(KMLFileMapLayer(self.context,self.context, zoom_here=True))
        return layers

class KMLFileTopicMapLayers(KMLMapLayers):
    '''
    create all layers for this view.
    the layer defined by the annotations +
    all kml files as layers
    '''
    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def layers(self):
        layers = super(KMLFileTopicMapLayers, self).layers()
        lcount = len(layers)
        query = {'object_provides': IGisFile.__identifier__}
        #XXX
        if self.context.portal_type == 'Folder':
            brains = self.context.getFolderContents(contentFilter=query)
        elif self.context.portal_type == 'Collection':
            query.update(queryparser.parseFormquery(
                self.context, self.context.getRawQuery()))
            brains=self.portal_catalog(**query)
        elif self.context.portal_type == 'Topic':
            query.update(self.context.buildQuery())
            brains=self.portal_catalog(**query)
        else:
            brains = []
            logger.error('cannot get query for current object')
        for brain in brains:
            object = brain.getObject()
            if object.content_type in MIMETYPES:
                layers.append(KMLFileMapLayer(self.context,
                                object, zoom_here=False))
        if len(layers) > lcount:
            layers[-1].zoom_here = True
        return layers
