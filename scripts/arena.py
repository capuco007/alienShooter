from ast import Break
import bge
def start(cont):
    own = cont.owner
    scene = own.scene
    own['port_entre'] = own.childrenRecursive.get('porta_entre')
    own['port_said'] = own.childrenRecursive.get('porta_saida')
    own.groupObject['status'] = 0
    own['p_contact'] = False
    own['animation'] = 0
    

def update(cont):
    own = cont.owner
    group = own.groupObject
    Colision_play = cont.sensors['Colision_p']
    Colision_enemy = cont.sensors['Colision_en']
    
    
    if Colision_play.positive and own.groupObject['status'] == 0:
        own['port_entre'].playAction('porta_entra',0,5,play_mode = 0)
        own['port_said'].playAction('porta_said',0,5,play_mode = 0)
        own.groupObject['status'] = 1
        

    if Colision_enemy.positive and own.groupObject['status'] == 1:
        own.groupObject['status'] = 2

    if not Colision_enemy.positive and own.groupObject['status'] == 2:
        own.groupObject['status'] = 3
        

    if own.groupObject['status'] == 3:
        own['port_entre'].playAction('porta_entra',5,0,play_mode = 0)
        own['port_said'].playAction('porta_said',5,0,play_mode = 0)
        own.groupObject['status'] = 4


    
        

 
          
