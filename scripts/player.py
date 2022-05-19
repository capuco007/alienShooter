import bge
from collections import OrderedDict
from mathutils import Vector

def start(cont):
    own = cont.owner
    scene = own.scene
    own['GunList'] = []
    own['gunSpw'] = ""



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
        mesh_arm_p = self.object.childrenRecursive.get('mesh_arm_p')
        #mesh_arm_p.replaceMesh(None)
        self.estamina = 100
        self.recargEstam = 100

    def onCollision(self,object):
        if 'dano' in object:
            bge.logic.sendMessage('shake')

        if 'dash' in object:
            tc = bge.logic.keyboard.inputs
            if self.activeDash == False:
                if tc[bge.events.EKEY].activated:
                    object.endObject()
                    self.activeDash = True


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
                    self.scene.addObject('buler_payer',self.spw_bulet,100)
                    self.timeSot = 10

            if self.object['GunList'][0] == 'metralhadora':
                if ms[bge.events.LEFTMOUSE].active and self.timeSot == 0:
                    self.scene.addObject('buler_payer',self.spw_bulet,100)
                    self.timeSot = 5

            if self.object['GunList'][0] == 'shotgun':
                if ms[bge.events.LEFTMOUSE].active and self.timeSot == 0:
                    self.scene.addObject('buler_payer',self.spw_bulet,100)
                    self.timeSot = 50

    def tradeGun(self):
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
                'position': list(self.object.worldPosition)
            },
            'objects': [],
        }

        for o in self.object.scene.objects:
            if 'save' in o:
                savegame['objects'].append(o.name)

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

            for o in self.object.scene.objects:
                if 'save' in o and not o.name in savegame['objects']:
                    o.endObject()


    def update(self):

        if self.life > 0:
            self.move()
            self.shot()
            self.efects()
            self.tradeGun()

            if bge.logic.keyboard.inputs[bge.events.F1KEY].activated:
                self.load()

            if bge.logic.keyboard.inputs[bge.events.F2KEY].activated:
                self.save()

            if self.activeDash:
                self.dash()

