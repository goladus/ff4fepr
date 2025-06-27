from .ff4data import *
from .datatypes import getbytesfortype
from .resource import load
from .core import bytes2int, num2bytes, toint
from .output import warning
romoffsets=load('romoffsets')
items=load('items')
eqsets=load('eqsets')

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
        print("%20s" % charname, end=' ')
        for index, eqr in enumerate(romoffsets['starting-equip-record']):
            itemeq=romdata[offset+index]
            if eqr not in ['rhno', 'lhno']:
                print("%15s" % items[itemeq], end=' ')
            else:
                print("%2d" % itemeq, end=' ')
        print()

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

def splitdefault(eqstr, default=1, splitter=':'):
    '''splits a string on a char and returns
    the first value and second value,
    or the first value and the default value if
    no splitter was present in the string
    '''
    tokens=eqstr.split(splitter)
    return (tokens[0], toint(list(tokens[1:2] + [1])[0]))

def seteqlevel(romdata, charname, eqleveltag):
    if eqleveltag not in eqsets[charname]:
        warning("No equipment set defined for %s:%s\n" % (charname, eqleveltag))
        return False
    rheqs, lheqs, head, body, arms = eqsets[charname][eqleveltag]
    rheq, rhno=splitdefault(rheqs)
    lheq, lhno=splitdefault(lheqs)
    setslot(romdata, charname, 'rheq', rheq, rhno)
    setslot(romdata, charname, 'lheq', lheq, lhno)
    setslot(romdata, charname, 'head', head)
    setslot(romdata, charname, 'body', body)
    setslot(romdata, charname, 'arms', arms)

def setall_eqlevel(romdata, eqleveltag):
    for charname in eqsets:
        seteqlevel(romdata, charname, eqleveltag)

def uptco_edward(romdata):
    def seted(x, y):
        setslot(romdata, "UptCo Edward", x, y)
    seted('head', 'Ribbon')
    seted('arms', 'Crystal Ring')
    seted('body', 'Adamant Armor')
    seted('rheq', 'Crystal Sword')
    seted('lheq', 'Drain Sword')
