from datetime import date,datetime
from llxquant.env import GLOBAL_SESSION
from llxquant.cons import DATE_FMT
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
    if isinstance(instance,str):
        return datetime.strptime(instance,DATE_FMT).date()
    if isinstance(instance,datetime):
        return instance.date()
    if hasattr(instance,date):
        parsed_date=instance.date()
        if isinstance(parsed_date,date):
            return parsed_date
    raise TypeError('cannot convert instance to date type ')
