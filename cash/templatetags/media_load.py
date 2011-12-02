from django import template
from django.template import Node, Template, Context
from django.conf import settings

register = template.Library()

class MediaNode(Node):
    def __init__(self, line):
        self.line = line
            
    def render(self, context):
        return self.line
    
def loadMedia(parser, token):
    bits = token.contents.split('"')
    line = '<link rel="stylesheet" href="%s%s"/>' % (settings.MEDIA_URL,bits[1])
    return MediaNode(line)
loadMedia = register.tag(loadMedia)

def loadStyle(parser, token):
    bits = token.contents.split('"')
    line = '<link rel="stylesheet" href="%s%s"/>' % (settings.MEDIA_URL + "css/",bits[1])
    return MediaNode(line)

loadStyle = register.tag(loadStyle)

def loadExtStyle(parser, token):
    bits = token.contents.split('"')
    line = '<link rel="stylesheet" href="%s%s"/>' % (settings.MEDIA_URL + settings.EXT_LOCATION + 'resources/css/',bits[1])
    return MediaNode(line)

loadExtStyle = register.tag(loadExtStyle)

def loadUxStyle(parser, token):
    bits = token.contents.split('"')
    line = '<link rel="stylesheet" href="%s%s"/>' % (settings.MEDIA_URL + settings.UX_LOCATION + 'css/',bits[1])
    return MediaNode(line)

loadUxStyle = register.tag(loadUxStyle)

def loadScript(parser, token):
    bits = token.contents.split('"')
    line = '<script type="text/javascript" src="%s%s"></script>' % (settings.MEDIA_URL,bits[1])
    return MediaNode(line)    

loadScript = register.tag(loadScript)

def loadExtUx(parser, token):
    bits = token.contents.split('"')
    line = '<script type="text/javascript" src="%(url)s%(location)s%(file)s.js"></script>' % {'url':settings.MEDIA_URL,'location': settings.UX_LOCATION,'file':bits[1]}
    return MediaNode(line)    

loadExtUx = register.tag(loadExtUx)

def addExt(parser, token):
    str = ""
    for file in settings.EXT_FILES:
        str += '<script type="text/javascript" src="%s%s"></script>\n' % (settings.MEDIA_URL,file)
    return MediaNode(str) 

addExt = register.tag(addExt)