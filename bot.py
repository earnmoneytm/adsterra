import ccxt
import pandas as pd
import talib
import time

# Configuración del exchange y API de Bit2Me (o cualquier exchange)
exchange = ccxt.bit2me({
    'apiKey': 'EYJU7vjcfTbxChRVclOanf7zqoSg1BW3LAFKLt03xPu0hs_I3OdcnNFq728xdy2jyRyYEYsc3YLN-8fLzRUnInCshamFKFYLztAknhIXINu6kIZukS0nMrtcFTCldjrt',
    'secret': '2Ra66aU8ZiL2NcS1uk1pIvIMxWO1JrCdi7UPQAjGSpAg70QGASBdOFtVWjfqKLAEHlDWoftMhVH7MXKa40CpJ3GLADGFE4YTSl9GcCjBTCctSYFMd6puf8QI-BBXJLgK'
})

symbol = 'BTC/EUR'  # Par de criptomonedas para operar
capital = 1000  # Capital para cada operación

def get_data():
    # Obtener datos de mercado
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=100)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df

def trading_bot():
    df = get_data()
    close = df['close']
    # Cálculo de indicadores
    sma20 = talib.SMA(close, timeperiod=20)
    rsi = talib.RSI(close, timeperiod=14)
    
    # Estrategia de compra
    if close.iloc[-1] < sma20.iloc[-1] * 0.95 and rsi.iloc[-1] < 30:
        print("Comprar")
        # Código para ejecutar orden de compra
        exchange.create_market_buy_order(symbol, capital / close.iloc[-1])

    # Estrategia de venta
    elif close.iloc[-1] > sma20.iloc[-1] * 1.05 or rsi.iloc[-1] > 70:
        print("Vender")
        # Código para ejecutar orden de venta
        exchange.create_market_sell_order(symbol, capital / close.iloc[-1])

# Ejecución del bot cada minuto
while True:
    try:
        trading_bot()
        time.sleep(60)  # Espera de 1 minuto antes de la siguiente ejecución
    except Exception as e:
        print(f"Error: {e}")
