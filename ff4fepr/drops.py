from ff4data import *
from resource import load
drop_tables=load('drop-tables')
jdrop_table=load('j-drop-table')
dropitems_rando=load('rando-dropitems')
almost_everything=dropitems_rando['almost-everything']
import random
import monsters

def dump2screen(romdata):
    startoff=romoffsets['dropdata']
    for index in range(romoffsets['dropdata-len']):
        offset=startoff+index*4
        print index, [items[x]
                      for x in romdata[offset:offset+4]]

def loaddroptables(romdata):
    startoff=romoffsets['dropdata']
    results={}
    for index in range(romoffsets['dropdata-len']):
        offset=startoff+index*4
        results.setdefault(index, [items[x]
                                   for x in romdata[offset:offset+4]])
    return results

def writedroptables(romdata, droptables):
    startoff=romoffsets['dropdata']
    writelist=[]
    for index in range(romoffsets['dropdata-len']):
        for itemname in droptables[index]:
            writelist.append(items.index(itemname))
    for index, itemnum in enumerate(writelist):
        offset=startoff+index
        if itemnum != romdata[offset]:
            romdata.addmod(offset, itemnum)

def testdroptables(romdata):
    writedroptables(romdata, loaddroptables(romdata))

def setjdroptables(romdata):
    writedroptables(romdata, dict([(index, table) for
                                   index, table in enumerate(jdrop_table)]))

def chooseitem(startlist=almost_everything, exclude=None):
    if exclude is None:
        exclude=set([])
    return random.choice(list(set(startlist).difference(exclude)))

def randomize_all(romdata):
    startoff=romoffsets['dropdata']
    for index in range(romoffsets['dropdata-len']):
        offset=startoff+index*4
        if index != 60:
            for slot in range(4):
                romdata.addmod(offset+slot, items.index(chooseitem(exclude=['Pass'])))
