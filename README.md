# Binance Assignment
For this assignemnt I chose `python` because of my familiarity with the language and the libraries it provides.  
I chose to provide the answers inside a parameterized script.  
## Requirements
Python 3.6

## Running the answers
`pip install -r requirements.txt`

1. `python answers.py q1`
2. `python answers.py q2`
3. `python answers.py q3`
4. `python answers.py q4`
5. `python answers.py q5`
6. `python answers.py q6`

The defaults for each commands are set with the parameters required by the assignemnt.  
Howerver, I set these parameters to be dynamic, so you can run stuff like:  
`python answers.py q1 --quote-asset USDT --results 20`  
`python answers.py q3 --results 20 --limit 300`  
`python answers.py q5 --refresh-rate 2 --json`  

## Asignment Details
### Assignment
- Use public market data from the SPOT API at https://api.binance.com
- Binance API spot documentation is at https://github.com/binance-exchange/binance-official-api-docs/
- All answers should be provided as source code written in either Go, Python, Java, Rust, and/or Bash.
### Questions:
1. Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order.
2. Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order.
3. Using the symbols from Q1, what is the total notional value of the top 200 bids and asks currently on each order book?
4. What is the price spread for each of the symbols from Q2?
5. Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol.
6. Make the output of Q5 accessible by querying http://localhost:8080/metrics using the Prometheus Metrics format.