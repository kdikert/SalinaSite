
import markdown

from django import template
from django.template import Node
from django.template.defaulttags import url
from django.template.base import TemplateSyntaxError
from django.utils import translation
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.safestring import mark_safe

from salina.models import CMSText

register = template.Library()


class CMSTextNode(Node):
    
    ALERT_BOX = '<div style="color: red; font-weight: bold;">&lt;%s&gt;</div>'
    
    def __init__(self, text_id):
        super(CMSTextNode, self).__init__()
        
        self.text_id = text_id
        self.text = None
        
        self.escape_output = False
        
        try:
            current_language = translation.get_language()
            cms_text = CMSText.objects.get(entry_id=self.text_id)
            
            transl = cms_text.get_translation_entry(current_language)
            if transl:
                self.text = transl.text
            else:
                self.text = CMSTextNode.ALERT_BOX % ('missing translation "%s" (%s)' % (self.text_id, current_language))
            
        except CMSText.DoesNotExist:
            self.text = CMSTextNode.ALERT_BOX % ('invalid text "%s"' % self.text_id)
    
    def render(self, context):
        value = force_unicode(self.text)
        
        if self.escape_output:
            value = escape(value)
        value = markdown.markdown(value)
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
                url_result = url_result[:-1]
            
            if self.full_match:
                if path == url_result:
                    return self.text
            else:
                if path.startswith(url_result):
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

