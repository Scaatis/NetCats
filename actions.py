
class ParseError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

"""Type referencing an abstract Action call"""
class action(object):
    def __init__(self):
        self.success = None
        self.cancelled = False
    
    def abort(self):
        self.cancelled = True
        self.success = False
    
    def perform(self, state):
        pass
    
    def successmessage(self):
        pass
    
    def usage(self):
        pass
    
    @staticmethod
    def parse(state, argv):
        return actions[argv[0]].parse(state, argv)
    
"""Connect to a remote host"""
class connect(action):
    def __init__(self, host):
        super().__init__()
        self.host = host
    
    def successmessage(self):
        return "connected to {}".format(self.host.name)
    
    def perform(self, state):
        state.current = self.host
    
    def usage(self):
        return ""
    
    @staticmethod
    def parse(state, argv):
        if len(argv) < 2:
            raise ParseError(usage())
        
        host = next((host for host in state.hosts if host.name == argv[1] or host.address == argv[1]), None)
        if not host:
            raise ParseError("Host {} not found".format(argv[1]))
        
        return connect(host)
    
    def __hash__(self):
        return hash(self.host)
    
    def __eq__(self, other):
        if not type(other) == connect:
            return False
        return self.host is other.host

class disconnect(action):
    def __init__(self, host):
        super().__init__()
        self.host = host
    
    def successmessage(self):
        return "Disconnected."
    
    def perform(self, state):
        state.current = None
    
    @staticmethod
    def parse(state, argv):
        return disconnect(state.current)
    
    def __hash__(self):
        return hash(self.host)
    
    def __eq__(self, other):
        if not type(other) == disconnect:
            return False
        return self.host is other.host

actions = {"connect":connect, "disconnect":disconnect}