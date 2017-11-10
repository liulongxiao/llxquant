from datetime import date,datetime
from llxquant.env import GLOBAL_SESSION
from llxquant.cons import DATE_FMT
from llxquant.assets import  stock,assets_map
from collections import OrderedDict
def set_global_session(sess):
    GLOBAL_SESSION.set_session(sess)


def get_global_session():
    return GLOBAL_SESSION.get_session()

def relese_global_session(sess):
    GLOBAL_SESSION.release_session(sess)

def max_drop_down(serial):
    if len(serial)==0:
        return 0,0
    mdd = 0
    peak = serial[0]
    peak_index=0
    drop_length=1
    for i,x in enumerate(serial):
        if x > peak:
            peak = x
            peak_index=i
        dd = (peak - x) / peak
        if dd > mdd:
            mdd = dd
            drop_length=i-peak_index

    return mdd,drop_length


def try_to_parse_date(instance):
    if isinstance(instance,date):
        return instance
    if isinstance(instance,str):
        return datetime.strptime(instance,DATE_FMT).date()
    if isinstance(instance,datetime):
        return instance.date()
    if hasattr(instance,date):
        parsed_date=instance.date()
        if isinstance(parsed_date,date):
            return parsed_date
    raise TypeError('cannot convert instance to date type ')


def transform_rawdict_to_formed(data_dict):
    result=OrderedDict()
    for k,v in data_dict.items():
        if stock(k) not in result.keys():
            result[stock(k)]=OrderedDict()
        for thedate,inner_data in v.items():
            result[stock(k)][try_to_parse_date(thedate)]=inner_data
    return result


def transform_rawdf_to_formed(df):
    """df shou have columns :ID,data,thetime"""
    assert 'ID' in df.columns
    assert 'data' in df.columns
    assert 'thetime' in df.columns
    groups=df.groupby('ID').apply(lambda x:x[['thetime','data']].set_index('thetime').to_dict()['data']).to_dict()
    final=transform_rawdict_to_formed(groups)
    return final


def generate_all_like(data_dict,n):
    result=OrderedDict()
    for k,v in data_dict.items():
        if k not in result.keys():
            result[k]=OrderedDict()
        for inner_date,inner_data in v.items():
            result[k][inner_date]=n
    return result