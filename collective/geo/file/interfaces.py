"""Define interfaces for your add-on.
"""
from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface
from collective.geo.kml.interfaces import IGeoKmlLayer

class IGeoFileLayer(IGeoKmlLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """

class IGisFile(Interface):
    """ Marker interface for files containing GIS data.
    Should just be used in the browser page definition!!! """


