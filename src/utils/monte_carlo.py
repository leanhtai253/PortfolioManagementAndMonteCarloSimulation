import pandas as pd
import numpy as np
from .utils import utils

class monte_carlo():
    def __init__(self, size, cov_matrix, mean_returns):
        self.size = size
        self.cov_matrix = cov_matrix
        self.mean_returns = mean_returns
    
    def get_equal_weights(self, size):
        n = 1.0 / size 
        return n
    
    def get_random_weights(self, size):
        weights = np.random.rand(size)
        weights /= np.sum(weights)
        return weights

    def generate_portfolios(self, df):
        companies = df.columns[1:]
        ports = pd.DataFrame({
            'company': pd.Series(companies)
        })
        ports['mean_return'] = self.mean_returns['mean_return']
        nr_companies = len(companies)
        port_0 = np.empty(nr_companies)
        port_0.fill(self.get_equal_weights(nr_companies))
        ports['port_0'] = pd.Series(port_0)

        random_weights = {}
        ports_columns = list(ports.columns)
        
        for i in range(self.size):
            ports_columns.append(f'port_{i+1}')
            random_weights[f'w_{i+1}'] = self.get_random_weights(nr_companies)
        
        weights_df = pd.DataFrame.from_dict(random_weights)
        ports = pd.concat([ports, weights_df], axis=1)
        ports.columns = ports_columns
        return ports 
    
    def evaluate_portfolios(self, ports, riskfree_rate=0):
        return_array = np.array(ports['mean_return'])
        port_return_list = []
        port_risk_list = []
        k = 2
        port_return_dict = {}
        port_risk_dict = {}
        for name,val in ports.items():
            if (k>0):
                k -= 1
                continue 
            port_return_dict[f're_{name}'] = utils().calculate_portfolio_returns(return_array,val)
            port_risk_dict[f'ri_{name}'] = utils().calculate_portfolio_volatility(val,
                                                                np.asarray(self.cov_matrix))

        port_expected_returns = pd.DataFrame({
            'return':port_return_dict
        }).reset_index(drop=True)
        port_volatility = pd.DataFrame({
            'risk': port_risk_dict,
        }).reset_index(drop=True)
        port_sharpe_ratios = utils().calculate_sharpe_ratio(
            port_expected_returns['return'],
            port_volatility['risk'],
            riskfree_rate
        ).reset_index(drop=True)

        ports_summary = pd.DataFrame({
            'portfolio': ports.columns[2:]
        })
        ports_summary = pd.concat([ports_summary, port_expected_returns, port_volatility], axis=1)
        ports_summary['sharpe_ratio'] = port_sharpe_ratios
        return ports_summary

            