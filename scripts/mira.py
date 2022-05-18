import bge

def start(cont):
    pass

def update(cont):

    own = cont.owner
    scene = own.scene
    mira = scene.objects['mira']
    always = cont.sensors['update']
    mouse = cont.sensors['Mouse']

    if always.positive:
        if mouse.positive:
            mira.worldPosition.x = mouse.hitPosition.x
            mira.worldPosition.y = mouse.hitPosition.y
   