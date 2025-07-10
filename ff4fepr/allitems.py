from .ff4data import *
from .ff4text import basicencode, encoding
from .resource import load

def changeitemname(romdata, itemname, newtext):
    itemnum=items.index(itemname)
    offset=romoffsets['itemnames']+itemnum*romoffsets['itemnames-size']
    newencoding=basicencode(newtext)
    nbytes=romoffsets['itemnames-size']
    if len(newencoding) >= nbytes:
        newbytes=newencoding[:nbytes]
    else:
        newbytes=newencoding + [255] * (nbytes-len(newencoding))
    for index in range(nbytes):
        romdata.addmod(offset+index, newbytes[index])

def dumpnames(romdata):
    startoff=romoffsets['itemnames']
    for index in range(len(items)):
        offset=startoff+index*romoffsets['itemnames-size']
        txtlst=romdata[offset:offset+romoffsets['itemnames-size']]
        print(''.join([encoding[x] for x in txtlst]), txtlst)

def checkdummy(romdata, itemname):
    itemnum = items.index(itemname)
    offset = romoffsets['itemnames']+itemnum*romoffsets['itemnames-size']
    txtlst = romdata[offset:offset+romoffsets['itemnames-size']]
    itemtxt = ''.join([encoding[x] for x in txtlst])
    return itemtxt.startswith('<blank>Dummy')

def fix_dummies(romdata):
    vanillamap = load('vanilla-item-namemap')
    for fullname, vanillaname in vanillamap:
        if vanillaname is not None:
            if checkdummy(romdata, fullname):
                changeitemname(romdata, fullname, vanillaname)

