
class ParseError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

"""Type referencing an abstract Action call"""
class action(type):
    argtypes = []
    
    check = None
    carryout = None
    report = None
    
    def __init__(self, *args):
        self.success = None
        self.cancelled = False
        self.args = []
        if len(args) != len(argtypes):
            raise TypeError("Expected {} arguments, got {}".format(len(argtypes), len(args)))
        
        for i, arg in enumerate(args):
            if tpye(arg) is not argtypes[i]:
                raise TypeError("Type mismatch for argument {}. Expected {} got {}".format(i, argtypes[i].name, type(arg).name))
            self.args.append(arg)
    
    def abort(self):
        self.cancelled = True
        self.success = False
    
    def resume(self):
        self.cancelled = False
        self.success = None
    
    # you may not instantiate action. instead, you get a subtype of action that you can then instantiate
    def __new__(cls, name, *argtypes):
        return type(name,
                    (cls,),
                    {"__new__": (lambda c, *args: super(cls, c).__new__(c, *args)),
                     "argtypes": argtypes})
     
    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        
        for i, arg in enumerate(self.args):
            if arg is not other.args[i]:
                return False
        
        return True
    
    def __hash__(self):
        h = hash(type(self))
        for arg in args:
            h ^ hash(arg)
        return h
