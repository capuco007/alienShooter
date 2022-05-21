import bge
import random

def start(cont):
    
    own = cont.owner
    scene = own.scene
    track = cont.actuators['track']
    own['pl'] = [obj for obj in scene.objects if 'player' in obj]
    own['life'] = own.groupObject['life']
    own['time'] = 0
    own['x'] = 0
    own['y'] = 0
    own['spw_dano'] = own.childrenRecursive.get('spw_dano')
    own['atack'] = 0
    colideMesh = cont.sensors['colideMesh']
    pl = scene.objects['player']
    own['group'] = own.groupObject

    if colideMesh.positive:
        arena = colideMesh.hitObject
        mesh =  arena.childrenRecursive.get('navMesh')
        print(mesh)

            
        track.target = pl
        track.navmesh = mesh #scene.objects['navemesh']
           

        #cont.activate(track)
    
    
    

def update(cont):
    own = cont.owner
    scene = own.scene
    track = cont.actuators['track']
    Collision = cont.sensors['Collision']
    dis = own.getDistanceTo( own['pl'][0])
    if own['time'] == 0:
        own['x'] = 0

    if own['time'] > 0:
        own['time'] -= 1


    if Collision.positive and own.groupObject['life'] > 0:
        own.groupObject['life'] -= 1
        

    if own.groupObject['life'] == 0:
        own['group'].endObject()
        scene.addObject('spw_coin',own,0)
       

    if own['pl']:
        dis = own.getDistanceTo( own['pl'][0])
        
           
        # Enemy tipo 1

        if '1' in own['group']['enemyTipe']:
            if dis> 2 and dis < 20:
                own.applyMovement([0,0.1,0], True)
                pass
            if dis <= 2:
                
                if own['atack'] == 0:
                    own['atack'] = 50
            if own['atack'] == 49:
                scene.addObject('dano_player',own['spw_dano'],1)
               
        # Enemy tipo 2
           
        if '2' in own['group']['enemyTipe']:
            if dis >15 and dis < 20:  
                own.applyMovement([0,0.1,0], True)
                pass
            if dis > 5 and dis <= 15:
                if own['atack'] == 0:
                    own['atack'] = -80
            if own['atack'] == -79:
                scene.addObject('dano',own['spw_dano'],100)
        
        
            if dis <=10:
                if own['time'] == 0:
                    own['time'] = 50
                if own['time'] == 49:
                    own['x'] = random.randint(-1, 1)
                own.applyMovement([own['x']/8,-0.1,0], True)
                pass
            if dis < 5:
                if own['atack'] == 0:
                    own['atack'] = 50

            if own['atack'] == 49:
                scene.addObject('dano_player',own['spw_dano'],1)

        # Enemy tipo 3

        if '3' in own['group']['enemyTipe']:
            if dis> 2 and dis < 20:
                own.applyMovement([0,0.1,0], True)
                pass
            if dis <= 2:
                
                if own['atack'] == 0:
                    own['atack'] = 50
            if own['atack'] == 1:
                scene.addObject('exploid',own)
                own.endObject()
             

    if own['atack'] > 0:
        own['atack'] -= 1

    if own['atack'] < -0:
        own['atack'] +=1

    if dis < 20:
        cont.activate(track)

   
   
        