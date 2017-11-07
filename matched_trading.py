from llxquant.session import session_based
from llxquant.assets import  asset
from llxquant.cons import *


class data_stream(session_based):
    def __init__(self,session,carlender_data_dict):
        super(data_stream,self).__init__(session)
        self._check_carlender_data(carlender_data_dict)
        self._data_stream=self._generate_data_stream(carlender_data_dict)
    def _check_carlender_data(self,carlender_data_dict):
        pass

    def _generate_data_stream(self,carlender_data_dict):
        pass




class order_marching_data_stream:
    def __init__(self,pricing_data_stream,on_trading_data_stream):
        self._check_data_stream(pricing_data_stream)
        self._check_data_stream(on_trading_data_stream)


    def _check_data_stream(self):
        pass

class account(session_based):
    pass

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

