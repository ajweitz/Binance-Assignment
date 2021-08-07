
import ast
from binance import AsyncClient
from typing import Dict, List, Union
import asyncio

class BinanceClient:

    @classmethod
    async def create(cls):
        self = BinanceClient()
        self.client = await AsyncClient.create()
        return self

    async def get_24h_summary(self, quote_asset: List[str], parameter: str) -> Dict:
        tickers = await self.client.get_ticker()
        return {t["symbol"]: ast.literal_eval(str(t[parameter])) for t in tickers if t["symbol"].endswith(quote_asset)}

    async def get_top_symbols(self, quote_asset: str, parameter: str, top: int, to_string: bool = False) -> Union[list, str]:
        """Gets the top x symbols based on a given parameter, can return either a list of symbols or a printable string"""

        # get a dictionary of symbol -> parameter
        volumes = await self.get_24h_summary(quote_asset, parameter)

        # get x symbols with highest value
        leaders = sorted(volumes, key=volumes.get, reverse=True)[:top]

        if to_string:
            return "\n".join([f"{index+1:<3} {val:<10} {volumes[val]}" for index, val in enumerate(leaders)])

        return leaders

    async def get_total_notional_bids_asks(self, symbol, limit):
        order_book = await self.client.get_order_book(symbol=symbol, limit=limit)
        return await asyncio.gather(self.__sum_n_val(order_book["bids"]),self.__sum_n_val(order_book["asks"]))

    async def get_bid_ask_spread(self,symbol):
        ticker = await self.client.get_ticker(symbol=symbol)
        return float(ticker["askPrice"]) - float(ticker["bidPrice"])

    async def close_connection(self):
        await self.client.close_connection()

    async def __sum_n_val(self, arr: list):
        total = 0
        for e in arr:
            total += float(e[0]) * float(e[1])
        return total
