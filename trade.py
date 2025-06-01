import os
from dotenv import load_dotenv
load_dotenv(override=True)
import python_bithumb
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("--buy", action="store_true", help="Execute buy order")
parser.add_argument("--sell", action="store_true", help="Execute sell order")
parser.add_argument("--amount_krw", type=float, default=5000, help="Minimum KRW amount for an order")

access = os.getenv("BITHUMB_ACCESS_KEY")
secret = os.getenv("BITHUMB_SECRET_KEY")
bithumb = python_bithumb.Bithumb(access, secret)

if __name__ == "__main__":
    args = parser.parse_args()

    my_krw = bithumb.get_balance("KRW")
    my_btc = bithumb.get_balance("BTC")

    print(f"Current KRW Balance: {my_krw:.2f} KRW")
    print(f"Current BTC Balance: {my_btc:.6f} BTC")
    print(f"Current BTC Price: {python_bithumb.get_current_price('KRW-BTC'):.2f} KRW")

    if args.amount_krw < 5000:
        print("### Error: Minimum order amounts must be at least 5000 KRW ###")
        exit(1)

    current_price = python_bithumb.get_current_price("KRW-BTC") # 1 BTC price in KRW
    # 1 btc : x = current_price : amount_krw
    # x = amount_krw / current_price
    amount_krw_to_btc = args.amount_krw / current_price

    if args.buy:

        print(f"""
            Amount to {'BUY' if args.buy else 'SELL'}: {args.amount_krw:.2f} KRW
            Equivalent BTC Amount: {amount_krw_to_btc:.6f} BTC
        """)

        if args.amount_krw >= 5000:
            print("### Buy Order Executed ###")
            bithumb.buy_market_order("KRW-BTC", args.amount_krw)
        else:
            print("### Buy Order Failed: Insufficient KRW (less than 5000 KRW) ###")
    
    elif args.sell:

        print(f"""
            Amount to {'BUY' if args.buy else 'SELL'}: {args.amount_krw:.2f} KRW
            Equivalent BTC Amount: {amount_krw_to_btc:.6f} BTC
        """)

        if args.amount_krw  >= 5000:
            print("### Sell Order Executed ###")
            bithumb.sell_market_order("KRW-BTC", amount_krw_to_btc)
        else:
            print("### Sell Order Failed: Insufficient BTC (less than 5000 KRW worth) ###")

    my_krw = bithumb.get_balance("KRW")
    my_btc = bithumb.get_balance("BTC")

    print(f"Updated KRW Balance: {my_krw:.2f} KRW")
    print(f"Updated BTC Balance: {my_btc:.6f} BTC")
    print(f"Updated BTC Price: {python_bithumb.get_current_price('KRW-BTC'):.2f} KRW")