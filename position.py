from llxquant.assets import asset,cash
from llxquant.cons import *

class position(dict):
    def __init__(self,init_position=None,init_cash=None,init_cash_id='cny'):
        self.cash_id=init_cash_id
        if not((init_position is None)^ (init_cash is None)):
            raise ValueError('only take one init parameter with init_position or init_cash ')
        if not init_cash is None :
            self.init_with_cash(init_cash)
        else:
            self.init_with_position(init_position)

    def init_with_cash(self,init_cash):
        self[cash(self.cash_id)]=init_cash

    def init_with_position(self,position):
        for assert_instance,amount in position.items():
            assert issubclass(assert_instance.asset_type,asset)
            self[assert_instance]=amount
        if cash(self.cash_id) not in position.keys():
            self[cash(self.cash_id)]=0

    def check_order(self,order_):
        if order_._direction_flag==BID:
            return order_.order_volme>0,order_
        elif order_._direction_flag==ASK:
            return  order_.order_volme>0,order_ if order_.order_volme<=self[order_.asset_instance] else order(order_.asset_instance,self[order_.asset_instance],order_.direction_flag)
        else:
            raise NotImplemented('order with flag {}'.format(order_._direction_flag))

    def reduce_cash(self,amount):
        self[cash(self.cash_id)]-=amount

    def add_cash(self,amount):
        self[cash(self.cash_id)] += amount

    def add_asset(self,asset_instance,amount):
        assert  amount>0
        if asset_instance in self.keys():
            self[asset_instance]+=amount
        else:
            self[asset_instance] = amount

    def reduce_asset(self,asset_instance,amount):
        assert  amount>0
        assert  isinstance(amount,int)
        self[asset_instance]-=amount

    def get_cash(self):
        return self[cash(self.cash_id)]


if __name__=='__main__':
    from llxquant.assets import stock

