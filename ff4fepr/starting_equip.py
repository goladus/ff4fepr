from ff4data import *
from datatypes import getbytesfortype
from resource import load
from core import bytes2int, num2bytes
romoffsets=load('romoffsets')
items=load('items')

def getoffset(charname, slot):
    startoff=romoffsets['starting-equip']
    charindex=romoffsets['charjoin-order'].index(charname)
    slotindex=romoffsets['starting-equip-record'].index(slot)
    return (startoff+charindex * len(romoffsets['starting-equip-record'])
            + slotindex)

def dump2screen(romdata):
    startoff=romoffsets['starting-equip']
    for charindex, charname in enumerate(romoffsets['charjoin-order']):
        offset=startoff+charindex*len(romoffsets['starting-equip-record'])
        print "%20s" % charname, 
        for index, eqr in enumerate(romoffsets['starting-equip-record']):
            itemeq=romdata[offset+index]
            if eqr not in ['rhno', 'lhno']:
                print "%15s" % items[itemeq],
            else:
                print "%2d" % itemeq,
        print

def setslot(romdata, charname, slot, itemname, quantity=1):
    offset=getoffset(charname, slot)
    if slot in ['head', 'body', 'arms']:
        romdata.addmod(offset, items.index(itemname))
    elif slot in ['rheq', 'lheq']:
        qoffset=offset+1
        if itemname is not None:
            romdata.addmod(offset, items.index(itemname))
        romdata.addmod(qoffset, quantity)
    elif slot in ['rhno', 'lhno']:
        romdata.addmod(offset, quantity)

def uptco_edward(romdata):
    def seted(x, y):
        setslot(romdata, "UptCo Edward", x, y)
    seted('head', 'Ribbon')
    seted('arms', 'Crystal Ring')
    seted('body', 'Adamant Armor')
    seted('rheq', 'Crystal Sword')
    seted('lheq', 'Drain Sword')
