import bge

def start(cont):
    own = cont.owner

    mesh = own.childrenRecursive.get('mesh_arm')
    group = own.groupObject
    
    mesh.replaceMesh( str(group['tipo']))