from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag(takes_context=True)
def page_url_with_filters(context, page):
    dic = QueryDict(mutable=True)
    dic.update({'page': page})

    if context.get('applied_filters').get('enabled', False):
        dic.setlist('filter', context['applied_filters'].keys())

    if context.get('feed_type') is not None:
        dic.setlist('feed_type', context['feed_type'])
    return '?' + dic.urlencode()


@register.simple_tag(takes_context=True)
def provide_filters_qs(context):
    dic = QueryDict(mutable=True)
    if context.get('applied_filters').get('enabled', False):
        dic.setlist('filter', context['applied_filters'].keys())

    if context.get('feed_type') is not None:
        dic.setlist('feed_type', [context['feed_type']])

    return '?' + dic.urlencode()
