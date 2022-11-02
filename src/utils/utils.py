from .data_processing import dp
from .calculations import calculations as calculate
import pandas as pd
import numpy as np
import os
from functools import reduce

class utils:
    def __init__(self):
        pass
    def set_params(self, RAW_PATH, PROCESSED_PATH, FINAL_PATH, SAVE_NAME):
        self.raw_path = RAW_PATH
        self.processed_path = PROCESSED_PATH
        self.final_path = FINAL_PATH
        self.save_name = SAVE_NAME


    def load_final_data(self, save_name=None):
        if save_name is None:
            save_name = self.save_name
        return pd.read_csv(os.path.join(self.final_path, save_name))
    
    def prepare_data(self, save_name=None):
        dp.transform_data(self.raw_path, self.processed_path, self.calculate_daily_log_return)
        if save_name is None: save_name = self.save_name
        dp.final_data(self.processed_path, self.final_path, save_name)
        print('Data prepration done')

    def calculate_mean_return(self, prices):
        return calculate.mean_return(prices)
    
    def calculate_daily_log_return(self, prices):
        return calculate.log_return(prices)

    def correlation_matrix(self, df):
        return calculate.correlation_matrix(df[df.columns[1:]])

    def covariance_matrix(self, df):
        return calculate.covariance_matrix(df[df.columns[1:]])

    def mean_returns_by_company(self, df):
        '''
        Calculate expected return of each company
        Input: dataframe
        Return: dataframe
        '''
        mean_returns = []
        for col in df.columns[1:]:
            mean_returns.append(self.calculate_mean_return(df[col]))

        mean_returns_df = pd.DataFrame({
            'name':df.columns[1:],
            'mean_return': pd.Series(mean_returns)
        })    
        return mean_returns_df

    def calculate_portfolio_volatility(self, w, corr):
        return calculate.portfolio_risk(w, corr)
    
    def calculate_portfolio_returns(self, val, w):
        return calculate.portfolio_mean_returns(val, w)
    
    def calculate_sharpe_ratio(self, mean_return, volatility, riskfree_rate):
        return calculate.sharpe_ratio(mean_return, volatility, riskfree_rate)

    def port_with_max_sharpe(self, df):
        return calculate.port_max_sharpe_ratio(df)
    
    def port_with_min_risk(self, df):
        return calculate.port_min_risk(df)

    def port_with_equal(self, df):
        return calculate.port_equal_allocations(df)
    
    def allocations_max_sharpe(self, df1, df2):
        return calculate.allocations_max_sharpe_ratio(df1, df2)
    
    def allocations_min_risk(self, df1, df2):
        return calculate.allocations_min_risk_ratio(df1, df2)

    def allocations_equal(self, df1, df2):
        return calculate.allocations_equal(df1, df2)
    
    def extract_main_ports(self, max_sharpe, min_risk, equal):
        main_ports = reduce(lambda x,y : pd.concat([x, y], axis=0), [max_sharpe, min_risk, equal])
        return main_ports