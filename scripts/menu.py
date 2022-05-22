
import bge

def start(cont):
    pass

def update(cont):
    own = cont.owner
    print('ok')
    m_over = cont.sensors['over']
    m_left = cont.sensors['mouse']
    menu_pos = own.childrenRecursive.get('menu_pos')

    if m_over.positive:
        if m_left.positive:
            if 'start' in m_over.hitObject:
                bge.logic.addScene('Game',0)
                menu_pos.worldPosition = [-4.0,0.0,0.0]

            if 'load' in m_over.hitObject:
                bge.logic.globalDict['load'] = -5
                bge.logic.addScene('Game',0)


