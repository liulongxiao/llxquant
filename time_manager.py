from llxquant.session import Session


class Time_manager:
    def __init__(self, frequence='d', carlender=None):
        self.frequance = frequence
        self.carlender = carlender

    def set_current_time(self, thetime):
        self.check_time(thetime)
        self.current_time = thetime

    def get_current_time(self):
        if self.current_time is None:
            raise ValueError('current time is not initialized')
        return self.current_time

    def check_time(self, thetime):
        if not (self.carlender is None):
            if thetime not in self.carlender:
                raise ValueError('time not in carlenders')


class Time_manager_session(Session):
    def __init__(self, time_manager):
        self.time_manager = time_manager
        super(Time_manager_session, self).__init__()

    def get_time(self):
        return self.time_manager.get_current_time()

    def set_time(self, current_time):
        self.time_manager.set_current_time(current_time)


        # def __enter__(self,current_time=None):
        #     super(Time_manager_session,self).__enter__()
        #     if current_time is None:
        #         raise NotImplemented('havent implemented None current time')
        #     else:
        #         self.time_manager.set_current_time(current_time)
        #
        # def __exit__(self, exc_type, exc_val, exc_tb):
        #     super(Time_manager_session, self).__exit__(self, exc_type, exc_val, exc_tb)
        #     self.time_manager.set_current_time(None)
