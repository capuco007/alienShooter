import bge



def start(cont):
    own = cont.owner
    scene = own.scene
    Plane = own.childrenRecursive.get('Plane')
    pl = [obj for obj in scene.objects if 'player' in obj]

    # Dialogos 
    textFalas = {
        'inicio':'',
        'fala_0': '',
        'fala_1': 'Nossa que fome e essa, \n acho que vou tomar aquele chocolate quente !',
        'fala_2': 'Tudo bem ?',
        'fala_3': 'teste',
        'fala_nokey': 'voce nao tem a chave !!'
        }
    #############################///////#####################

    textDialog = own.childrenRecursive.get('falas')
    fala = bge.logic.globalDict['text']
    textDialog['text'] = textFalas[fala]

    if bge.logic.globalDict['text'] == 'fala_0':
        Plane.visible = False

def trades(cont):
    own = cont.owner
    scene = own.scene
    
    LB = own.childrenRecursive.get('lifeBar')
    L_1 = own.childrenRecursive.get('L_1')
    L_2 = own.childrenRecursive.get('L_2')
    if 'estamina' in bge.logic.globalDict:
        own['estaminaP'] = bge.logic.globalDict['estamina']

    if 'lifePlayer' in bge.logic.globalDict:
        own['vidaPlayer'] = bge.logic.globalDict['lifePlayer']

    if bge.logic.globalDict['keysicon'] == None:
        bge.logic.sendMessage('keyVisibleFalse')
    else:
        own['keyIcon'] = False
        bge.logic.sendMessage('keyVisibleTrue')

    if 'gun' in bge.logic.globalDict:
        L_1.replaceMesh(bge.logic.globalDict['gun'][0])
        if len(bge.logic.globalDict['gun'])> 1:
            L_2.replaceMesh(bge.logic.globalDict['gun'][1])
        else:
            L_2.replaceMesh('stand')
    else:
        L_1.replaceMesh('stand')
        L_2.replaceMesh('stand')

    
