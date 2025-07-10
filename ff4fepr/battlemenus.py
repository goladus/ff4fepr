from .ff4data import *
from . import ff4text
from .datatypes import getbytesfortype
from .resource import load
from .core import bytes2int, num2bytes
romoffsets=load('romoffsets')
commands=load('battle-commands')

def loadcommands(romdata):
    loaded_commands = {}
    startoff=romoffsets['charmenus']
    order = ['Blank'] + romoffsets['charjoin-order']
    rsize=romoffsets['charmenus-size']
    for index, charname in enumerate(order):
        offset=startoff+index*rsize
        loaded_commands[charname] = [commands[x] if x < 0xff else 'x' for x in romdata[offset:offset+rsize]]
    return loaded_commands


def writecommands(romdata, loaded_commands):
    startoff=romoffsets['charmenus']
    order = ['Blank'] + romoffsets['charjoin-order']
    rsize=romoffsets['charmenus-size']
    for index, charname in enumerate(order):
        offset=startoff+index*rsize
        for menunum in range(rsize):
            cmdstr = loaded_commands[charname][menunum]
            if cmdstr == 'x':
                cmd = 0xff
            else:
                cmd = commands.index(cmdstr)
                romdata.addmod(offset+menunum, cmd)


def testcommands(romdata):
    writecommands(romdata, loadcommands(romdata))


def modify_menu(romdata, args):
    loaded_menus = loadcommands(romdata)
    charname, remainder = args.split(':')
    for pair in remainder.split(','):
        numstr, value = pair.split('=')
        num = toint(numstr)
        loaded_menus[charname][num] = value
    writecommands(romdata, loaded_menus)


def replace_menu(romdata, args):
    loaded_menus = loadcommands(romdata)
    rsize = romoffsets['charmenus-size']
    charname, menustr = args.split('=')
    charmenu = menustr.split(',')
    if len(charmenu) <= rsize:
        loaded_menus[charname] = charmenu + ['x' for x in range(rsize - len(charmenu))]
    else:
        loaded_menus[charname] = charmenu[:rsize]
    writecommands(romdata, loaded_menus)


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


def dump_menu_text(romdata):
    menutxtoff = romoffsets['charmenu-text']
    menutxtsz = romoffsets['charmenu-text-size']
    for index, cmd in enumerate(commands):
        offset = menutxtoff + (index * menutxtsz)
        hexbytes = ','.join([hex(x) for x in romdata[offset:offset+menutxtsz]])
        asstr = ff4text.dodecode(romdata[offset:offset+menutxtsz])
        print(index, cmd, asstr, hexbytes)

def fix_dummy_menus(romdata):
    menutxtoff = romoffsets['charmenu-text']
    menutxtsz = romoffsets['charmenu-text-size']
    for index, cmd in enumerate(commands):
        offset = menutxtoff + (index * menutxtsz)
        asstr = ff4text.dodecode(romdata[offset:offset+menutxtsz])
        if cmd != 'Dummy':
            if asstr.startswith('Dummy'):
                for mi, mbyte in enumerate((ff4text.basicencode(cmd) + [0xff] * 5)[:5]):
                    romdata.addmod(offset+mi, mbyte)
