from django.utils.http import urlencode
from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def query_param_replace(context, **kwargs):
    query = context['request'].GET.copy()
    for query_key, query_value in kwargs.items():
        query[query_key] = query_value

    for query_key, query_value in query.items():
        if not query_value:
            del query[query_key]

    return query.urlencode()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
