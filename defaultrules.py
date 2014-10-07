
from gamestate import Gamestate
from host import Host
from action import action
import output
import states

state = Gamestate()

prompt = state.triggeronprompt
parse = state.triggeronparse
oninput = state.triggeroninput

before = state.triggerbefore
instead = state.triggerinstead
after = state.triggerafter

def check(actiontype):
    def register(func):
        actiontype.check = func
        return func
    return register
        
def carryout(actiontype):
    def register(func):
        actiontype.carryout = func
        return func
    return register

def report(actiontype):
    def register(func):
        actiontype.report = func
        return func
    return register


localhost = Host(state, "localhost", "127.0.0.1")
state.localhost = localhost
state.current = localhost

connect = action("connect", Host)
disconnect = action("disconnect", Host)

@prompt
def defaultprompt():
    output.addmsg("{}@{} >".format(state.current.name, state.current.address))

@oninput
def getline():
    return output.getline()

@parse
def defaultparse(argv):
    if argv[0] not in state.actions:
        output.addmsg("Error: command {} not found".format(argv[0]))
        return None
    
    actiontype = state.actions[argv[0]]
    args = []
    
    if actiontype is disconnect:
        return disconnect(state.current)
    
    pools = {Host: state.hosts} # User: state.current.users Files: state.current.files
    
    for i, argtype in enumerate(actiontype.argtypes):
        if argv[i+1] not in pools[argtype]:
            output.addmsg("Error: {} {} not found".format(argtype.name, argv[i+1]))
            return None
        args.append(pools[argtype][argv[i+1]])
    
    return actiontype(*args)

@check(connect)
def connectcheck(action):
    if state.current is action.args[0]:
        # message?
        action.abort()

@check(disconnect)
def disconnectcheck(action):
    if action.args[0] is not state.current:
        # message?
        action.abort()
    elif action.args[0] is localhost:
        output.deny("Ain't time to jack out yet!")
        action.abort()

@carryout(disconnect)
def dodisconnect(action):
    state.current = localhost

@carryout(connect)
def doconnect(action):
    state.current = action.args[0]

@report(disconnect)
def reportdisconnect(action):
    output.addmsg("Disconnected.")

@report(connect)
def reportconnect(action):
    output.addmsg("Successfully connected to {}".format(action.args[0].name))
