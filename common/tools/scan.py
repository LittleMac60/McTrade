import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup


# ASX_TICKERS = ['CBA.AX', 'BHP.AX', 'CSL.AX', 'FMG.AX', 'NAB.AX']
ASX_TICKERS = ['JBH.AX','SRG.AX','SHA.AX','MND.AX','CWP.AX','APZ.AX','RMD.AX','SNL.AX','IAG.AX','CQR.AX','EOL.AX','CLW.AX','INA.AX']
SHORT_MA = 50
LONG_MA = 200
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

def calculate_indicators(df):
    # Moving Averages
    df['MA_short'] = df['Close'].rolling(SHORT_MA).mean()
    df['MA_long'] = df['Close'].rolling(LONG_MA).mean()

    # RSI Calculation
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(RSI_PERIOD).mean()
    loss = -delta.where(delta < 0, 0).rolling(RSI_PERIOD).mean()
    gain, loss = gain.align(loss, axis=0, copy=False)  # Align by index
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD and Signal Line
    exp1 = df['Close'].ewm(span=MACD_FAST, adjust=False).mean()
    exp2 = df['Close'].ewm(span=MACD_SLOW, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['MACD_signal'] = df['MACD'].ewm(span=MACD_SIGNAL, adjust=False).mean()

    # 52-week high proximity
    df['52w_high'] = df['Close'].rolling(window=252).max()

    # Fix: Ensure both operands are Series and aligned by index
    close = df['Close']
    high = df['52w_high']
    if isinstance(close, pd.DataFrame):
        close = close.squeeze()
    if isinstance(high, pd.DataFrame):
        high = high.squeeze()
    close, high = close.align(high, axis=0, copy=False)
    df['near_high'] = close > 0.95 * high

    return df

def scan_ticker(ticker):
    data = yf.download(ticker, period='1y', interval='1d', auto_adjust=True)

    if data.empty:
        return None

    df = calculate_indicators(data)
    df = df.dropna()
    if df.empty:
        return None

    latest = df.iloc[-1]

    # Safely convert RSI to float before rounding
    try:
        rsi_rounded = round(latest['RSI'].item(), 2)
    except (AttributeError, ValueError, TypeError):
        rsi_rounded = None

    # Safely extract boolean flags
    try:
        golden_cross = bool(latest['MA_short'] > latest['MA_long'])
        death_cross = bool(latest['MA_short'] < latest['MA_long'])
        macd_bullish = bool(latest['MACD'] > latest['MACD_signal'])
        near_high_flag = latest['near_high'].item() if hasattr(latest['near_high'], 'item') else bool(latest['near_high'])
    except Exception:
        golden_cross = death_cross = macd_bullish = near_high_flag = None

    return {
        'Ticker': ticker,
        'Golden_Cross': golden_cross,
        'Death_Cross': death_cross,
        'MACD_Bullish': macd_bullish,
        'RSI': rsi_rounded,
        'Near_52w_High': near_high_flag
    }

def run_scan(ticker_list):
    results = []
    for t in ticker_list:
        result = scan_ticker(t)
        if result:
            results.append([
                result['Ticker'],
                result['Golden_Cross'],
                result['Death_Cross'],
                result['MACD_Bullish'],
                result['RSI'],
                result['Near_52w_High']
            ])
    return results


def get_asx_all_ords_tickers():
    url = "https://www.marketindex.com.au/all-ordinaries"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tickers = []

    for row in soup.select('table tbody tr'):
        code_cell = row.select_one('td')
        if code_cell:
            tickers.append(code_cell.text.strip() + ".AX")

    return tickers


def run_scan_with_all_ords():
    ticker_file = "all_ords_tickers.csv"
    tickers = pd.read_csv(ticker_file)['Symbol'].tolist()
