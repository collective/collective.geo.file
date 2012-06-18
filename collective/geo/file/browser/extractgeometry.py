import logging
from zope import interface, schema
from zope.formlib import form
from zope.app.form.browser import RadioWidget
from five.formlib import formbase
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from elementtree.ElementTree import XML

from Products.statusmessages.interfaces import IStatusMessage
from shapely.geometry import Point, LineString, Polygon
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon

from collective.geo.contentlocations.interfaces import IGeoManager

from collective.geo.file import fileMessageFactory as _


logger = logging.getLogger('collective.geo.file')

def extractfeatures_from_file(data):
    kmldom = XML(data)
    ns = kmldom.tag.strip('kml')
    points = kmldom.findall('.//%sPoint' % ns)
    lines = kmldom.findall('.//%sLineString' % ns)
    polygons = kmldom.findall('.//%sPolygon' % ns)
    mpoint = []
    mline =[]
    mpoly = []
    for point in points:
        coordinates = point.findall('.//%scoordinates' % ns)
        for coordinate in coordinates:
            latlon = coordinate.text.strip().split(',')
            coords = [float(c) for c in latlon]
            try:
                p = Point(coords)
                mpoint.append(p)
            except:
                logger.info('invalid point geometry: %s' % coordinates[:10] )

    for line in lines:
        coordinates = line.findall('.//%scoordinates' % ns)
        for coordinate in coordinates:
            latlons = coordinate.text.split()
            coords = []
            for latlon in latlons:
                coords.append([float(c) for c in latlon.split(',')])
            try:
                l = LineString(coords)
                mline.append(l)
            except:
                logger.info('invalid linestring geometry: %s' % coordinates[:10] )

    for polygon in polygons:
        coordinates = polygon.findall('.//%scoordinates' % ns)
        for coordinate in coordinates:
            latlons = coordinate.text.split()
            coords = []
            for latlon in latlons:
                coords.append([float(c) for c in latlon.split(',')])
            try:
                l = Polygon(coords)
                mpoly.append(l)

            except:
                logger.info('invalid polygon geometry: %s' % coordinates[:10] )

    result = {'MultiPoint':None, 'MultiLineString':None, 'MultiPolygon':None}
    if mpoint:
        result['MultiPoint'] =  MultiPoint(mpoint)
    if mline:
        result['MultiLineString'] = MultiLineString(mline)
    if mpoly:
        result['MultiPolygon'] = MultiPolygon(mpoly)


    return result



class IExtractGeometrySchema(interface.Interface):
    # -*- extra stuff goes here -*-

    simplify = schema.Bool(
        title=u'Simplify',
        description=u'Simplify Geometry',
        required=False,
        readonly=False,
        default=False,
        missing_value=False,
        )

    simplifyvalue = schema.Float(
        title=u'Simplify by',
        description=u'A simplified representation of the geometric object',
        required=False,
        readonly=False,
        default=0.2,
        min = 0.0,
        )


    #form.widget(extractfeature=RadioWidget)
    extractfeature = schema.Choice(
        title=_(u'Extract features'),
        description=_(u'Extract Features of type'),
        required=True,
        readonly=False,
        default=4,
        vocabulary=SimpleVocabulary((
            SimpleTerm(value=1, token='Point', title=_(u'Point')),
            SimpleTerm(value=2, token='LineString', title=_(u'LineString')),
            SimpleTerm(value=3, token='Polygon', title=_(u'Polygon')),
            SimpleTerm(value=4, token='Envelope', title=_(u'Envelope')),
            SimpleTerm(value=5, token='ConvexHull', title=_(u'Convex Hull'))
            ))
        )


class ExtractGeometry(formbase.PageForm):
    form_fields = form.FormFields(IExtractGeometrySchema)
    label = _(u'Extract the geometry from the file')
    description = _(u'Extract the geometry from the File and set it as annotations')

    @property
    def next_url(self):
        url = self.context.absolute_url()
        url += '/view'

        return url

    def simplify(self, geom, tolerance, go):
        if go:
            return geom.simplify(tolerance)
        else:
            return geom

    @form.action('Submit')
    def actionSubmit(self, action, data):
        geo = IGeoManager(self.context)
        url = self.context.absolute_url()
        if data.get('extractfeature'):
            features = extractfeatures_from_file(self.context.get_data())
            if data['extractfeature'] == 1:
                if features['MultiPoint']:
                    geom = self.simplify(features['MultiPoint'],
                        data['simplifyvalue'], data['simplify'])
                    q = geom.__geo_interface__
                    geo.setCoordinates(q['type'], q['coordinates'])

            elif data['extractfeature'] == 2:
                if features['MultiLineString']:
                    geom = self.simplify(features['MultiLineString'],
                                data['simplifyvalue'], data['simplify'])
                    q = geom.__geo_interface__
                    geo.setCoordinates(q['type'], q['coordinates'])

            elif data['extractfeature'] == 3:
                if features['MultiPolygon']:
                    geom = self.simplify(features['MultiPolygon'],
                                data['simplifyvalue'], data['simplify'])
                    q = geom.__geo_interface__
                    geo.setCoordinates(q['type'], q['coordinates'])
            elif data['extractfeature'] == 4:
                if (features['MultiPoint'] or
                features['MultiLineString'] or
                features['MultiPolygon']):
                    geoms =[]
                    if features['MultiPoint']:
                        geoms.append(features['MultiPoint'].envelope)
                    if features['MultiLineString']:
                        geoms.append(features['MultiLineString'].envelope)
                    if features['MultiPolygon']:
                        geoms.append(features['MultiPolygon'].envelope)
                    q = MultiPolygon(geoms).envelope.__geo_interface__
                    geo.setCoordinates(q['type'], q['coordinates'])
            elif data['extractfeature'] == 5:
                if (features['MultiPoint'] or
                features['MultiLineString'] or
                features['MultiPolygon']):
                    geoms =[]
                    if features['MultiPoint']:
                        geoms.append(features['MultiPoint'].convex_hull)
                    if features['MultiLineString']:
                        geoms.append(features['MultiLineString'].convex_hull)
                    if features['MultiPolygon']:
                        geoms.append(features['MultiPolygon'].convex_hull)
                    geom = self.simplify(MultiPolygon(geoms).convex_hull,
                                data['simplifyvalue'], data['simplify'])
                    q = geom.__geo_interface__
                    geo.setCoordinates(q['type'], q['coordinates'])

            self.request.response.redirect(self.context.absolute_url() +
                                            '/@@manage-coordinates')

    @form.action('Cancel')
    def actionCancel(self, action, data):
        self.request.response.redirect(self.next_url)



