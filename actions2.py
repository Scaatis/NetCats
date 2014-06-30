
from random import random

class action(object):
    def __init__(self, *argtypes):
        self.argtypes = argtypes
        self.rand = random()
    
    def __call__(self, *args):
        if len(args) != len(self.argtypes):
            raise Exception("Wrong number of arguments")
        for i, arg in enumerate(args):
            if type(arg) is not self.argtypes[i]:
                raise Exception("Wrong type of argument {}, expected {}, got {}".format(i, self.argtypes[i], type(arg))
        h = hash(self.rand)
        for arg in args:
            h ^ hash(arg)
        return h
    
    def parse(self, state, argv):
        if len(argv) != len(self.argtypes):
            raise Exception("Wrong number of arguments!") # this has got to go different
        args = []
        for i, arg in enumerate(argv[1:]):
            if arg not in state.pools[self.argtypes[i]]:
                raise Exception("Cannot find {} {}".format(self.argtypes[i], arg)) # this too
            args.append(state.pools[self.argtypes[i]][arg])
        return args