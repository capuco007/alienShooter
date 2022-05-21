import bge



def start(cont):
    own = cont.owner
    scene = own.scene
    Plane = own.childrenRecursive.get('Plane')
    pl = [obj for obj in scene.objects if 'player' in obj]
    textFalas = {
        'fala_0': '',
        'fala_1': 'Nossa que fome e essa, \n acho que vou tomar aquele chocolate quente !',
        'fala_2': 'Tudo bem ?',
        'fala_3': 'teste'
        }

    textDialog = own.childrenRecursive.get('falas')
    fala = bge.logic.globalDict['text']
    textDialog['text'] = textFalas[fala]
    print(bge.logic.globalDict['text'])

    if bge.logic.globalDict['text'] == 'fala_0':
        Plane.visible = False

