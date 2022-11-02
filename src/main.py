from utils.utils import utils as utils
from utils.monte_carlo import monte_carlo
from utils.plots import plots
# SOME SETTINGS
RAW_DATA = '../data/raw'
PROCESSED_DATA = '../data/processed'
FINAL_DATA = '../data/final'
SAVE_NAME = 'final_data.csv'
util = utils()
util.set_params(RAW_DATA, PROCESSED_DATA, FINAL_DATA, SAVE_NAME)
plot = plots()
# GET DATA
util.prepare_data()
df = util.load_final_data()
df = df[1:]

# FIND CORRELATION MATRIX
# corr_matrix = util.correlation_matrix(df)
cov_matrix = util.covariance_matrix(df)
# CALCULATE EXPECTED RETURNS OF EACH COMPANY
mean_returns = util.mean_returns_by_company(df)

# SET NUMBER OF SIMULATED PORTFOLIOS
n_simulations = 10000
# INITIALIZE MONTE CARLO MODEL
mc = monte_carlo(n_simulations, cov_matrix, mean_returns)
# GENERATE PORTFOLIOS
ports = mc.generate_portfolios(df)
# EVALUATE EACH PORTFOLIO BASED ON ITS EXPECTED RETURN, RISK, AND SHARPE RATIO
ports_summary = mc.evaluate_portfolios(ports, riskfree_rate=0)

# FIND PORTFOLIO WITH HIGHEST SHARPE RATIO
port_max_sharpe = util.port_with_max_sharpe(ports_summary)
# FIND PORTFOLIO WITH LOWEST RISK
port_min_risk = util.port_with_min_risk(ports_summary)
# PORTFOLIO THAT HAVE EQUAL ALLOCATIONS OF SHARES
port_equal = util.port_with_equal(ports_summary)

# FIND SPECIFIC PERCENTAGE OF ALLOCATIONS FOR THOSE THREE PORTFOLIOS
allo_max_sharpe = util.allocations_max_sharpe(ports_summary, ports)
allo_min_risk = util.allocations_min_risk(ports_summary, ports)
allo_equal = util.allocations_equal(ports_summary, ports)
main_ports = util.extract_main_ports(port_max_sharpe, port_min_risk, port_equal)

# PLOTS
scatter_portfolios_plot = plot.scatter_plot_portfolios(ports_summary, main_ports)
all_daily_returns_plot = plot.plot_all_daily_returns(df)
corr_matrix_vs = plot.visualize_corr_matrix(util.correlation_matrix(df))