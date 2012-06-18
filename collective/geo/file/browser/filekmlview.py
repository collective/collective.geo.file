import tempfile
import zipfile
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


class IKmzFileKmlView(Interface):
    """
    File Kmz view interface
    """

class KmzFileKmlView(BrowserView):
    """
    browser view to display a kml for a kmz file
    """
    implements(IKmzFileKmlView)

    def __call__(self):
        self.request.RESPONSE.setHeader('Content-Type',
            'application/vnd.google-earth.kml+xml; charset=utf-8')
        tmp = tempfile.NamedTemporaryFile()
        tmp.file.write(self.context.data)
        tmp.file.flush()
        text = u''
        if zipfile.is_zipfile(tmp.name):
            tmpzip = zipfile.ZipFile(tmp.file)
            for zi in tmpzip.infolist():
                if zi.filename.endswith('.kml'):
                    tz = tmpzip.open(zi)
                    id = tz.name
                    text = tz.read().decode('utf-8', 'replace')
                    tz.close()
                    break
        tmp.close()
        return text


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
