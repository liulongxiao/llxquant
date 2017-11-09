from datetime import date
from llxquant.env import CARLENDER_DAILY_TYPE
class carlender_daily(list):
    def __init__(self,*args,**kwargs):
        super(carlender_daily,self).__init__(*args,**kwargs)
        self.check_data_and_sort(allow_type=(CARLENDER_DAILY_TYPE))

    def first_time(self):
        return self[0]

    def last_time(self):
        return self[-1]

    def count_time(self):
        return len(self)

    def to_list(self):
        pass

    def check_data_and_sort(self,allow_type):
        for v in self:
            assert type(v) in allow_type
        assert  set(self).__len__()==self.__len__(),'carlender contain dupicates'
        self=sorted(self)
