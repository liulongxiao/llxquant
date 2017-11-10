import pandas as pd
from llxquant.session import  session_based
from llxquant.time_manager import Time_manager_session,Time_manager
from collections import OrderedDict
from llxquant.log import Logger
from llxquant.graph import plot_charts_with_market_value
from llxquant.assets import stock,cash,asset
from llxquant.position import position
from llxquant.engines import  market_engine,stock_engine,asset_engine_map
from collections import OrderedDict
from llxquant.carlender import carlender_daily
from llxquant.orders import generate_orders_from_positions
from llxquant.utils import transform_rawdf_to_formed
from copy import deepcopy


def merge_dict(dict1,dict2):
    result=OrderedDict()
    for k,v in dict1.items():
        if k not in result.keys():
            result[k]=v
        else:
            result[k]+=v
    for k,v in dict2.items():
        if k not in result.keys():
            result[k]=v
        else:
            result[k]+=v
    return result

def find_most_recent(value,value_ordereddict):
    current=None
    for k,v in value_ordereddict.items():
        if k<=value:
            current=v
        else:
            return current
    return v


class back_test(session_based):
    def __init__(self,stock_universe,carlender,initial_capital=1000000,tax_rate_and_commission=0.002):
        """warning! carlender must be sorted"""
        session=Time_manager_session(Time_manager(carlender=carlender))
        super(back_test,self).__init__(session)
        self.stock_universe=stock_universe
        self.carlender=carlender
        self.initial_capital=initial_capital
        self.tax_rate_and_commission=tax_rate_and_commission
        self.pre_load()
        self.positions_percent=OrderedDict()
        self.market_value=OrderedDict()
        self.position=OrderedDict()
        self.log=Logger(self.session)
        self.tmp_cash=OrderedDict()

    def pre_load(self):
        """ usr counld overwrite this method to load features"""
        pass

    def regist_trade_price(self,trade_price,on_trading):
        self.trade_price=trade_price
        self.on_trading=on_trading

    def update_trade_carlender(self,actual_trade_carlender):
        self.actual_trade_carlender=actual_trade_carlender

    def get_current_date(self):
        return self.session.get_time()

    def generate_position_percent(self):
        """"this method should written by user to implement stratege"""
        pass


    def generate_position(self,position_percent,market_value,last_position,thetime=None):


        if thetime is None:
            thetime = self.session.get_time()

        ####找到停牌不能卖出的仓位
        remain_position = OrderedDict()
        for k, v in last_position.items():
            if self.on_trading[(k, thetime)] == 0:
                remain_position[k] = v

        remain_value = self.calculate_market_value(remain_position)
        ##当前可用的资金为总市值减去不能卖出股票的市值
        market_value -= remain_value
        position = OrderedDict()

        self.tmp_cash[thetime] = 0
        for k,v in position_percent.items():
            try:
                position[k]=market_value*v/self.trade_price[(k,thetime)]
            except KeyError as e:
                self.log.error(self.__repr__()+e.__repr__())
                self.tmp_cash[thetime]+=market_value*v

        ##合并生成总仓位
        return merge_dict(position,remain_position)

    def calculate_market_value(self,current_position,thetime=None):
        """""
        根据一定的持仓计算出 市值，如果停牌则用最后一天的股价计算市值
        """
        if thetime is None:
            thetime=self.session.get_time()
        market_value=0
        for k,v in current_position.items():
            market_value+=v*self.trade_price[(k,thetime)]
        return market_value


    def fresh_position(self,position_percent,thetime=None):
        """"
        将停牌股票的买入percent归零
        """
        if thetime is None:
            thetime=self.session.get_time()
        ##############注意迭代过程中不能动态删除
        thekeys=list(position_percent.keys())
        for k in thekeys:
            if self.on_trading[(k,thetime)]==0:
                del position_percent[k]

        ###如果全部为0，则返回0的dict，如果不全部为0，标准化和为1
        value_sum= sum(position_percent.values())
        if value_sum!=0:
            for k,v in position_percent.items():
                position_percent[k]/=value_sum
        return position_percent


    def generate_carlender_marketvalues(self):
        carlender_market_values=OrderedDict()
        for thedate in self.carlender:
            position=find_most_recent(thedate,self.position)
            tmp_cash=find_most_recent(thedate,self.tmp_cash)
            if position is None :
                carlender_market_values[thedate]=self.initial_capital
            else:
                carlender_market_values[thedate]=tmp_cash+self.calculate_market_value(position,thetime=thedate)
        return carlender_market_values




    def back_test(self):
        last_position=OrderedDict()
        for trade_date in self.actual_trade_carlender:
            ####设置时间戳
            self.session.set_time(trade_date)
            ####生成当前时间点的market_value 注意停牌股票用的最近一个交易日的价格
            if len(self.market_value)==0:
                self.market_value[trade_date]=self.initial_capital
            else:
                self.market_value[trade_date]=self.calculate_market_value(self.position[last_trade_date])+self.tmp_cash[last_trade_date]

            ##############生成当前时间点的position percent，并进行处理。

            self.positions_percent[trade_date] =self.fresh_position(self.generate_position_percent())
            self.position[trade_date]=self.generate_position(self.positions_percent[trade_date],self.market_value[trade_date],last_position)
            last_trade_date=trade_date
        ###生成总的carlender return
        market_value=pd.Series(self.generate_carlender_marketvalues())
        plot_charts_with_market_value(market_values=market_value)


class BackTest(session_based):
    def __init__(self,carlender, asset_field=[stock],initial_capital=1000000, tax_rate_and_commission=0.002):
        """warning! carlender must be sorted"""
        session = Time_manager_session(Time_manager(carlender=carlender))
        super(BackTest, self).__init__(session)
        self.carlender=carlender
        self.session.set_time(carlender.first_time())
        with self.session.as_default():
            self.current_pisition=position(init_cash=initial_capital)
            self.market_engine=market_engine()
            for asset_type in asset_field:
                self.market_engine.set_engine(asset_type,asset_engine_map[asset_type]())
            self.pre_load()
        self.position_log=OrderedDict()
        self.market_value=OrderedDict()

    def pre_load(self):
        """method to be overwrite to preload data or feature """
        raise  NotImplemented()


    def generate_trade_carlender(self):
        """method to be overwrite to generate the actual trade carlender (days that contain orders)"""
        self.trade_carlender=self.carlender


    def _generate_position_percent(self):
        target_position_percent=self.generate_position_percent()
        for key in target_position_percent.keys():
            assert  issubclass(type(key),asset)
        return target_position_percent

    # def load_engine_pricing_data(self,datasource,from_raw=False):
    #     with self.session.as_default():
    #         for engine in self.market_engine.asset_engine_dict.values():
    #             if from_raw:
    #                 engine.load_marketing_data(transform_raw_to_formed(engine.load_marketing_data(datasource[engine.asset_type])))
    #             else:
    #                 engine.load_marketing_data(datasource[engine.asset_type])

    def generate_position(self):
        target_position_percent=self._generate_position_percent()
        target_position=self.market_engine.to_target_percent(self.current_pisition,target_position_percent)
        return target_position



    def back_test(self):
        with self.session.as_default():
            for current_time in self.trade_carlender:
                """use tmp to catch internal positions"""
                tmp_position=deepcopy(self.current_pisition)

                self.session.set_time(current_time)
                target_position=self.generate_position()
                orders_to_apply=generate_orders_from_positions(older_position=self.current_pisition,new_position=target_position)
                for order in orders_to_apply:
                    self.current_pisition.check_order(order)
                    tmp_position=self.market_engine.apply_order(order,tmp_position)
                self.position_log[current_time]=tmp_position
                self.current_pisition=tmp_position


if __name__=='__main__':
    class my_test(BackTest):
        def generate_position_percent(self):
            return """Asset(stockId):percent """

    test=my_test(initial_capital=100)
    test.back_test()
