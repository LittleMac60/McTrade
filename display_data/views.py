from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import Coalesce
import csv
import pandas as pd

from common.models import search_results
from common.tools.filters import search_results_filter_scan_1   
from common.tools.general import clean_querystring, export_to_csv, has_filters_applied
from common.tools.forms import SearchResultsForm  


def home(request):
    return render(request, 'common/base.html')


def stock_list(request):
    queryset = search_results.objects.all()
    stock_filter = search_results_filter_scan_1(request.GET, queryset=queryset)

    sort_by = request.GET.get('sort', 'symbol_name')
    direction = request.GET.get('direction', 'asc')

    if direction == 'desc':
        sort_by = f'-{sort_by}'

    sorted_qs = stock_filter.qs.order_by(sort_by)

    paginator = Paginator(sorted_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    querydict = request.GET.copy()
    querydict.pop('page', None)
    querystring = querydict.urlencode()

    return render(request, 'common/stock_list.html', {
        'filter': stock_filter,
        'page_obj': page_obj,
        'querystring': querystring,
        'current_sort': request.GET.get('sort', ''),
        'current_dir': request.GET.get('direction', ''),
    })


def stock_pivot_view(request):
    queryset = search_results.objects.all()
    stock_filter = search_results_filter_scan_1(request.GET, queryset=queryset)
    stock_filter_qs = stock_filter.qs

    fields = ['igsymbol', 'scan_name', 'scan_result']
    df = pd.DataFrame.from_records(stock_filter_qs.values(*fields))
    
    if df.empty:
        pivot_df = pd.DataFrame(columns=['igsymbol'])  # or whatever minimal structure you need
        page_obj = Paginator([], 25).get_page(1)
    else:

        pivot_df = pd.pivot_table(
            df,
            index='igsymbol',
            columns='scan_name',
            values='scan_result',
            aggfunc='sum',
            fill_value='',
            margins=True,
            margins_name='Total'
        ).reset_index()

    sort_by = request.GET.get("sort_by")
    sort_order = request.GET.get("sort_order", "asc")

    if sort_by in pivot_df.columns:
        ascending = sort_order == "asc"

        # Sample values to detect type
        sample_values = pivot_df[sort_by].dropna().astype(str).unique()

        def is_binary_column(values):
            return all(v.strip() in ["", "1"] for v in values)

        def is_numeric_column(values):
            return all(v.strip().replace('.', '', 1).isdigit() for v in values if v.strip() != "")

        if is_binary_column(sample_values):
            # Binary column: "1" or blank
            pivot_df["_sort_key"] = pivot_df[sort_by].apply(lambda x: 1 if str(x).strip() == "1" else -1)
            pivot_df = pivot_df.sort_values(by="_sort_key", ascending=ascending)
            pivot_df = pivot_df.drop(columns=["_sort_key"])
        elif is_numeric_column(sample_values):
            # Numeric column: "2", "3", etc.
            pivot_df["_sort_key"] = pivot_df[sort_by].apply(
                lambda x: float(x) if str(x).strip().replace('.', '', 1).isdigit() else float('-inf')
            )
            pivot_df = pivot_df.sort_values(by="_sort_key", ascending=ascending)
            pivot_df = pivot_df.drop(columns=["_sort_key"])
        else:
            # Text column: sort normally
            pivot_df = pivot_df.sort_values(by=sort_by, ascending=ascending)
    

    # ✅ Paginate
    paginator = Paginator(pivot_df.values.tolist(), 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': stock_filter,
        'page_obj': page_obj,
        'columns': pivot_df.columns.tolist(),
        'sort_by': sort_by,
        'sort_order': sort_order,
        "scan_name": request.GET.get("scan_name"),
        "igsymbol": request.GET.get("igsymbol"),
        "scan_result": request.GET.get("scan_result"),
        "has_data": not pivot_df.empty,
        'clean_querystring': clean_querystring(request, exclude_keys=['sort_by', 'sort_order', 'page']),
    }

    return render(request, 'common/stock_pivot.html', context)


def stock_search_view(request):
    form = SearchResultsForm(request.GET or None)

    queryset = search_results.objects.all()
    stock_filter = search_results_filter_scan_1(request.GET, queryset=queryset)

    sort_by = request.GET.get('sort', 'symbol_name')
    direction = request.GET.get('direction', 'asc')
    if direction == 'desc':
        sort_by = f'-{sort_by}'

    sorted_qs = stock_filter.qs.order_by(sort_by)

    # ✅ Export logic after sorted_qs is defined
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="filtered_stocks.csv"'

        writer = csv.writer(response)
        writer.writerow(['IG Symbol', 'CMC Symbol', 'TV Symbol', 'Symbol Name', 'Industry', 'Country', 'Exchange', 'Scan Name', 'Trade Type'])

        for stock in sorted_qs:
            writer.writerow([
                stock.igsymbol,
                stock.cmcsymbol,
                stock.tvsymbol,
                stock.symbol_name,
                stock.symbol_industry,
                stock.country_code,
                stock.exchange,
                stock.scan_name,
                stock.trade_type
            ])

        return response


    paginator = Paginator(sorted_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    querydict = request.GET.copy()
    querydict.pop('page', None)
    querystring = querydict.urlencode()

    return render(request, 'common/stock_list.html', {
        'form': form,
        'filters_applied': has_filters_applied(request),
        'filter': stock_filter,
        'page_obj': page_obj,
        'querystring': querystring,
        'current_sort': request.GET.get('sort', ''),
        'current_dir': request.GET.get('direction', ''),
    })


def export_stocks_csv(request):
    queryset = search_results_filter_scan_1(request.GET, queryset=search_results.objects.all()).qs
    queryset = queryset.values_list(
    'symbol', 'symbol_name', 'symbol_industry', 'symbol_sector',
    'scan_source', 'scan_name', 'scan_result', 'scan_cob_date', 'scan_run_date',
    'trade_type')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stocks.csv"'

    writer = csv.writer(response)
    writer.writerow(['symbol', 'symbol_name', 'symbol_industry', 'symbol_sector', 'scan_source', 'scan_name', 'scan_result', 'scan_cob_date', 'scan_run_date', 'trade_type'])

    for row in queryset:
        writer.writerow(row)

    return response


def export_stocks_pivot_csv(request):
    queryset = search_results.objects.all()
    stock_filter = search_results_filter_scan_1(request.GET, queryset=queryset)
    stock_filter_qs = stock_filter.qs

    fields = ['igsymbol', 'scan_name', 'scan_result']
    df = pd.DataFrame.from_records(stock_filter_qs.values(*fields))

    pivot_df = pd.pivot_table(
        df,
        index='igsymbol',
        columns='scan_name',
        values='scan_result',
        aggfunc='sum',
        fill_value='',
        margins=True,
        margins_name='Total'
    )

    # ✅ Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock_pivot.csv"'
    pivot_df.to_csv(response)

    return response