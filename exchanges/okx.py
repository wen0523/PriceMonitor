class OKX:
    def __init__(self, exchange, timeFrame, threshold):
        self.exchange = exchange
        self.timeFrame = timeFrame
        self.threshold = threshold

    async def getResult(self, symbol, since):
        ohlcv = await self.exchange.fetch_ohlcv(symbol, self.timeFrame, since, limit=1)

        try:
            open_time, open_price, high_price, low_price, close_price, volume = ohlcv[0]
            increase = ((close_price - open_price) / open_price) * 100
            if abs(increase) >= self.threshold:
                return f"\nSymbol: {symbol}, Price Change: {increase:.2f}%"
            else:
                return ''
        except Exception as e:
            return e
