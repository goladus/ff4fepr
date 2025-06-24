from .ff4data import *
from .resource import load
from .core import bytes2int, num2bytes, identity
from .core import getmaskedvalue, mergemaskedvalue
romoffsets=load('romoffsets')
items=load('items')
from collections import defaultdict
itemcats=load('item-categories')
import random
eqtoff=romoffsets['equip-tables']
eqrsize=romoffsets['equip-tables-size']

eqclassmap=dict(list(zip(romoffsets['equip-classes'], romoffsets['equip-table-record'])))

def loadequiptables(romdata):
    results={}
    for eqindex in range(32):
        offset=eqtoff+eqindex*eqrsize
        results.setdefault(eqindex,
                           spliteqtable(romdata[offset:offset+eqrsize]))
    return results

def spliteqtable(twobytes):
    results={}
    for eqclass in romoffsets['equip-classes']:
        bitinfo=eqclassmap[eqclass]
        results.setdefault(eqclass, getmaskedvalue(twobytes[bitinfo[0]],
                                                   bitinfo))
    return results

def eqtable2bytes(eqtable):
    results=[0,0]
    for eqclass in romoffsets['equip-classes']:
        bitinfo=eqclassmap[eqclass]
        i=bitinfo[0]
        results[i]=mergemaskedvalue(results[i],
                                    eqtable[eqclass],
                                    bitinfo)
    return results

def equiptables2rom(romdata, eqtables):
    bytelist=[]
    for eqindex in range(romoffsets['equip-tables-num']):
        bytelist += eqtable2bytes(eqtables[eqindex])
    for index, byt in enumerate(bytelist):
        offset=eqtoff+index
        if byt != romdata[offset]:
            romdata.addmod(offset, byt)

def showeqtable(eqd):
    return ','.join(["%s:%s" % (k, eqd[k]) for k in romoffsets['equip-classes']])

def testeq(romdata):
    equiptables2rom(romdata, loadequiptables(romdata))

def dumpindexes(romdata):
    for eqindex in range(romoffsets['equip-tables-num']):
        offset=eqtoff+eqindex*eqrsize
        print(eqindex, showeqtable(spliteqtable(romdata[offset:offset+eqrsize])))

#3, 4, 5, 6, 7, 19(daggers) 
def darkknight_equip(romdata):
    eqt=loadequiptables(romdata)
    for i in [3, 4, 5, 6, 7, 19]:
        eqt[i]['DKCecil']=1
    equiptables2rom(romdata, eqt)
