import django_filters

from common.models import search_results


class search_results_filter_scan_1(django_filters.FilterSet):
    scan_cob_date = django_filters.DateFilter(field_name='scan_cob_date')  # ✅ uses 'exact' by default
    scan_run_date = django_filters.DateFilter(field_name='scan_run_date')  # ✅ uses 'exact' by default

    scan_result = django_filters.ChoiceFilter(
        field_name='scan_result',
        choices=[('', 'All'), ('1', 'Selected'), ('0', 'Not Selected')],
        empty_label='All',
        label='Scan Result'
    )

    trade_type = django_filters.ChoiceFilter(
        field_name='trade_type',
        choices=[('', 'All'), ('Long', 'Long'), ('Short', 'Short')],
        empty_label='All',
        label='Trade Type'
    )

    class Meta:
        model = search_results
        fields = [
            'symbol', 'symbol_name', 'country_code', 'exchange',
            'symbol_industry', 'symbol_sector', 'scan_source',
            'scan_name', 'scan_result', 'scan_cob_date',
            'scan_run_date', 'trade_type'
        ]
        filter_overrides = {
            django_filters.CharFilter: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                    'label': f.verbose_name.capitalize()
                }
            },
         }


class StockFilter(django_filters.FilterSet):
    symbol = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = search_results
        fields = ['symbol', 'symbol_name', 'country_code', 'exchange', 'symbol_industry', 'symbol_sector', 'scan_source', 'scan_name', 'scan_result', 'scan_cob_date', 'scan_run_date', 'trade_type']


def has_filters_applied(request):
    # Exclude pagination and sorting keys
    ignored_keys = {'page', 'sort', 'direction'}
    return any(key for key in request.GET if key not in ignored_keys and request.GET.get(key))