from stockmarket import baselinemodel
from numpy.testing import assert_equal

def test_baselinemodel():
    """Check if the baseline model runs"""
    agents, firms, stocks, order_books = baselinemodel.stockMarketSimulation(seed=0,
                                                                         simulation_time=30,
                                                                         init_backward_simulated_time=200,
                                                                         number_of_agents=100,
                                                                         share_chartists=0.5,
                                                                         share_mean_reversion=0.5,
                                                                         amount_of_firms=1,
                                                                         initial_total_money=(26000,28000),
                                                                         initial_profit=(1000, 1000),
                                                                         discount_rate=0.17,
                                                                         init_price_to_earnings_window=((13, 16), (21, 24)),
                                                                         order_expiration_time=200,
                                                                         agent_order_price_variability=(1,1),
                                                                         agent_order_variability=1.5,
                                                                         agent_ma_short=(20, 40),
                                                                         agent_ma_long=(120, 150),
                                                                         agents_hold_thresholds=(0.9995, 1.0005),
                                                                         agent_volume_risk_aversion=0.1,
                                                                         agent_propensity_to_switch=1.1,
                                                                         firm_profit_mu=0.058,
                                                                         firm_profit_delta=0.00396825396,
                                                                         firm_profit_sigma=0.125,
                                                                         profit_announcement_working_days=20,
                                                                         mean_reversion_memory_divider=4,
                                                                         printProgress=False,
                                                                         )
    assert_equal(len(agents), 100)
