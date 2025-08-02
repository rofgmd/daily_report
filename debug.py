from fetchers.stock import get_us_stock_watchlist
import yaml

def debug():
    print(get_us_stock_watchlist())


if __name__ == "__main__":
    debug()