#!/usr/bin/env python3

from binance_client import BinanceClient
import asyncio
import typer
app = typer.Typer()
loop = asyncio.get_event_loop()


async def _print_top_symbols(quote_asset, param, size):
    client = await BinanceClient.create()

    result = await client.get_top_symbols(quote_asset, param, size, to_string=True)
    print(result)

    await client.close_connection()

# Answer to Question 1
@app.command()
def q1(quote_asset: str = "BTC", results: int = 5):
    """prints the top symbols by highest volume"""
    loop.run_until_complete(_print_top_symbols(quote_asset, "volume", results))

# Answer to Question 2
@app.command()
def q2(quote_asset: str = "USDT", results: int = 5):
    """prints the top symbols by highest number of trades"""
    loop.run_until_complete(_print_top_symbols(quote_asset, "count", results))

# Answer to Question 3
@app.command()
def q3(quote_asset: str = "BTC", results: int = 5, limit: int = 200):
    """prints the total notional value of top symbols by volume"""
    async def _q3():
        client = await BinanceClient.create()

        symbols = await client.get_top_symbols(quote_asset, "volume", results)
        summary = await asyncio.gather(*[client.get_total_notional_bids_asks(s, limit) for s in symbols])
        print(f"NUM SYMBOL{' '*5}BIDS{' '*17}ASKS")

        for i, s in enumerate(summary):
            print(f"{i+1:<3} {symbols[i]:<10} {s[0]:<20} {s[1]}")

        await client.close_connection()

    loop.run_until_complete(_q3())


if __name__ == "__main__":
    app()
