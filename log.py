from llxquant.session import session_based
class Logger(session_based):
    """simple logger class."""

    level_mapping = dict(DEBUG=0, INFO=1, WARN=2, ERROR=3)

    def __init__(self, session=None, log_level='INFO'):
        super(Logger, self).__init__(session)
        self.context=self.session
        self.level = self.level_mapping.get(log_level, 0)

    @property
    def _time(self):
        return str(self.context.get_time())

    def debug(self, string):
        if self.level > self.level_mapping['DEBUG']:
            return
        print('[DEBUG ' + self._time + '] ' + string)

    def info(self, string):
        if self.level > self.level_mapping['INFO']:
            return
        print('[INFO ' + self._time + '] ' + string)

    def warn(self, string):
        if self.level > self.level_mapping['WARN']:
            return
        print('[WARN ' + self._time + '] ' + string)

    def error(self, string):
        if self.level > self.level_mapping['ERROR']:
            return
        print('[ERROR ' + self._time + '] ' + string)