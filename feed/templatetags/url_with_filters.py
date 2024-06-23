from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag(takes_context=True)
def page_url_with_filters(context, page):
    dic = QueryDict(mutable=True)
    dic.update({'page': page})
    print()
    if context.get('applied_filters').get('enabled', False):
        dic.setlist('filter', context['applied_filters'].keys())
    return '?' + dic.urlencode()
