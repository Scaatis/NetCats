
# Default rules and behavior
from gamestate import Gamestate
from host import Host
from actions import *
import states

state = Gamestate()

#convenience
before = state.triggerbefore
after = state.triggerafter

# not "hard"-coded into the engine
# might want to change this behavior
localhost = Host(state, "localhost", "127.0.0.1")

state.current = localhost

@before(disconnect(localhost))
def dontdclocalhost(action):
    action.abort()
    state.deny("Not time to jack out yet")

@after(disconnect)
def gotolocalhost(action):
    state.current = localhost

@before(connect)
def dcfirst(action):
    if state.current is not localhost:
        if not state.perform(disconnect(state.current)):
            action.abort()

# specific to the script
SenseNet = Host(state, "SenseNet", "23.44.51.132")

state.run()