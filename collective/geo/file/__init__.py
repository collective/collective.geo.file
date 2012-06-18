  # -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory

fileMessageFactory = MessageFactory('collective.geo.file')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
