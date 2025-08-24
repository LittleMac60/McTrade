# ASX = Australian Stock Exchange
# LSE = London Stock Exchange
# NASDAQ = American Nasdac
# AMEX = Amerian Stock Exchange
# NYSE = New York Stock Exchange
#### Exchange Codes from VectorVest
# N = New York Stock Exchange
# A = American Stock Exchange
# O = Over-the-Counter (OTC) / NASDAQ
# TO = Toronto Stock Exchange


def us_conv_tv_exchangecode(Exchange):
    rtexcode = ''    
    if Exchange == 'xN':    
        rtexcode = 'NYSE'
    if Exchange == 'xA':
        rtexcode = 'AMEX'
    if Exchange == 'xO':
        rtexcode = 'NASDAQ'
    if Exchange == 'NYSE':
        rtexcode = 'N'
    if Exchange == 'AMEX':    
        rtexcode = 'A'
    if Exchange == 'NASDAQ':
        rtexcode = 'O'

    return rtexcode 


def us_exchange_conv(sn, symbol, country_code, exchange):
    if sn[0:4] == 'L-VV' or sn[0:4] == 'S-VV':
        tvsymbol = us_conv_tv_exchangecode(exchange) + ':' + symbol.split('.')[0]            
        exchange = exchange.replace('x', '')
        igsymbol = symbol + "." + exchange
        cmcsymbol = symbol.split('.')[0] + ':US'
    elif sn[0:4] == 'L-TV' or sn[0:4] == 'S-TV':
        igsymbol =  symbol.split('.')[0] + '.' + us_conv_tv_exchangecode(exchange)
        exchange = exchange
        cmcsymbol = symbol.split('.')[0] + ':US'
        tvsymbol = exchange + ':' + symbol.split('.')[0]
    elif sn[0:5] == 'L-CMC' or sn[0:5] == 'S-CMC':
        igsymbol = symbol.split('.')[0] + '.XX'       
        cmcsymbol = symbol
        tvsymbol = 'XX:' + symbol.split('.')[0]
    elif sn[0:4] == 'L-TR' or sn[0:4] == 'S-TR':
        igsymbol = symbol + '.XX'       
        cmcsymbol = symbol + ':US'
        tvsymbol = 'XX:' + symbol     
    else:
        igsymbol =  symbol.split('.')[0] + '.' + us_conv_tv_exchangecode(exchange)
        exchange = exchange
        cmcsymbol = symbol.split('.')[0] 
        tvsymbol = exchange + ':' + symbol.split('.')[0]
    return igsymbol, cmcsymbol, tvsymbol, exchange


def au_exchange_conv(sn, symbol, country_code, exchange):
    exchange = 'ASX'
    if sn[0:4] == 'L-VV' or sn[0:4] == 'S-VV':
        igsymbol = symbol
        cmcsymbol = symbol.split('.')[0]
        tvsymbol = 'ASX:' + symbol.split('.')[0]
    else:
        igsymbol = symbol + '.AX'       
        cmcsymbol = symbol
        tvsymbol = 'ASX:' + symbol
    return igsymbol, cmcsymbol, tvsymbol, exchange


def uk_exchange_conv(sn, symbol, country_code, exchange):
    exchange = 'LSE'
    if sn[0:4] == 'L-VV' or sn[0:4] == 'S-VV':
        igsymbol = symbol
        cmcsymbol = symbol.split('.')[0] 
        tvsymbol = 'LSE:' + symbol.split('.')[0]
    elif sn[0:4] == 'L-TV' or sn[0:4] == 'S-TV':
        igsymbol = symbol + '.L'       
        cmcsymbol = symbol + ':GB'
        tvsymbol = 'LSE:' + symbol
    elif sn[0:5] == 'L-CMC' or sn[0:5] == 'S-CMC':
        igsymbol = symbol.split('.')[0] + '.L'       
        cmcsymbol = symbol
        tvsymbol = 'LSE:' + symbol.split('.')[0]
    elif sn[0:4] == 'L-TR' or sn[0:4] == 'S-TR':
        igsymbol = 'LSE:' + symbol + '.L'       
        cmcsymbol = 'LSE:' + symbol + ':GB'
        tvsymbol = 'LSE:' + symbol      
    else:
        igsymbol = 'LSE:' + symbol + '.L'       
        cmcsymbol = 'LSE:' + symbol
        tvsymbol = 'LSE:' + symbol
    return igsymbol, cmcsymbol, tvsymbol, exchange

    