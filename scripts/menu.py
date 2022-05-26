from distutils.command.clean import clean
import bge
from bge.types import *
from pathlib import Path
from bge.logic import expandPath

def start(cont):
    # type: (SCA_PythonController) -> None
    pass

def update(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    
    m_over = cont.sensors['over'] # type: KX_MouseFocusSensor
    m_left = cont.sensors['mouse'] # type: SCA_MouseSensor
    menu_pos = own.childrenRecursive.get('menu_pos') # type: KX_GameObject
    tc = bge.logic.keyboard.inputs 
    listScene = bge.logic.getSceneList()
    #ts = bge.logic.setTimeScale(0.5)
   

    if own['fade'] > 0:
        own['fade'] -=1


    if 'Game' in listScene:
        bge.logic.sendMessage('startGame')
        pl = listScene['Game'].objects['player']
        if pl['vida'] == 0:
            menu_pos.worldPosition = [-9.35,0.0,0.0]
            own['status'] = 'gameOuver'
            listScene['Game'].suspend()
            #listScene['Game'].setTimeScale( 0.5 )

    if tc[bge.events.ESCKEY].activated and  own['status'] == 'game':
         menu_pos.worldPosition = [-3.6,0.0,0.0]
         listScene['Game'].suspend()
         own['status'] = 'pause'

    if own['status'] == 'inicio':
        if m_over.positive:
            if m_left.positive:
                if 'start' in m_over.hitObject:
                    own['fade'] = 80
                    own['transition'] = 'start'
        if own['fade'] == 20 and own['transition'] == 'start':
            bge.logic.addScene('Game',0)
            menu_pos.worldPosition = [6.0,0.0,0.0]
            own['status'] = 'game'
                    #listScene['Game'].restart()
            bge.logic.globalDict['load'] = 0
            bge.logic.sendMessage('out')

    if own['status'] == 'inicio':
        if m_over.positive:
            if m_left.positive:
                if 'load' in m_over.hitObject:
                    saveFile = Path(expandPath('//save.txt'))
                    if saveFile.exists():
                        own['fade'] = 80
                        own['transition'] = 'load'
        if own['fade'] == 20 and own['transition'] == 'load':              
            menu_pos.worldPosition = [6.0,0.0,0.0]
            bge.logic.globalDict['load'] = -5
            bge.logic.addScene('Game', 0)
            own['status'] = 'game'
            bge.logic.sendMessage('out') 

        if m_over.positive:
            if m_left.positive:
                if 'quit' in m_over.hitObject:
                    own['fade'] = 80
                    own['transition'] = 'quit'
        if own['fade'] == 20 and own['transition'] == 'quit':
            bge.logic.endGame()

    if own['status'] == 'pause':
        if m_over.positive:
            if m_left.positive:
                if 'resume' in m_over.hitObject:
                    menu_pos.worldPosition = [6.0,0.0,0.0]
                    listScene['Game'].resume()
                    own['status'] = 'game'

                if 'quit' in m_over.hitObject:
                    own['fade'] = 80
                    own['transition'] = 'quitmenu'
                    

        if own['fade'] == 20 and own['transition'] == 'quitmenu':
            bge.logic.globalDict['load'] = -5
            bge.logic.addScene('Game', 0)
            menu_pos.worldPosition = [0.0,0.0,0.0]
            own['status'] = 'inicio'
            listScene['Game'].end()
    
        if own['fade'] == 79 and own['transition'] == 'quitmenu': 
            listScene['hud'].end()

    if own['status'] == 'gameOuver':
        if m_over.positive:
            if m_left.positive:
                if 'restart' in m_over.hitObject:
                    own['fade'] = 80
                    own['transition'] = 'restart'
                    bge.logic.sendMessage('oute')

        if own['fade'] == 20 and own['transition'] == 'restart':
                    menu_pos.worldPosition = [6.0,0.0,0.0]
                    bge.logic.globalDict['load'] = -5
                    listScene['Game'].restart()
                    own['status'] = 'game'
        if m_over.positive:
            if m_left.positive:
                if 'quit' in m_over.hitObject:
                    own['fade'] = 80
                    own['transition'] = 'quitmenu'

        if own['fade'] == 20 and own['transition'] == 'quitmenu':            
                    menu_pos.worldPosition = [0.0,0.0,0.0]
                    listScene['Game'].end()
                    
                    own['status'] = 'inicio'
        if own['fade'] == 79 and own['transition'] == 'quitmenu': 
            listScene['hud'].end()