#!/usr/bin/env python3

from binance_client import BinanceClient
from datetime import datetime
import time
import asyncio
import typer
import json as jsonParser # to avoid conflict with json parameter of q5 command
from flask import Response, Flask
import prometheus_client

cli = typer.Typer()
server = Flask(__name__)
loop = asyncio.get_event_loop()
client = loop.run_until_complete(BinanceClient.create())

Q1_DEFAULT_QUOTE_ASSET = "BTC"
Q1_COMPARE_PARAMETER = "volume"
Q2_DEFAULT_QUOTE_ASSET = "USDT"
Q2_COMPARE_PARAMETER = "count"
DEFAULT_TOTAL_RESULTS = 5
DEFAULT_LIMIT = 200
DEFAULT_REFRESH_RATE = 10
PROMETHEUS_PORT = 8080

# for question 1 and 2
async def _print_top_symbols(quote_asset, param, size):
    client = await BinanceClient.create()

    result = await client.get_top_symbols(quote_asset, param, size, to_string=True)
    print(result)

    await client.close_connection()

# Answer to Question 1
@cli.command()
def q1(quote_asset: str = Q1_DEFAULT_QUOTE_ASSET, results: int = DEFAULT_TOTAL_RESULTS):
    """prints the top symbols by highest volume"""
    loop.run_until_complete(_print_top_symbols(quote_asset, Q1_COMPARE_PARAMETER, results))

# Answer to Question 2
@cli.command()
def q2(quote_asset: str = Q2_DEFAULT_QUOTE_ASSET, results: int = DEFAULT_TOTAL_RESULTS):
    """prints the top symbols by highest number of trades"""
    loop.run_until_complete(_print_top_symbols(quote_asset, Q2_COMPARE_PARAMETER, results))

# Answer to Question 3
@cli.command()
def q3(quote_asset: str = Q1_DEFAULT_QUOTE_ASSET, results: int = DEFAULT_TOTAL_RESULTS, limit: int = DEFAULT_LIMIT):
    """prints the total notional value of top symbols by volume"""
    async def _q3():
        client = await BinanceClient.create()

        symbols = await client.get_top_symbols(quote_asset, Q1_COMPARE_PARAMETER, results)
        summary = await asyncio.gather(*[client.get_total_notional_bids_asks(s, limit) for s in symbols])
        print(f"NUM SYMBOL{' '*5}BIDS{' '*17}ASKS")

        for i, s in enumerate(summary):
            print(f"{i+1:<3} {symbols[i]:<10} {s[0]:<20} {s[1]}")

        await client.close_connection()

    loop.run_until_complete(_q3())

# Answer to Question 4
@cli.command()
def q4(quote_asset: str = Q2_DEFAULT_QUOTE_ASSET, results: int = DEFAULT_TOTAL_RESULTS):
    """prints the price spread for each of the top symbols by highest number of trades"""
    async def _q4():
        client = await BinanceClient.create()

        symbols = await client.get_top_symbols(quote_asset, Q2_COMPARE_PARAMETER, results)
        summary = await client.get_bid_ask_spread(symbols)
        print(f"NUM SYMBOL{' '*5}SPREAD")

        for i, s in enumerate(summary):
            print(f"{i+1:<3} {symbols[i]:<10} {s}")

        await client.close_connection()

    loop.run_until_complete(_q4())

# Answer to Question 5
@cli.command()
def q5(quote_asset: str = Q2_DEFAULT_QUOTE_ASSET, results: int = DEFAULT_TOTAL_RESULTS, refresh_rate: int = DEFAULT_REFRESH_RATE, json: bool = False):
    """prints the absolute delta of the price spread for each of the top symbols by highest number of trades"""
    async def _q5():
        async def _print_human_readable(symbols, deltas):
            print(datetime.now())
            for i, d in enumerate(deltas):
                print(f"{i+1:<3} {symbols[i]:<10} {d}")
            print("")

        async def _print_json_format(symbols, deltas):
            j = {
                "timestamp": int(time.time() * 1000 ),
                "spreadDeltas": []}
            for i, d in enumerate(deltas):
                j["spreadDeltas"].append([symbols[i],d])
            print(jsonParser.dumps(j))

        client = await BinanceClient.create()

        symbols = await client.get_top_symbols(quote_asset, Q2_COMPARE_PARAMETER, results)
        await client.set_spread_tracking(symbols)

        while True:
            await asyncio.sleep(refresh_rate)
            deltas = await client.get_spread_abs_delta()
            if json:
                await _print_json_format(symbols, deltas)
            else:
                await _print_human_readable(symbols, deltas)

    loop.run_until_complete(_q5())

# Answer to Question 6
gauges = []
@cli.command()
def q6(quote_asset: str = Q2_DEFAULT_QUOTE_ASSET, results: int = DEFAULT_TOTAL_RESULTS, refresh_rate: int = DEFAULT_REFRESH_RATE, json: bool = False):
    """prints the absolute delta of the price spread for each of the top symbols by highest number of trades"""
    symbols = loop.run_until_complete(client.get_top_symbols(quote_asset, Q2_COMPARE_PARAMETER, results))
    for s in symbols:
        gauges.append(prometheus_client.Gauge(f"price_spread_delta_{s}", f"Gauge of the absolute delta of the price spread for {s}"))
    loop.run_until_complete(client.set_spread_tracking(symbols))
    server.run(port=PROMETHEUS_PORT)

@server.route("/metrics")
def q6_metrics():
    deltas = loop.run_until_complete(client.get_spread_abs_delta())
    res = []
    for i, d in enumerate(deltas):
        gauges[i].set(d)
        res.append(prometheus_client.generate_latest(gauges[i]))
    return Response(res, mimetype="text/plain")    

if __name__ == "__main__":
    cli()
