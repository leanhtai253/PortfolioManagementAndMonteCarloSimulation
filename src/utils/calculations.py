from functools import reduce
import os
import pandas as pd
import numpy as np

class calculations:
    @staticmethod
    def log_return(prices):
        '''
        Return log-standardized daily return
        Input: a df column of price values
        Return pd.Series
        '''
        log_return = np.log(prices / prices.shift(1))
        return pd.Series(log_return)
    
    @staticmethod
    def mean_return(prices):
        return prices.mean() * 252

    @staticmethod
    def correlation_matrix(df):
        return df.corr()

    @staticmethod
    def covariance_matrix(df):
        return df.cov() * 252

    @staticmethod
    def portfolio_risk(w_matrix, corr_matrix):
        return np.sqrt(reduce(np.matmul, [w_matrix, corr_matrix, w_matrix.T]))
    
    @staticmethod
    def portfolio_mean_returns(val, w):
        return np.matmul(val, w)

    @staticmethod
    def sharpe_ratio(mean_return, volatility, riskfree_rate):
        return (mean_return - riskfree_rate) / volatility 
    
    @staticmethod
    def port_max_sharpe_ratio(df):
        return df.iloc[[df['sharpe_ratio'].idxmax()]]
    
    @staticmethod
    def port_min_risk(df):
        return df.iloc[[df['risk'].idxmin()]]

    @staticmethod 
    def port_equal_allocations(df):
        return df.iloc[[0]]

    @staticmethod
    def get_allocations_by(df1,df2, func):
        temp_df = func(df1)
        index = temp_df.index.values[0]
        return df2.iloc[:, [0,index+2]]

    @staticmethod
    def allocations_max_sharpe_ratio(df1,df2):
        return calculations.get_allocations_by(
                df1, df2,
                calculations.port_max_sharpe_ratio)

    @staticmethod 
    def allocations_min_risk_ratio(df1, df2):
        return calculations.get_allocations_by(
            df1, df2,
            calculations.port_min_risk
        )
    
    @staticmethod 
    def allocations_equal(df1,df2):
        return calculations.get_allocations_by(
            df1, df2,
            calculations.port_equal_allocations
        )
