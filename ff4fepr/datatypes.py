from .resource import load
types=load('types')

def getbytesfortype(stat):
    if stat in types['int2']:
        return 2
    elif stat in types['int3']:
        return 3
    else:
        return 1
