import django_tables2 as tables
from common.models import search_results

class StockTable(tables.Table):
    class Meta:
        model = search_results
        template_name = "django_tables2/bootstrap5.html"
        fields = ('symbol', 'symbol_name', 'country_code', 'exchange', 'symbol_industry', 'symbol_sector', 'scan_source', 'scan_name', 'scan_result', 'scan_cob_date', 'scan_run_date', 'trade_type')