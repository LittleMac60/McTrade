from django.shortcuts import render
from common.tools.scan import run_scan
from django.core.paginator import Paginator
from common.models import search_results
from common.tools.filters import search_results_filter_scan_1, has_filters_applied  
from common.tools.general import clean_querystring, sort_key 


def home(request):
    return render(request, 'common/base.html')


def au_mom_dashboard(request):
    queryset = search_results.objects.all()
    stock_filter = search_results_filter_scan_1(request.GET, queryset=queryset)

    sort_by = request.GET.get('sort', 'symbol_name')
    direction = request.GET.get('direction', 'asc')
    if direction == 'desc':
        sort_by = f'-{sort_by}'

    sorted_qs = stock_filter.qs.order_by(sort_by)

    momentum_table = []
    if has_filters_applied(request):
        filtered_tickers = sorted_qs.values_list('igsymbol', flat=True)
        tickers = [f"{symbol}" for symbol in filtered_tickers]
        momentum_table = run_scan(tickers)

    paginator = Paginator(momentum_table, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    querydict = request.GET.copy()
    querydict.pop('page', None)
    querystring = querydict.urlencode()

    return render(request, 'common/mom_dashboard.html', {
        'filter': stock_filter,
        'page_obj': page_obj,
        'querystring': querystring,
        'current_sort': request.GET.get('sort', ''),
        'current_dir': request.GET.get('direction', ''),
        'filters_applied': has_filters_applied(request),
    })

