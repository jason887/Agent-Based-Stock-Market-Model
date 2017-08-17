"""This file runs tests for all functions in agents"""
import pytest

from stockmarket.limitorderbook import *
from stockmarket.agent import Trader
from stockmarket.firms import Firm
from stockmarket.stock import Stock
from stockmarket.valuationfunctions import *
from numpy.testing import assert_equal

@pytest.fixture()
def agents():
    return [Trader("Agent1", 1000, 0, 2, 3, 5, lambda **x: extrapolate_average_profit(**x), propensity_to_switch=1.1),
            Trader("Agent2", 1000, 0, 2, 3, 5, lambda **x: extrapolate_ma_price(**x), propensity_to_switch=1.1)]

@pytest.fixture()
def limitorderbooks():
    # create a firm
    firm = Firm("Firm1", 10000, [200, 300, 400, 300])
    # create a stock of that firm
    stocks = Stock(firm, 1000)
    return [LimitOrderBook(stocks, 100, 120)]

def test_add_bid(limitorderbooks):
    limitorderbooks[0].add_bid(10, 20, 'trader-1')
    limitorderbooks[0].add_bid(5, 20, 'trader-2')
    limitorderbooks[0].add_bid(7, 20, 'trader-3')
    limitorderbooks[0].add_bid(7, 20, 'trader-4')
    limitorderbooks[0].add_bid(7, 20, 'trader-5')
    # highest bid is 10
    assert_equal(limitorderbooks[0].bids[-1].price, 10)
    # lowest bid is 5
    assert_equal(limitorderbooks[0].bids[0].price, 5)
    # second highest bid trader = trader-2
    assert_equal(limitorderbooks[0].bids[-2].owner, 'trader-3')

def test_add_ask(limitorderbooks):
    limitorderbooks[0].add_ask(11, 20, 'trader-1')
    limitorderbooks[0].add_ask(5, 20, 'trader-2')
    limitorderbooks[0].add_ask(7, 20, 'trader-3')
    limitorderbooks[0].add_ask(7, 20, 'trader-4')
    limitorderbooks[0].add_ask(7, 20, 'trader-5')
    # highest ask is 11
    assert_equal(limitorderbooks[0].asks[-1].price, 11)
    # lowest ask is 5
    assert_equal(limitorderbooks[0].asks[0].price, 5)
    # second highest ask trader = trader-5
    assert_equal(limitorderbooks[0].asks[-2].owner, 'trader-5')

def test_clean_book(limitorderbooks):
    limitorderbooks[0].add_bid(10, 20, 'trader-1')
    limitorderbooks[0].add_bid(5, 20, 'trader-2')
    limitorderbooks[0].add_ask(11, 20, 'trader-1')
    limitorderbooks[0].add_ask(5, 20, 'trader-2')
    for n in range(119):
        limitorderbooks[0].clean_book()
    assert_equal(len(limitorderbooks[0].bids), 2)
    assert_equal(len(limitorderbooks[0].asks), 2)
    limitorderbooks[0].clean_book()
    assert_equal(len(limitorderbooks[0].bids), 0)
    assert_equal(len(limitorderbooks[0].asks), 0)

def test_match_orders(limitorderbooks):
    # add some asks
    limitorderbooks[0].add_ask(5, 20, 'trader-2')
    limitorderbooks[0].add_ask(7, 20, 'trader-3')
    limitorderbooks[0].add_ask(7, 20, 'trader-4')
    limitorderbooks[0].add_ask(7, 20, 'trader-5')
    # and bids
    limitorderbooks[0].add_bid(10, 20, 'trader-1')
    limitorderbooks[0].add_bid(4, 20, 'trader-11')
    limitorderbooks[0].add_bid(9, 20, 'trader-11')
    matched_orders = limitorderbooks[0].match_orders()
    # after an orderbook match both order books are reduced by 1
    assert_equal(len(limitorderbooks[0].bids), 2)
    assert_equal(len(limitorderbooks[0].asks), 3)
    # and the highest bid was matched to the lowest ask, difference is 5
    assert_equal(matched_orders[2].price - matched_orders[3].price, 5)
    # the second match is bid p9 and ask p7, difference is 2
    matched_orders = limitorderbooks[0].match_orders()
    assert_equal(matched_orders[2].price - matched_orders[3].price, 2)
    # Once again the order books are reduced by 1 in size
    assert_equal(len(limitorderbooks[0].bids), 1)
    assert_equal(len(limitorderbooks[0].asks), 2)
    # then no more match is possible
    matched_orders = limitorderbooks[0].match_orders()
    assert_equal(matched_orders, None)
    for n in range(500):
        limitorderbooks[0].clean_book()
    limitorderbooks[0].add_ask(5, 10, 'trader-2')
    limitorderbooks[0].add_ask(7, 8, 'trader-3')
    limitorderbooks[0].add_bid(10, 20, 'trader-1')
    # first match should reduce asks book by 1
    matched_orders = limitorderbooks[0].match_orders()
    assert_equal(len(limitorderbooks[0].bids), 1)
    assert_equal(len(limitorderbooks[0].asks), 1)
    assert_equal(matched_orders[2].price - matched_orders[3].price, 5)
    # the bid should have a remaining volume of 10
    assert_equal(limitorderbooks[0].bids[0].volume, 10)
    # second match
    matched_orders = limitorderbooks[0].match_orders()
    # should reduce the lenght of the asks book to zero and bids should remain 1
    assert_equal(len(limitorderbooks[0].bids), 1)
    assert_equal(len(limitorderbooks[0].asks), 0)
    # the bid should have a remaining volume of 2
    assert_equal(limitorderbooks[0].bids[0].volume, 2)
    # price should be 7 and volume 8
    assert_equal(matched_orders[0], 7)
    assert_equal(matched_orders[1], 8)
    # no more matches should be possible, leaving the order in the orderbook
    assert_equal(limitorderbooks[0].match_orders(), None)
