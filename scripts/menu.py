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
    print('ok')
    m_over = cont.sensors['over'] # type: KX_MouseFocusSensor
    m_left = cont.sensors['mouse'] # type: SCA_MouseSensor
    menu_pos = own.childrenRecursive.get('menu_pos') # type: KX_GameObject

    if m_over.positive:
        if m_left.positive:
            if 'start' in m_over.hitObject:
                bge.logic.addScene('Game',0)
                menu_pos.worldPosition = [-4.0,0.0,0.0]

            if 'load' in m_over.hitObject:
                saveFile = Path(expandPath('//save.txt'))

                if saveFile.exists():
                    bge.logic.globalDict['load'] = -5
                    bge.logic.addScene('Game', 0)

