from django import template
from django.template import resolve_variable
import re

register = template.Library()

def html_euro(value):
    "Formats a value with two decimal digits and andds an Euro sign in HTML entity notation"

    try:
        value = float(value)
    except ValueError:
        return value
    return "%.2f&nbsp;&euro;" % (value)
register.filter(html_euro)


class FieldAndErrorInfoNode(template.Node):
    def __init__(self, field):
        self.field = field

    def render(self, context):
        field = resolve_variable(self.field, context)
        ret = str(field)
        if not field.errors():
            return ret
        #return "*** " + (", ".join([str(x) for x in field.errors()]))
        return '<div class="error">%s %s</div>' % (ret, field.html_error_list())

def do_field_and_error_info(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, field = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents[0]
    return FieldAndErrorInfoNode(field)
register.tag('field_and_error_info', do_field_and_error_info)
