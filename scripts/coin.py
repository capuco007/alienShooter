import bge


def update(cont):
    own = cont.owner
    scene = own.scene
    pl = scene.objects['player']
    track = cont.actuators['track']
    track.object = pl
    cont.activate(track)
    dis = own.getDistanceTo(pl)
    if dis < 8:
        own.applyMovement([0,0.3,0], True)