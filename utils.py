from .env import GLOBAL_SESSION
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