
import output
from types import MethodType

class Gamestate(object):
    def __init__(self):
        self.actions = {}
        
        self.hosts = {}
        
        self.check = {}
        self.carryout = {}
        self.report = {}
        
        self.before = {}
        self.instead = {}
        self.after = {}
        
        self.atinput = None
        self.atparse = None
        self.atprompt = None
        
        self.current = None
        self.running = False
    
    def turn(self):
        # invoke prompt rule, i.e. print the prompt
        self.atprompt()
        
        # remembers cursor location for subsequent deny()
        output.startinput()
        
        # invoke input rule, i.e. handle user typing
        line = self.atinput()
        
        # remembers cursor location again for subsequent deny()
        output.stopinput()
        
        if argv == line:
            return
        argv = line.split()
        
        # invoke parse rule, i.e. construct appropriate action
        act = self.atparse(argv)
        if not act:
            return
        
        self.perform(act)
    
    def perform(self, action, silent=False):
        # 1: before
        for rule in self.before.get(type(action), []):
            rule(action)
        
        if action.cancelled:
            return action.success
        
        for rule in self.before.get(action, []):
            rule(action)
        
        if action.cancelled:
            return action.success
        
        # 2: check
        action.check()
        
        if action.cancelled:
            return action.success
        
        # 3: instead
        if action in self.instead:
            action.cancelled = True
            for rule in self.instead[action]:
                rule(action)
        elif type(action) in self.instead:
            action.cancelled = True
            for rule in self.instead[type(action)]:
                rule(action)
        
        if action.cancelled:
            return action.success
        
        # 4: perform
        action.carryout()
        
        # 5: report
        if action.success and not silent:
            action.report()
        
        # 6: after
        for rule in self.after.get(action, []):
            rule(action)
        
        for rule in self.after.get(type(action), []):
            rule(action)
        
        return action.success
    
    def run(self):
        self.running = True
        output.init()
        try:
            while self.running:
                self.turn()
        except KeyboardInterrupt:
            pass
        output.uninit()
    
    def unlock(self, actiontype):
        self.actions[actiontype.name] = actiontype
    
    def triggerbefore(self, action):
        if action not in self.before:
            self.before[action] = []
        
        def register(func):
            self.before[action].append(func)
            return func
        return register
    
    def disablebefore(self, action, func):
        if action in self.before:
            self.before[action].remove(func)
    
    def triggerinstead(self, action):
        if action not in self.instead:
            self.instead[action] = []
        
        def register(func):
            self.instead[action].append(func)
            return func
        return register
    
    def disableinstead(self, action, func):
        if action in self.instead:
            self.instead[action].remove(func)
    
    def triggerafter(self, action):
        if action not in self.before:
            self.before[action] = []
        
        def register(func):
            self.after[action].append(func)
            return func
        return register
    
    def disableafter(self, action, func):
        if action in self.after:
            self.after[action].remove(func)
    
    def triggeroninput(self, func):
        self.atinput = func
        return func
    
    def triggeronparse(self, func):
        self.atparse = func
        return func
    
    def triggeronprompt(self, func):
        self.atprompt = func
        return func
