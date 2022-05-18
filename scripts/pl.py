import bge
from mathutils import Vector

def start(cont):
    own = cont.owner

    own['char'] = bge.constraints.getCharacter(own)
    #own['speed'] = 0.08

def update(cont):
    own = cont.owner
    tc = bge.logic.keyboard.inputs

    x = tc[bge.events.DKEY].active - tc[bge.events.AKEY].active
    y = tc[bge.events.WKEY].active - tc[bge.events.SKEY].active

    own['char'].walkDirection = Vector([x,y,0]).normalized()*own['speed']