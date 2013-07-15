import logging
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite
from zope.interface import alsoProvides
from Products.CMFPlone.utils import getToolByName
from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem
from collective.geo.file.interfaces import IGisFile
# The profile id of your package:
PROFILE_ID = 'profile-collective.geo.file:default'

from config import MIMETYPES

GIS_MIMETYPES = [
    {'name': 'application/vnd.google-earth.kml+xml',
    'extensions': ('kml',),
    'globs': ('*.kml',),
    'icon_path': 'text.png',
    'binary': True,
    'mimetypes': ('application/vnd.google-earth.kml+xml',)},
    {'name': 'application/vnd.google-earth.kmz',
    'extensions': ('kmz',),
    'globs': ('*.kmz',),
    'icon_path': 'text.png',
    'binary': True,
    'mimetypes': ('application/vnd.google-earth.kmz',)},
    {'name': 'application/gpx+xml',
    'extensions': ('gpx',),
    'globs': ('*.gpx',),
    'icon_path': 'text.png',
    'binary': True,
    'mimetypes': ('application/gpx+xml',)}
]




def do_nothing(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.geo.file')
    logger.info("Empty upgrade step")

def attach_igisfile(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.geo.file')
    logger.info('attaching IGisFile to KML, KMZ and GPS Files')
    portal = getSite()
    catalog = getToolByName(portal, 'portal_catalog')
    brains = catalog(portal_type='File')
    reindex = False
    for brain in brains:
        ob = brain.getObject()
        mimetype = ob.content_type
        if mimetype in MIMETYPES:
            if not IGisFile.providedBy(ob):
                alsoProvides(ob, IGisFile)
                reindex = True
    if reindex:
        logger.info('rebuilding object_provides catalog index')
        catalog.manage_reindexIndex(ids=['object_provides',])

def add_extract_menue(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.geo.file')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'actions')
    logger.info('adding extract coordinates menu')

def add_mimetypes(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.geo.file')
    portal = getSite()
    mimetypes_registry = getToolByName(portal, 'mimetypes_registry')
    all_mimetypes = mimetypes_registry.list_mimetypes()

    for mtype in GIS_MIMETYPES:
        if mtype['name'] not in all_mimetypes:
            logger.info('Registering mimetype %s' % mtype['name'])
            mimetypes_registry.register(MimeTypeItem(**mtype))

def import_various(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Only run step if a flag file is present
    if context.readDataFile('collective.geo.file-default.txt') is None:
        return
    logger = context.getLogger('collective.geo.file')
    add_mimetypes(context, logger)
    attach_igisfile(context, logger)

