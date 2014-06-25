
from output import show, getline
from actions import actions, ParseError

class Gamestate(object):
    def __init__(self):
        self.hosts = []
        self.before = {}
        self.after = {}
        self.current = None
        self.running = False
    
    def turn(self):
        print(self.current.name, end="")
        argv = getline()
        if argv == "":
            return
        argv = argv.split(" ")
        
        if argv[0] not in actions:
            show("Unknown command: {}".format(argv[0]))
            return
        
        act = None
        try:
            act = actions[argv[0]].parse(self, argv)
        except ParseError as err:
            show(err.message)
            return
        
        self.perform(act)
    
    def perform(self, action, silent=False):
        if action.__class__ in self.before:
            self.before[action.__class__](action)
        
        if action.cancelled:
            return False
        
        if action in self.before:
            self.before[action](action)
        
        if action.cancelled:
            return False
        
        if not action.success:
            action.perform(self)
        action.success = True
        
        if not silent:
            show(action.successmessage())
        
        if action in self.after:
            self.after[action](action)
        
        if action.__class__ in self.after:
            self.after[action.__class__](action)
        
        return action.success
    
    def run(self):
        self.running = True
        while self.running:
            self.turn()
    
    def deny(self, msg):
        show(msg)
    
    def triggerbefore(self, action):
        def register(func):
            self.before[action] = func
            return func
        return register
    
    def disablebefore(self, action):
        if action in self.before:
            del self.before[action]
    
    def triggerafter(self, action):
        def register(func):
            self.after[action] = func
            return func
        return register
    
    def disableafter(self, action):
        if action in self.after:
            del self.after[action]