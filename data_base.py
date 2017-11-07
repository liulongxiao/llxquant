from llxquant.session import session_based
from llxquant.assets import asset,stock
from abc import ABC,abstractmethod

class DataBase(session_based,ABC):
    def __init__(self, session=None):
        super(DataBase, self).__init__(session)
        self.data=dict()

    @abstractmethod
    def _load_data(self, datasource):
        pass


class DfFeature(DataBase):
    def __init__(self, datasource, session=None):
        super(DfFeature, self).__init__(session)
        self._load_data(datasource)

    def _load_data(self, datasource):
        """data source must have thetime columns"""
        import pandas as pd
        if not isinstance(datasource, pd.DataFrame):
            raise TypeError('DfFeature must loaded from pd.DataFrame')
        self.data = datasource

    def _filter(self, data):
        current_time = self.session.time_manager.get_current_time()
        return data[data['thetime'] < current_time]

    def get_data(self):
        return self._filter(self.data)


class PRICING_DATA_STOCK(DataBase):
    def __init__(self, name,session=None):
        self.name=name
        super(PRICING_DATA_STOCK, self).__init__(session)

    def get_data(self,asset_instance,thetime=None):
        if thetime is None:
            thetime=self.session.get_time()
        return self.data[(asset_instance,thetime)]

    def _load_data(self, datasource):
        """datasource should be stockId(str):calender(datetime.date):data recursive dict"""
        for stockId,values in datasource.items():
            for thedate,inner_data in values.items():
                self.data[(stock(stockId),thedate)]=inner_data


if __name__=='__main__':
    import tushare as ts
    from llxquant.time_manager import Time_manager,Time_manager_session
    import pandas as pd
    df1=ts.get_k_data('600233').set_index('date').close
    df2=ts.get_k_data('600104').set_index('date').close
    d=df1.to_dict()
    x={'600233':d}
    x['600104']=df2.to_dict()
    sess=Time_manager_session(Time_manager(carlender=list(pd.date_range('2017-11-01','2017-11-07').map(lambda x:str(x.date())))))
    F=PRICING_DATA_STOCK(name='close',session=sess)
    F._load_data(x)
    sess.set_time('2017-11-06')
    F.get_data(stock('600233'))
