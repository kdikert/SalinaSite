
from django import template
from django.template import Node
from django.template.defaulttags import url
from django.template.base import TemplateSyntaxError
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.safestring import mark_safe

from salina.models import CMSText

register = template.Library()


class CMSTextNode(Node):
    
    def __init__(self, text_id):
        super(CMSTextNode, self).__init__()
        self.text_id = text_id
        try:
            self.text_object = CMSText.objects.get(text_id=self.text_id)
        except CMSText.DoesNotExist:
            raise TemplateSyntaxError('Text with ID "%s" does not exist' % text_id)
            pass
    
    def render(self, context):
        value = self.text_object.text
        value = force_unicode(value)
        value = escape(value)
        return mark_safe(value)


@register.tag
def cms_text(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' takes text id as argument" % bits[0])
    text_id = bits[1]
    return CMSTextNode(text_id)


class UrlMatchTextNode(Node):
    
    def __init__(self, url_node, text, full_match):
        super(UrlMatchTextNode, self).__init__()
        self.text = text
        self.url_node = url_node
        self.full_match = full_match
    
    def render(self, context):
        url_result = self.url_node.render(context)
        if url_result:
            request = context.get('request')
            path = request.path
            
            # Remove possible query string parameters
            path = path.split('?')[0]
            
            # Normalize the paths by removing trailing slashes
            if len(path) > 1 and path.endswith("/"):
                path = path[:-1]
            if len(url_result) > 1 and url_result.endswith("/"):
                url_result = path[:-1]
            
            if self.full_match:
                if url_result == request.path:
                    return self.text
            else:
                if request.path.startswith(url_result):
                    return self.text
        
        return ''


@register.tag
def url_equals(parser, token):
    url_node = url(parser, token)
    return UrlMatchTextNode(url_node, "selectedLink", full_match=True)

@register.tag
def url_startswith(parser, token):
    url_node = url(parser, token)
    return UrlMatchTextNode(url_node, "selectedLink", full_match=False)

