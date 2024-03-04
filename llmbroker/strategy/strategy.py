from llmbroker import StrategyBase, Query
from llmbroker import StrategyContext, StockManager


class TestStrategy(StrategyBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.stock_list = ['sh000001', 'sz000001']
        self.ktype_list = [Query.MIN, Query.DAY]

    @staticmethod
    async def on_bar(self, ktype):
        print("on bar {}".format(ktype))
        print("{}".format(len(StockManager.instance())))
        sm = StockManager.instance()
        for s in sm:
            print(s)


if __name__ == '__main__':
    s = TestStratege()
    s.run()
