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

    if own['pl']:
        
        track.object = own['pl'][0]

        cont.activate(track)
    own['group'] = own.groupObject
    

def update(cont):
    own = cont.owner
    scene = own.scene
    print(own['atack'])
    Collision = cont.sensors['Collision']
    if own['time'] == 0:
        own['x'] = 0

    if own['time'] > 0:
        own['time'] -= 1


    if Collision.positive and own['life'] > 0:
        own['life'] -= 1
        

    if own['life'] == 0:
        own.endObject()
        scene.addObject('spw_coin',own,0)
       

    if own['pl']:
        dis = own.getDistanceTo( own['pl'][0])
        
           
        # Enemy tipo 1

        if '1' in own['group']['enemyTipe']:
            if dis> 2 and dis < 15:
                own.applyMovement([0,0.1,0], True)
            if dis <= 5:
                
                if own['atack'] == 0:
                    own['atack'] = 50
                if own['atack'] == 49:
                    scene.addObject('dano_long',own['spw_dano'],1)
               
        # Enemy tipo 2
           
        if '2' in own['group']['enemyTipe']:
             if dis >6 and dis < 15:  
                own.applyMovement([0,0.1,0], True)
                if own['atack'] == 0:
                    own['atack'] = -80
                if own['atack'] == -79:
                    scene.addObject('dano',own['spw_dano'],100)
        
        
             if dis < 7:
                if own['time'] == 0:
                    own['time'] = 50
                if own['time'] == 49:
                    own['x'] = random.randint(-1, 1)
                own.applyMovement([own['x']/10,-0.1,0], True)
                if own['atack'] == 0:
                    own['atack'] = 50

                if own['atack'] == 49:
                    scene.addObject('dano_long',own['spw_dano'],1)

             

    if own['atack'] > 0:
        own['atack'] -= 1

    if own['atack'] < -0:
        own['atack'] +=1

       