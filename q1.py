#!/usr/bin/env python3

import asyncio
from binance_client import BinanceClient


async def main():
    top = 5  # set how many results we want to see in the output
    quote_asset = "BTC"  # the quote asset we're interested in
    parameter = "volume"  # the parameter we are interested in

    client = await BinanceClient.create()

    result = await client.get_top_symbols(quote_asset, parameter, top, True)
    print(result)
    
    await client.close_connection()


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
