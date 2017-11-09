from abc import ABC


class asset(ABC):
    engine=None

    @classmethod
    def set_engine(cls,engine):
        cls.engine=engine

    @classmethod
    def get_engine(cls):
        if cls.engine is None:
            raise RuntimeError('asset {}{} engine hasnt been initializeed(seted)',format(str(cls)))
        else:
            return cls.engine


    def __init__(self, catagory):
        self._catagory = catagory

    @property
    def catagory(self):
        return self._catagory

    @property
    def asset_type(self):
        return type(self)

    def ID(self):
        return 'base asset '

    def __repr__(self):
        return 'asset {}-{}'.format(self.catagory,self.ID)

    def __str__(self):
        return self.__repr__()



class stock(asset):

    def __init__(self, stockId):
        self._ID = stockId
        super(stock, self).__init__('stock')

    def __hash__(self):
        return hash(self._catagory + self.ID)

    def __eq__(self, other):
        return hash(self)==hash(other)

    @property
    def ID(self):
        return self._ID


class cash(asset):
    def __init__(self, cash_id='cny'):
        super(cash, self).__init__('cash')
        self._ID = cash_id

    def __hash__(self):
        return hash(self._catagory + self.ID)

    def __eq__(self, other):
        return hash(self)==hash(other)

    @property
    def ID(self):
        return self._ID




