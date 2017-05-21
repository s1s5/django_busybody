# coding: utf-8
from urlparse import urlparse
from urlparse import urlunparse
from django.http import QueryDict
from django.template import Library

register = Library()


@register.simple_tag
def replace_query_param(url, attr, val):
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    query_dict = QueryDict(query).copy()
    query_dict[attr] = val
    query = query_dict.urlencode()
    return urlunparse((scheme, netloc, path, params, query, fragment))
