#!/usr/bin/env python3

import asyncio
from binance_client import BinanceClient


async def main():
    total_symbols = 5
    limit = 200  # limit
    quote_asset = "BTC"  # the quote asset we're interested in
    parameter = "volume"  # the parameter we are interested in

    client = await BinanceClient.create()

    symbols = await client.get_top_symbols(quote_asset, parameter, total_symbols)
    summary = await asyncio.gather(*[client.get_total_notional_bids_asks(s,limit) for s in symbols])
    print(f"NUM SYMBOL{' '*5}BIDS{' '*17}ASKS")
    
    for i, s in enumerate(summary):
        print(f"{i+1:<3} {symbols[i]:<10} {s[0]:<20} {s[1]}")

    await client.close_connection()


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
