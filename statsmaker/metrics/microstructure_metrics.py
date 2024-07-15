import numpy as np

def calculate_spread(bid_prices, ask_prices):
    return np.mean(ask_prices - bid_prices)

def calculate_depth(bid_sizes, ask_sizes, levels=5):
    return np.mean(np.sum(bid_sizes[:levels]) + np.sum(ask_sizes[:levels]))

def calculate_amihud_illiquidity(returns, volume, window=22):
    daily_illiq = np.abs(returns) / volume
    return np.mean(daily_illiq.rolling(window).mean())

def calculate_kyle_lambda(price_changes, order_flow, window=22):
    lambda_est = np.abs(price_changes / order_flow)
    return np.mean(lambda_est.rolling(window).mean())