from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def sort_link(field, request_get):
    query = request_get.copy()
    current_sort = query.get('sort')
    current_direction = query.get('direction', 'asc')

    if current_sort == field:
        query['direction'] = 'desc' if current_direction == 'asc' else 'asc'
    else:
        query['sort'] = field
        query['direction'] = 'asc'

    return '?' + urlencode(query, doseq=True)
