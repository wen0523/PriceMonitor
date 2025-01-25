class Exchange:
    def __init__(self, exchange, threshold):
        self.exchange = exchange
        self.threshold = threshold

    # Get the price through the exchange API and calculate the price change.
    async def getResult(self, symbol, sinceCurrent, sinceBefore):
        ohlcvCurrent = await self.exchange.fetch_ohlcv(symbol, '1m', sinceCurrent, limit=1)
        ohlcvBefore = await self.exchange.fetch_ohlcv(symbol, '1m', sinceBefore, limit=1)

        try:
            close_price = ohlcvCurrent[0][4]
            open_price = ohlcvBefore[0][1]
            
            increase = ((close_price - open_price) / open_price) * 100
            if abs(increase) >= self.threshold:
                return f"\nSymbol: {symbol}, Price Change: {increase:.2f}%"
            else:
                return None
        except Exception as e:
            return e
