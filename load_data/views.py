import pandas as pd
import os
import csv
from datetime import date, time, datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages


from common.tools.exchange_conv import au_exchange_conv, us_exchange_conv, uk_exchange_conv, us_conv_tv_exchangecode
from common.tools.forms import COBDateForm 
from common.models import search_results    


def crud_data(path_in, csv_in, sn, country_code, cob_date_formatted):
    csv_file_path = path_in + '\\' + csv_in
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader, None) # Skip header row if present
        data_rows = list(reader)

        if not data_rows:
            print("CSV has only header, no data rows.")
        else:
            for row in data_rows:
                if len(row) < 2:
                    print(f"Skipping row with insufficient data: {row}")
                    continue
                # Create a new model instance for each row
                exchange = ''
                if sn[0:1] == 'L':
                    trade_type = 'Long'
                elif sn[0:1] == 'S':
                    trade_type = 'Short'
                else:
                    trade_type = 'Unknown'   

                if sn[2:4] == 'VV':
                    exchange = ''
                    symbol = ''                   
                    if country_code == 'US':
                        symbol = row[1]                # eg BHP.AX    
                        exchange = row[2]
                        igsymbol, cmcsymbol, tvsymbol, exchange = us_exchange_conv(sn, symbol, country_code, exchange)
                    elif country_code == 'AU':
                        symbol = row[1]                # eg BHP.AX    
                        igsymbol, cmcsymbol, tvsymbol, exchange = au_exchange_conv(sn, symbol, country_code, exchange)
                    elif country_code == 'UK':
                        symbol = row[1]                # eg BHP.AX    
                        igsymbol, cmcsymbol, tvsymbol, exchange = uk_exchange_conv(sn, symbol, country_code, exchange)
                    else:
                        symbol = row[1]                # eg BHP.AX    
                        igsymbol, cmcsymbol, tvsymbol, exchange = None, None, None, None

                    try:
                        if country_code == 'US':
                            symbol = row[1]                # eg BHP.AX    
                            symbol_name = row[0]           # eg BHP
                            symbol_industry = row[3]
                            symbol_sector = row[4]
                            exchange_val = row[2]
                        else: 
                            symbol = row[1]                # eg BHP.AX    
                            symbol_name = row[0]           # eg BHP
                            symbol_industry = row[2]
                            symbol_sector = row[3]
                            exchange_val = exchange

                        search_results.objects.create(
                            symbol = symbol,
                            symbol_name = symbol_name,
                            symbol_industry = symbol_industry,
                            symbol_sector = symbol_sector,
                            country_code = country_code,     # eg AU
                            scan_source = sn[2:4],           # eg VV - Vectorvest, TV - Tradingview    
                            scan_name = sn,                  # eg L-VV(SS TL) - Long Vectorvest(save stocks trade long)
                            scan_result = True,
                            scan_cob_date = cob_date_formatted,
                            scan_cob_time = time(),
                            scan_run_date = date.today(),
                            scan_run_time = time(),
                            exchange = exchange_val,
                            igsymbol = igsymbol,
                            cmcsymbol = cmcsymbol,
                            tvsymbol = tvsymbol,
                            trade_type = trade_type,
                        )
                    except Exception as e:
                        print(f"Error saving to database: {e}")

                elif sn[2:5] == 'CMC':
                    symbol = row[17]                     # eg BHP.AX
                    if country_code == 'US':
                        igsymbol, cmcsymbol, tvsymbol, exchange = us_exchange_conv(sn, symbol, country_code, exchange)
                    elif country_code == 'AU':  
                        igsymbol, cmcsymbol, tvsymbol, exchange = au_exchange_conv(sn, symbol, country_code, exchange)
                    elif country_code == 'UK':
                        igsymbol, cmcsymbol, tvsymbol, exchange = uk_exchange_conv(sn, symbol, country_code, exchange)
                    else:
                        igsymbol, cmcsymbol, tvsymbol, exchange = None, None, None, None

                    if sn == 'L-CMC(SS)' or sn == 'S-CMC(US)':
                        symbol = row[17]                # eg BHP.AX    
                        symbol_name = row[0]           # eg BHP
                        symbol_industry = row[2]
                        symbol_sector = row[1]
                        exchange_val = exchange
                    else: 
                        symbol = row[17]                # eg BHP.AX    
                        symbol_name = row[0]           # eg BHP
                        symbol_industry = row[2]
                        symbol_sector = row[1]
                        exchange_val = exchange

                    try:
                        search_results.objects.create(
                            symbol = row[17],             # eg BHP.AX    
                            symbol_name = row[0],           # eg BHP
                            symbol_industry = symbol_industry,
                            symbol_sector = symbol_sector,
                            country_code = country_code,     # eg AU
                            scan_source = sn[2:5],           # eg VV - Vectorvest, TV - Tradingview    
                            scan_name = sn,                  # eg L-VV(SS TL) - Long Vectorvest(save stocks trade long)
                            scan_result = True,
                            scan_cob_date = cob_date_formatted,
                            scan_cob_time = time(),
                            scan_run_date = date.today(),
                            scan_run_time = time(),
                            exchange = exchange_val,
                            igsymbol = igsymbol,
                            cmcsymbol = cmcsymbol,
                            tvsymbol = tvsymbol,
                            trade_type = trade_type,
                        )
                    except Exception as e:
                        print(f"Error saving to database: {e}") 

                elif sn[2:4] == 'TV':
                    symbol = row[0]
                    exchange = row[2]                     # eg BHP.AX
                    if country_code == 'US':
                        igsymbol, cmcsymbol, tvsymbol, exchange = us_exchange_conv(sn, symbol, country_code, exchange)
                    elif country_code == 'AU':  
                        igsymbol, cmcsymbol, tvsymbol, exchange = au_exchange_conv(sn, symbol, country_code, exchange)
                    elif country_code == 'UK':
                        igsymbol, cmcsymbol, tvsymbol, exchange = uk_exchange_conv(sn, symbol, country_code, exchange)
                    else:
                        igsymbol, cmcsymbol, tvsymbol, exchange = None, None, None, None

                    try:
                        search_results.objects.create(
                            symbol = row[0],                # eg BHP.AX    
                            symbol_name = row[1],           # eg BHP
                            symbol_industry = '',
                            symbol_sector = '',
                            country_code = country_code,     # eg AU
                            scan_source = sn[2:4],           # eg VV - Vectorvest, TV - Tradingview    
                            scan_name = sn,                  # eg L-VV(SS TL) - Long Vectorvest(save stocks trade long)
                            scan_result = True,
                            scan_cob_date = cob_date_formatted,
                            scan_cob_time = time(),
                            scan_run_date = date.today(),
                            scan_run_time = time(),
                            exchange = exchange,
                            igsymbol = igsymbol,
                            cmcsymbol = cmcsymbol,
                            tvsymbol = tvsymbol,
                            trade_type = trade_type,
                        )
                    except Exception as e:
                        print(f"Error saving to database: {e}")

                elif sn[2:4] == 'TR':
                    symbol = row[17]                     # eg BHP.AX
                    if country_code == 'US':
                        igsymbol, cmcsymbol, tvsymbol, exchange = us_exchange_conv(sn, symbol, country_code, exchange)
                    elif country_code == 'AU':  
                        igsymbol, cmcsymbol, tvsymbol, exchange = au_exchange_conv(sn, symbol, country_code, exchange)
                    elif country_code == 'UK':
                        igsymbol, cmcsymbol, tvsymbol, exchange = uk_exchange_conv(sn, symbol, country_code, exchange)
                    else:
                        igsymbol, cmcsymbol, tvsymbol, exchange = None, None, None, None
                        
                    try:
                        search_results.objects.create( 
                            symbol = row[17],               # eg BHP.AX    
                            symbol_name = row[0],           # eg BHP
                            symbol_industry = '',
                            symbol_sector = row[2],
                            country_code = country_code,     # eg AU
                            scan_source = sn[2:4],           # eg VV - Vectorvest, TV - Tradingview    
                            scan_name = sn,                  # eg L-VV(SS TL) - Long Vectorvest(save stocks trade long)
                            scan_result = True,
                            scan_cob_date = cob_date_formatted,
                            scan_cob_time = time(),
                            scan_run_date = date.today(),
                            scan_run_time = time(),
                            exchange = exchange,
                            igsymbol = igsymbol,
                            cmcsymbol = cmcsymbol,
                            tvsymbol = tvsymbol,
                            trade_type = trade_type,
                        )
                    except Exception as e:
                        print(f"Error saving to database: {e}")        
        

# def allocate_file_2_process(path_in, country, scan_source):
def allocate_file_2_process(path_in, country, scan_source, cob_date):
    cob_date_formatted = cob_date.strftime("%Y-%m-%d")
    print(f"Processing {scan_source} for {country} on {cob_date_formatted}")
    
    # Example: use date in filename or tagging
    # filename = f"{scan_source}_update_{formatted_date}.csv"
    # full_path = os.path.join(path_in, filename)





    print("Processing " + scan_source + " files")
    files = os.listdir(path_in)
    for file in files:
        sn = r'nothing'
# VectorVest
        if scan_source == 'VV':
            sn = r'nothing'

            if file[3:11] == 'L-VV(SS)':
                sn = r'L-VV(SS)'
            
            if file[3:14] == 'L-VV(SS TL)':
                sn = r'L-VV(SS TL)'

            if file[3:11] == 'S-VV(US)':
                sn = r'S-VV(US)'

            if file[3:14] == 'S-VV(US TS)':
                sn = r'S-VV(US TS)'
        
            if file[3:11] == 'L-VV(ST)':
                sn = r'L-VV(ST)'

            if file[3:11] == 'S-VV(ST)':
                sn = r'S-VV(ST)'

            if file[3:12] == 'L-VV(VST)':
                sn = r'L-VV(VST)'

            if file[3:12] == 'S-VV(VST)':
                sn = r'S-VV(VST)'  

            if file[3:19] == 'L-VV(Entry-Exit)':
                sn = r'L-VV(EE)'

            if file[3:19] == 'S-VV(Entry-Exit)':
                sn = r'S-VV(EE)'      
# TradingView
        if scan_source == 'TV':
            sn = r'nothing'

            if file[2:14] == '01-L-TV(BUV)':
                sn = r'L-TV(BUV)'
            
            if file[2:14] == '01-S-TV(BOV)':
                sn = r'S-TV(BOV)'

            if file[2:15] == '03-L-TV(TU1W)':
                sn = r'L-TV(TU1W)'

            if file[2:15] == '03-S-TV(TD1W)':
                sn = r'S-TV(TD1W)'
    
            if file[2:25] == '13-L-TV(L-CMC(MS-UV)) T':
                sn = r'L-TV-CMC(MS-UV) T' 

            if file[2:25] == '13-S-TV(S-CMC(MS-OV)) T':
                sn = r'S-TV-CMC(MS-OV) T'
                
            if file[2:22] == '13-L-TV(L-CMC(SS)) T':
                sn = r'L-TV-CMC(SS) T'

            if file[2:22] == '13-S-TV(S-CMC(US)) T':
                sn = r'S-TV-CMC(US) T'

            if file[2:25] == '13-L-TV(L-CMC(SC-UP)) T':
                sn = r'L-TV-CMC(SC-UP) T'

            if file[2:25] == '13-S-TV(S-CMC(SC-DN)) T':
                sn = r'S-TV-CMC(SC-DN) T'            

            if file[2:21] == '12-L-TV(L-TR(OP)) T':
                sn = r'L-TV-TR(OP) T'

            if file[2:21] == '12-S-TV(S-TR(UP)) T':
                sn = r'S-TV-TR(UP) T'

            if file[2:21] == '11-L-TV(L-VV(SS)) T':
                sn = r'L-TV-VV(SS) T'

            if file[2:21] == '11-S-TV(S-VV(US)) T':
                sn = r'S-TV-VV(US) T'

            if file[2:20] == '14-L-TV(ANAL-TECH)':
                sn = r'L-TV(ANAL-TECH)'

            if file[2:20] == '14-S-TV(ANAL-TECH)':
                sn = r'S-TV(ANAL-TECH)'

            if file[2:18] == '15-L-TV(ema-3x8)':
                sn = r'L-TV(ema-3x8)' 

            if file[2:18] == '15-S-TV(ema-3x8)': 
                sn = r'S-TV(ema-3x8)'

            if file[2:19] == '16-L-TV(ema-5x40)':
                sn = r'L-TV(ema-5x40)'

            if file[2:19] == '16-S-TV(ema-5x40)':
                sn = r'S-TV(ema-5x40)' 

            if file[2:20] == '17-L-TV(Tech-Only)':
                sn = r'L-TV(Tech-Only)'

            if file[2:20] == '17-S-TV(Tech-Only)':
                sn = r'S-TV(Tech-Only)'
# CMC
        if scan_source == 'CMC':
            sn = r'nothing'

            if file[-13:] == 'CMC-SC-UP.csv':
                sn = r'L-CMC(SC-UP)'

            if file[-13:] == 'CMC-SC-DN.csv':
                sn = r'S-CMC(SC-DN)'

            if file[-13:] == 'CMC-MS-UV.csv':
                sn = r'L-CMC(MS-UV)'

            if file[-13:] == 'CMC-MS-OV.csv':
                sn = r'S-CMC(MS-OV)'

            if file[-10:] == 'CMC-SS.csv':
                sn = r'L-CMC(SS)'

            if file[-10:] == 'CMC-US.csv':
                sn = r'S-CMC(US)'
# Tip Ranks
        if scan_source == 'TR':
            sn = r'nothing'

            if file[-9:] == 'TR-OP.csv':
                sn = r'L-TR(OP)'
            
            if file[-9:] == 'TR-UP.csv': 
                sn = r'S-TR(UP)'

        if sn != 'nothing':
            csv_in = file
            print("Processing file " + file)
            crud_data(path_in, csv_in, sn, country, cob_date_formatted)   


def au_create_search_results(request):
    country = 'AU'

    if request.method == "POST":
        form = COBDateForm(request.POST)
        if form.is_valid():
            cob_date = form.cleaned_data["cob_date"]

            # Define all scan sources and paths
            scan_sources = {
                'VV': r'C:\Users\wayne\OneDrive\Documents\McTrading\AU McTrading V1\AU McTrading - VV',
                'TV': r'C:\Users\wayne\OneDrive\Documents\McTrading\AU McTrading V1\AU McTrading - TV',
                'CMC': r'C:\Users\wayne\OneDrive\Documents\McTrading\AU McTrading V1\AU McTrading - CMC',
                'TR': r'C:\Users\wayne\OneDrive\Documents\McTrading\AU McTrading V1\AU McTrading - TR',
            }

            # Process each source with the COB date
            for scan_source, path_in in scan_sources.items():
                allocate_file_2_process(path_in, country, scan_source, cob_date)

            return HttpResponse("AU CRUD process completed.")
    else:
        form = COBDateForm()

    return render(request, "common/upload.html", {"form": form})


# US ###################
def us_create_search_results(request):
    country = 'US'

    if request.method == "POST":
        form = COBDateForm(request.POST)
        if form.is_valid():
            cob_date = form.cleaned_data["cob_date"]

            # Define all scan sources and paths
            scan_sources = {
                'VV': r'C:\Users\wayne\OneDrive\Documents\McTrading\US McTrading V1\US McTrading - VV',
                'TV': r'C:\Users\wayne\OneDrive\Documents\McTrading\US McTrading V1\US McTrading - TV',
                'CMC': r'C:\Users\wayne\OneDrive\Documents\McTrading\US McTrading V1\US McTrading - CMC',
                'TR': r'C:\Users\wayne\OneDrive\Documents\McTrading\US McTrading V1\US McTrading - TR',
            }

            # Process each source with the COB date
            for scan_source, path_in in scan_sources.items():
                allocate_file_2_process(path_in, country, scan_source, cob_date)

            return HttpResponse("US CRUD process completed.")
    else:
        form = COBDateForm()

    return render(request, "common/upload.html", {"form": form})


# UK ###################
def uk_create_search_results(request):
    country = 'UK' \

    if request.method == "POST":
        form = COBDateForm(request.POST)
        if form.is_valid():
            cob_date = form.cleaned_data["cob_date"]

            # Define all scan sources and paths
            scan_sources = {
                'VV': r'C:\Users\wayne\OneDrive\Documents\McTrading\UK McTrading V1\UK McTrading - VV',
                'TV': r'C:\Users\wayne\OneDrive\Documents\McTrading\UK McTrading V1\UK McTrading - TV',
                'CMC': r'C:\Users\wayne\OneDrive\Documents\McTrading\UK McTrading V1\UK McTrading - CMC',
                'TR': r'C:\Users\wayne\OneDrive\Documents\McTrading\UK McTrading V1\UK McTrading - TR',
            }

            # Process each source with the COB date
            for scan_source, path_in in scan_sources.items():
                allocate_file_2_process(path_in, country, scan_source, cob_date)

            return HttpResponse("UK CRUD process completed.")
    else:
        form = COBDateForm()

    return render(request, "common/upload.html", {"form": form})


def create_tv_import_csv(df, csv_out_tv_wlimp):
    csvline = df['TV Symbol'].str.cat(sep = ',')
    with open(csv_out_tv_wlimp, 'w', newline = '') as csvfile:
        csvfile.write(csvline)
    csvfile.close() 


def home(request):
    return render(request, 'common/base.html')


def delete_search_results(pcountry, pcob_date):
    deleted_count, _ = search_results.objects.filter(country_code=pcountry, scan_cob_date=pcob_date).delete()
    date_str = pcob_date.strftime('%Y-%m-%d') if pcob_date else 'unspecified'
    if deleted_count:
         return HttpResponse(f"✅ Deleted {deleted_count} record(s) for country code '{pcountry}' on COB date {date_str}.")
    else:
        return HttpResponseNotFound(f"No records found with country code '{pcountry}' for COB date {date_str}.")


def au_delete_search_results(request):
    pcountry = 'AU'

    if request.method == "POST":
        form = COBDateForm(request.POST)
        if form.is_valid():
            pcob_date = form.cleaned_data["cob_date"]

            # Get the response from delete function
            response = delete_search_results(pcountry, pcob_date)

            # Extract message from response content
            result_message = response.content.decode()

            # Use Django messages framework to pass it to the template
            messages.info(request, "AU CRUD delete records process completed.")
            messages.success(request, result_message)

            return redirect('au_delete_search_results')  # Redirect to GET view to show messages
    else:
        form = COBDateForm()

    return render(request, "common/delete_records_prompt.html", {"form": form})


def delete_files_for_date(path_in, pcountry, scan_source, pcob_date):
    formatted_date = pcob_date.strftime("%Y-%m-%d")
    filename = f"{scan_source}_update_{formatted_date}.csv"
    full_path = os.path.join(path_in, filename)

    if os.path.exists(full_path):
        os.remove(full_path)
        print(f"Deleted: {full_path}")
    else:
        print(f"File not found: {full_path}")


def au_delete_search_results_files(request):
    pcountry = 'AU'

    if request.method == "POST":
        form = COBDateForm(request.POST)
        if form.is_valid():
            pcob_date = form.cleaned_data["cob_date"]

            # Define scan sources and paths
            scan_sources = {
                'VV': r'C:\Users\wayne\OneDrive\Documents\McTrading\AU McTrading V1\AU McTrading - VV',
                'TV': r'C:\Users\wayne\OneDrive\Documents\McTrading\AU McTrading V1\AU McTrading - TV',
                'CMC': r'C:\Users\wayne\OneDrive\Documents\McTrading\AU McTrading V1\AU McTrading - CMC',
                'TR': r'C:\Users\wayne\OneDrive\Documents\McTrading\AU McTrading V1\AU McTrading - TR',
            }

            # Run delete logic for each source
            for scan_source, path_in in scan_sources.items():
                delete_files_for_date(path_in, pcountry, scan_source, pcob_date)

            return HttpResponse("AU CRUD delete files process completed.")
    else:
        form = COBDateForm()

    return render(request, "common/delete_files_prompt.html", {"form": form})


def us_delete_search_results(request):
    pcountry_code = 'US'
    return delete_search_results(pcountry_code)


def uk_delete_search_results(request):
    pcountry_code = 'UK'
    return delete_search_results(pcountry_code)

       