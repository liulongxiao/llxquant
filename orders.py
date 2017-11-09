from llxquant.cons import *
from llxquant.assets import  asset,cash,stock
from llxquant.position import  position

class order:
    def __init__(self,asset_instance,order_volume,direction_flag):
        assert issubclass(asset_instance.asset_type,asset)
        assert direction_flag in DIRECTIONS
        self._asset_instance=asset_instance
        self._asset_type=asset_instance.asset_type
        self._direction_flag =direction_flag
        self._order_volume=order_volume

    @property
    def asset_type(self):
        return self.asset._asset_type

    @property
    def direction_flag(self):
        return self._direction_flag

    @property
    def order_volume(self):
        return self._order_volume

    @order_volume.setter
    def order_volme(self,order_volume):
        assert  order_volume>0
        self._order_volume=order_volume

    @property
    def asset_instance(self):
        return self._asset_instance

    def __repr__(self):
        return 'Asset :{} ,amount {} flag {}'.format(self.asset_instance,self.order_volme,self.direction_flag)


def generate_orders_from_positions(older_position,new_position):
    orders=[]
    for asset_instance,amount in older_position.items():
        if isinstance(asset_instance,cash):continue
        if asset_instance not in new_position.keys():
            orders.append(order(asset_instance,older_position[asset_instance],ASK))
        elif older_position[asset_instance]>new_position[asset_instance]:
            orders.append(order(asset_instance,older_position[asset_instance]-new_position[asset_instance],ASK))
        elif older_position[asset_instance]<new_position[asset_instance]:
            orders.append(order(asset_instance,new_position[asset_instance]-older_position[asset_instance],BID))
    for asset_instance,amount in new_position.items():
        if isinstance(asset_instance, cash): continue
        if asset_instance not in older_position.keys():
            orders.append(order(asset_instance,amount,BID))
    orders=sorted(orders,key=lambda x:x.direction_flag)
    return orders


if __name__=='__main__':
    position1=position(init_cash=1000000)
    position2=position(init_cash=1000000)
    position1.add_asset(stock('600233'),100)
    position1.add_asset(stock('600232'), 10)

    position2.add_asset(stock('600233'), 10)
    position2.add_asset(stock('600234'), 10)
    orders=generate_orders_from_positions(position1,position2)
    orders[2]
