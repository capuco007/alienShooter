import bge
from collections import OrderedDict
from mathutils import Vector


def start(cont):
    own = cont.owner
    scene = own.scene
    own['GunList'] = []
    own['gunSpw'] = ""
    bge.logic.globalDict['text'] = 'fala_0'
    bge.logic.globalDict['pause'] = False
    
def Colision(cont):
    own = cont.owner
    scene = own.scene
    kb = bge.logic.keyboard.inputs
    dano = cont.sensors['dano']
    getGun = cont.sensors['gun']
    spw_gun = own.childrenRecursive.get('spw_gun')
    mesh_arm_p = own.childrenRecursive.get('mesh_arm_p')

    if own['GunList']:
        mesh_arm_p.replaceMesh( str(own['GunList'][0]))



    # Pegar Armas
    if getGun.positive:
        gunGroup = getGun.hitObject.groupObject
        itenGun = getGun.hitObject

        if kb[bge.events.EKEY].activated:
            if not gunGroup['tipo'] in own['GunList']:
                if len(own['GunList'])>=2:
                    iten = own['GunList'][0]
                    del own['GunList'][0]
                    obj = scene.addObject('guns',gunGroup)
                    obj['tipo'] = iten
                    own['GunList'].reverse()

                own['GunList'] = [gunGroup['tipo']] + own['GunList']
                gunGroup.endObject()



    # Tomar Dano
    if dano.positive:
        scene.addObject('sangue',own,100)

def coin(cont):
    own = cont.owner
    coinColider = cont.sensors['coins']
    if coinColider.positive:
        own['coin_player'] += 1

class Player(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
    ])

    def start(self, args):
        self.scene = self.object.scene
        self.spw_bulet = self.scene.objects['spw_bulet']
        self.shadowPlay = self.scene.objects['shadowPlayer']
        self.char = bge.constraints.getCharacter(self.object)
        self.speed = 0.2
        self.life = 100
        self.timeSot = 0
        self.timeDash = 0
        self.guns = []
        self.cash = 0
        self.object.collisionCallbacks.append(self.onCollision)
        self.activeDash = False
        self.estamina = 100
        self.recargEstam = 100
        self.key = ['1']
        
        self.timeSaveLoad = 0
        if 'load' in  bge.logic.globalDict:
            self.timeSaveLoad =  bge.logic.globalDict['load']
 
    def dialogs(self):
        pass
    def onCollision(self,object):
        if 'dano' in object:
            bge.logic.sendMessage('shake')
            if self.life >0:
                self.life -= 1

        if 'dash' in object:
            tc = bge.logic.keyboard.inputs
            if self.activeDash == False:
                if tc[bge.events.EKEY].activated:
                    object.groupObject.endObject()
                    self.activeDash = True
        if 'arena' in object:
            pass
            #eixo = self.scene.objects['eixo']
            #eixo.worldPosition.x = object.worldPosition.x
            #eixo.worldPosition.y = object.worldPosition.y - 10.0

        if 'openDor' in object:
            tc = bge.logic.keyboard.inputs
            if tc[bge.events.EKEY].activated:
                if object.groupObject['key'] in self.key:
                    object['openDor'] = True

        if 'save' in object:
            
            if object['save'] == True:
                self.timeSaveLoad = 5
                object['save'] = False

        if 'fala' in object:
            bge.logic.globalDict['text'] = object['fala']
            object.endObject()
            bge.logic.sendMessage('dialog')
            self.object['text'] = 10
            
    def move(self):
        kb = bge.logic.keyboard.inputs
        y = kb[bge.events.WKEY].active - kb[bge.events.SKEY].active
        x = kb[bge.events.DKEY].active - kb[bge.events.AKEY].active
        self.char.walkDirection = Vector([x,y,0]).normalized()*self.speed

    def shot(self):
        if self.timeSot > 0:
            self.timeSot -=1
        ms = bge.logic.mouse.inputs

        if self.object['GunList']:
            if self.object['GunList'][0] == 'pistola':
                if ms[bge.events.LEFTMOUSE].active and self.timeSot == 0:
                    self.scene.addObject('buler_payer',self.spw_bulet,25)
                    self.timeSot = 10

            if self.object['GunList'][0] == 'metralhadora':
                if ms[bge.events.LEFTMOUSE].active and self.timeSot == 0:
                    self.scene.addObject('buler_payer',self.spw_bulet,25)
                    self.timeSot = 5

            if self.object['GunList'][0] == 'shotgun':
                if ms[bge.events.LEFTMOUSE].active and self.timeSot == 0:
                    self.scene.addObject('buler_payer',self.spw_bulet,25)
                    self.timeSot = 50

    def tradeGun(self):
        mesh_arm_p = self.object.childrenRecursive.get('mesh_arm_p')
       
        kb = bge.logic.keyboard.inputs
        if self.object['GunList'] != 0:
            if len(self.object['GunList'])>1:
                if kb[bge.events.QKEY].activated:
                    mesh_arm_p = self.object.childrenRecursive.get('mesh_arm_p')
                    self.timeSot = 0
                    self.object['GunList'].reverse()
                    mesh_arm_p.replaceMesh( str(self.object['GunList'][0]))
               
    def dash(self):
        kb = bge.logic.keyboard.inputs

        if self.timeDash >0:
            self.timeDash -= 1
        if kb[bge.events.SPACEKEY].activated and self.timeDash == 0:

            if self.estamina >= self.recargEstam:
                self.estamina -= self.recargEstam
                self.timeDash = 15
        if self.timeDash >8:
            self.speed = 0.8
        else:
            self.speed = 0.2
        if self.estamina < 100:
            self.estamina += 1

    def efects(self):
        pass

    def save(self):
        savegame = {
            'player': {
                'GunList': self.object['GunList'],
                'life': self.life,
                'cash': self.cash,
                'recargEstam': self.recargEstam,
                'position': list(self.object.worldPosition),
                'activeDash': self.activeDash
            },
            'objects': [],
        }

        for o in self.object.scene.objects:
            if 'save' in o:
                savegame['objects'].append(o.name)
            if 'dor' in o:
                
                for prop in o.getPropertyNames():
                    savegame[o.name] = o[prop]

            if 'openDor' in o:
                for prop in o.getPropertyNames():
                    savegame[o.name] = o[prop]

        
            

        with open(bge.logic.expandPath('//save.txt'), 'w') as openedFile:
            openedFile.write(str(savegame))
            print('> Savegame salvo em', openedFile.name)

    def load(self):
        from ast import literal_eval

        savegame = {}

        try:
            with open(bge.logic.expandPath('//save.txt'), 'r') as openedFile:
                savegame = literal_eval(openedFile.read())
                print('> Savegame carregado de', openedFile.name)
        except Exception as e:
            print('X Savegame não existe', e)

        if savegame:
            self.object['GunList'] = savegame['player']['GunList']
            self.life = savegame['player']['life']
            self.cash = savegame['player']['cash']
            self.recargEstam = savegame['player']['recargEstam']
            self.object.worldPosition = savegame['player']['position']
            self.activeDash = savegame['player']['activeDash']

            for o in self.object.scene.objects:
                if 'save' in o and not o.name in savegame['objects']:
                    o.endObject()
                if 'dor' in o and o.name in savegame:
                    o['status'] = savegame[o.name]

                if 'openDor' in o and o.name in savegame:
                    o['openDor'] = savegame[o.name]

        mesh_arm_p = self.object.childrenRecursive.get('mesh_arm_p')
        self.timeSot = 0
        #self.object['GunList'].reverse()
        mesh_arm_p.replaceMesh( str(self.object['GunList'][0]))

    def dialogs(self):

        if self.object['text'] > 1:
            self.object['text'] -= 1

        if self.object['text'] == 1:
            bge.logic.setTimeScale(0.0)
            

    def update(self):
        if bge.logic.keyboard.inputs[bge.events.SPACEKEY].activated and bge.logic.globalDict['text'] != 'fala_0':
            self.object['text'] = 0
            bge.logic.globalDict['text'] = 'fala_0'
            bge.logic.sendMessage('dialog')
            bge.logic.sendMessage('notdialog')
        
        print(self.object['text'])
        
        if self.object['text'] == 0:
            if self.life > 0:

                self.move()
                self.shot()
                self.efects()
                self.tradeGun()
                self.dialogs()

                if bge.logic.keyboard.inputs[bge.events.F1KEY].activated:
                    self.load()

                if bge.logic.keyboard.inputs[bge.events.F2KEY].activated:
                    self.save()

                if self.activeDash:
                    self.dash()
            else:
                bge.logic.globalDict['load'] = -5
                bge.logic.restartGame()
        else:
            self.char.walkDirection = Vector([0,0,0]).normalized()*self.speed

        if self.timeSaveLoad >0:
            self.timeSaveLoad -= 1

        if self.timeSaveLoad < -0:
            self.timeSaveLoad += 1

        if self.timeSaveLoad == 1:
            self.save()
        if self.timeSaveLoad == -1:
            self.load()
           

