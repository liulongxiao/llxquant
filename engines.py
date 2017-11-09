from abc import ABC,abstractmethod
from llxquant.session import  session_based
from llxquant.errors import  ENGINE_NOT_FOUND_ERROR
from llxquant.assets import  asset,stock,cash
from llxquant.cons import *
from collections import OrderedDict
import numpy as np
from copy import deepcopy

class asset_engine(session_based,ABC):
    def __init__(self,asset_type,session=None):
        super(asset_engine,self).__init__(session)
        assert issubclass(asset_type,asset)
        self._asset_type=asset_type

    def is_engine(self,asset):
        if self._asset_type==asset:
            return True
        else:
            return False


    @property
    def asset_type(self):
        return self._asset_type

    @abstractmethod
    def load_marketing_data(self,pricing_data_dict):
        raise NotImplemented()

    @abstractmethod
    def apply_order(self,order,position):
        raise NotImplemented()

    @property
    def asset_type(self):
        return self._asset_type

class stock_engine(asset_engine):
    def __init__(self,session=None):
        super(stock_engine,self).__init__(stock,session)


    def load_marketing_data(self,pricing_data_dict):
        """pricing_data_dict should be a session_based data object"""
        for KEY in STOCK_PRICING_DATA_KEY:
            assert pricing_data_dict[KEY].session==self.session
            setattr(self,KEY,pricing_data_dict[KEY])


    def apply_order(self,order,position):
        position=deepcopy(position)
        current_price=getattr(self,PRICE).get_data(order._asset_instance)
        if order.direction_flag==BID:
            bid_amount=min(order.order_volme,position.get_cash()//current_price,0 if not getattr(self,ON_TRADING).get_data(order._asset_instance) else np.inf,
                           0 if  getattr(self, IS_LIMITUP).get_data(order._asset_instance) else np.inf)
            cash_consume=bid_amount*current_price
            position.add_asset(order._asset_instance,bid_amount)
            position.reduce_cash(cash_consume)
            return position
        elif order.direction_flag==ASK:
            ask_amount=min(order._order_volume,0 if not getattr(self,ON_TRADING).get_data(order._asset_instance) else np.inf, 0 if  getattr(self, IS_LIMITDOWN).get_data(order._asset_instance) else np.inf)
            cash_gain=ask_amount*current_price
            position.reduce_asset(order._asset_instance,ask_amount)
            position.add_cash(cash_gain)
        return position

class market_engine(session_based):
    def __init__(self,session):
        super(market_engine, self).__init__(session)
        self.asset_engine_dict=dict()

    def set_engine(self,_asset_type,asset_engine_):
        assert issubclass(asset_engine_,asset_engine)
        assert asset_engine_.is_engine(_asset_type)
        assert issubclass(_asset_type,asset)
        ##存储engine
        self.asset_engine_dict[_asset_type]=asset_engine_

    def find_engine(self,asset_type):
        if asset_type not in self.asset_engine_dict.keys():
            raise  ENGINE_NOT_FOUND_ERROR('engine for {} not found in market_engine'.format(asset_type))
        else:
            return self.asset_engine_dict[asset_type]

    def apply_order(self,order,position):
        engine_to_apply=self.find_engine(order.asset_type)
        newposition=engine_to_apply.apply_order(order,position)
        return newposition

    def calculate_market_value(self,position):
        market_value=0
        for asset,amount in position.items():
            market_value+=self.find_engine(asset.asset_type).calculate_market_value(asset)
        return market_value

    def asset_pricing(self,asset_instance):
        engine_to_apply = self.find_engine(asset_instance.asset_type)
        return getattr(engine_to_apply,PRICE).get_data(asset_instance)

    def max_amout_can_ask(self,asset_instance,position):
        pass

    def max_amount_can_bid(self,asset_instance,position):
        pass

    def to_target_percent(self,position,target_percent_position):
        target_position=OrderedDict()
        market_value=self.calculate_market_value(position)
        for k,v in target_percent_position:
            if isinstance(k,cash):
                cash_=k
                continue
            target_position[k]=(v*market_value)//self.asset_pricing(k)
        target_position[cash_]=market_value-self.calculate_market_value(target_position)
        return target_position


asset_engine_map={stock:stock_engine}






