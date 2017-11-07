from llxquant.errors import EMPTY_GLOBAL_SESSION_ERROR



class GLOBAL_SESSION:
    sessions=list()
    @classmethod
    def release_session(cls):
        if len(cls.sessions)>0:
            cls.sessions.pop()
        else:
            raise EMPTY_GLOBAL_SESSION_ERROR('global sessions list is empty')

    @classmethod
    def set_session(cls,session):
        cls.sessions.append(session)
    @classmethod
    def get_session(cls):
        if len(cls.sessions)>0:
            return cls.sessions[-1]
        else:
            raise EMPTY_GLOBAL_SESSION_ERROR('global sessions list is empty')

RISK_FREE_RATE=0.03

