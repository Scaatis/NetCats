import sys

class _states(object):
    def __init__(self):
        self._num = 0
    
    def __getattr__(self, name):
        setattr(self, name, self._num)
        self._num += 1
        return self.__dict__[name]

sys.modules[__name__] = _states()