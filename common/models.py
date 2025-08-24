from django.db import models

class search_results(models.Model):
    country_code = models.CharField(max_length=2)           # eg AU
    exchange = models.CharField(max_length=10)              # eg ASX     
    symbol = models.CharField(max_length=10)                # eg BHP.AX    
    symbol_name = models.CharField(max_length=30)           # eg BHP
    symbol_industry = models.CharField(max_length=30)
    symbol_sector = models.CharField(max_length=30)
    scan_source = models.CharField(max_length=5)           # eg VV - Vectorvest, TV - Tradingview    
    scan_name = models.CharField(max_length=30)            # eg L-VV(SS TL) - Long Vectorvest(save stocks trade long),
    scan_result = models.BooleanField(default=False)
    scan_cob_date = models.DateField()  # Close of Business date
    scan_cob_time = models.TimeField(auto_now_add=True, null=True)  # Close of Business time
    scan_run_date = models.DateField(auto_now_add=True)
    scan_run_time = models.TimeField(auto_now_add=True)
    igsymbol = models.CharField(max_length=10)
    cmcsymbol = models.CharField(max_length=10)
    tvsymbol = models.CharField(max_length=10)
    trade_type = models.CharField(max_length=10,default='Long')

    def __str__(self):
        return f"{self.symbol_name} ({self.symbol})"