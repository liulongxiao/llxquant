from llxquant.context_manager import context_manager
from llxquant.utils import set_global_session, relese_global_session, get_global_session


class context_time:
    pass


class session_based:
    def __init__(self, session=None):
        if session is None:
            self.session = get_global_session()
        else:
            self.session = session


class Session(context_manager):
    def __init__(self):
        pass

    def __enter__(self):
        set_global_session(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        relese_global_session(self)


