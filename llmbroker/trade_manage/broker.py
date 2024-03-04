from llmbroker import OrderBrokerBase
from llmbroker import Datetime


class OrderBrokerWrap(OrderBrokerBase):
    
    def __init__(self, broker, slip=0.03):
        
        super(OrderBrokerWrap, self).__init__()
        self._broker = broker
        self._slip = slip

    def _buy(self, datetime, market, code, price, num):
        self._broker.buy('{}{}'.format(market, code), price, num)
        return datetime

    def _sell(self, datetime, market, code, price, num):
        self._broker.sell('{}{}'.format(market, code), price, num)
        return datetime


class TestOrderBroker:
    def __init__(self):
        pass

    def buy(self, code, price, num):
        print("买入：%s  %.3f  %i" % (code, price, num))

    def sell(self, code, price, num):
        print("卖出：%s  %.3f  %i" % (code, price, num))


def crtOB(broker, slip=0.03):
    return OrderBrokerWrap(broker, slip)