from urllib.parse import urlencode
from django.http import HttpResponse
import csv

def clean_querystring(request, exclude_keys=None):
    exclude_keys = exclude_keys or []
    querydict = request.GET.copy()
    for key in exclude_keys:
        querydict.pop(key, None)
    return urlencode(querydict)


def sort_key(val):
    if val == "1":
        return 1
    return -1  # Treat blanks as lowest value for sorting


def has_filters_applied(request):
    ignored_keys = {'page', 'sort', 'direction'}
    return any(k for k in request.GET if k not in ignored_keys and request.GET.get(k))


def export_to_csv(data):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="momentum_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Ticker', 'Golden Cross', 'Death Cross', 'MACD Bullish', 'RSI', 'Near 52w High'])

    for row in data:
        writer.writerow(row)

    return response