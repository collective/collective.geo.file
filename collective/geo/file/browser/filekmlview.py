from zope.interface import implements, Interface

from Products.Five import BrowserView

class IFileKmlView(Interface):
    """
    File Kml view interface
    """

class FileKmlView(BrowserView):
    """
    browser view to display a map for a kml file
    """
    implements(IFileKmlView)


class ITopicFileKmlView(Interface):
    """
    Interface for TopicFileKmlView
    """

class TopicFileKmlView(BrowserView):
    """
    displays kml files in the results of the topic
    as layers in the map
    """
    implements(ITopicFileKmlView)
