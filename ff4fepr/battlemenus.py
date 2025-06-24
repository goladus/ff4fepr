from .ff4data import *
from .datatypes import getbytesfortype
from .resource import load
from .core import bytes2int, num2bytes
romoffsets=load('romoffsets')
commands=load('battle-commands')

def dump2screen(romdata):
    startoff=romoffsets['charmenus']
    order = ['Blank'] + romoffsets['charjoin-order']
    rsize=romoffsets['charmenus-size']
    for index, charname in enumerate(order):
        offset=startoff+index*rsize
        print(charname, [commands[x] if x < 0xff else 'x' for x in romdata[offset:offset+rsize]])

def replace_commandset_args(romdata, stringarg):
    charspecs=stringarg.split('.')
    for charspec in charspecs:
        charname, menustr = charspec.split('=')
        menuset=menustr.split(',')
        replace_commandset(romdata, charname, menuset)

def replace_commandset(romdata, charname, menuset):
    startoff=romoffsets['charmenus']
    order = ['Blank'] + romoffsets['charjoin-order']
    rsize=romoffsets['charmenus-size']
    charindex=order.index(charname)
    offset=startoff + charindex*rsize
    newmenu=[commands.index(cmd) for cmd in menuset] + [0xff] * (rsize-len(menuset))
    for index in range(rsize):
        romdata.addmod(offset+index, newmenu[index])

def uptco_edward(romdata):
    replace_commandset(romdata, "UptCo Edward",
                       ['Fight', 'Sing', 'Dart', 'Hide', 'Item'])
