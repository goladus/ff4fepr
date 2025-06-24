from ff4data import *
from datatypes import getbytesfortype
from resource import load
from core import bytes2int, num2bytes, toint
romoffsets=load('romoffsets')

def dump2screen2(romdata):
    startoff=romoffsets['starting-stats']
    sssize=romoffsets['starting-stats-size']
    for offset in range(startoff, startoff+0x200, sssize):
        print(romdata[offset:offset+0x20])

def dump2screen(romdata):
    startoff=romoffsets['starting-stats']
    sssize=romoffsets['starting-stats-size']
    ssorder=romoffsets['starting-stats-order']
    for index, name in enumerate(ssorder):
        offset=startoff+(index*sssize)
        print(name, romdata[offset:offset+sssize])

def getstatoff(charname, stat):
    charindex=romoffsets['starting-stats-order'].index(charname)
    sssize=romoffsets['starting-stats-size']
    statindex=romoffsets['starting-stats-record-map'][stat]
    return romoffsets['starting-stats']+(charindex * sssize) + statindex

def getstatval(romdata, charname, stat):
    offset=getstatoff(charname, stat)
    nbytes=getbytesfortype(stat)
    if stat in romoffsets['split-stats']:
        bitmask = romoffsets['split-stats'][stat][1]
        bitshift = romoffsets['split-stats'][stat][2]
        return (romdata[offset] & bitmask) >> bitshift
    else:
        return bytes2int(romdata[offset:offset+nbytes])

def dumpcharstats(romdata, charname):
    results={}
    for stat in ['charid',
                 'left-handed',
                 'right-handed',
                 'sprite',
                 'backrow',
                 'level',
                 'hp',
                 'maxhp',
                 'mp',
                 'maxmp',
                 'str',
                 'agi',
                 'vit',
                 'wis',
                 'wil',
                 'xp',
                 'xpnext']:
        results.setdefault(stat, getstatval(romdata, charname, stat))
    results.setdefault('charname', charname)
    print("{charname}: {charid} {sprite} {level} {hp} {mp} {xp} {wis} {wil} [{left-handed}{right-handed}]".format(**results))

def dumpstartingstats(romdata):
    for charname in romoffsets['starting-stats-order']:
        dumpcharstats(romdata, charname)

def modifystatval(romdata, charname, stat, new_value):
    offset=getstatoff(charname, stat)
    nbytes=getbytesfortype(stat)
    if new_value is True:
        newval=1
    elif new_value is False:
        newval=0
    else:
        newval=new_value
    if stat in romoffsets['split-stats']:
        bitmask = romoffsets['split-stats'][stat][1]
        bitshift = romoffsets['split-stats'][stat][2]
        currval = romdata[offset]
        newbyte = (currval & ~ bitmask) | (newval << bitshift)
        bytelist=[newbyte]
    else:
        bytelist=num2bytes(newval, nbytes)
    for index, btval in enumerate(bytelist):
        if romdata[offset+index] != btval:
            romdata.addmod(offset+index, btval)

def setdualwield(romdata, charname):
    modifystatval(romdata, charname, 'left-handed', True)
    modifystatval(romdata, charname, 'right-handed', True)

def setdualwields(romdata, argstring):
    for charname in argstring.split(','):
        setdualwield(romdata, charname)

def uptco_edward(romdata):
    charname="upt CoEdward"
    modifystatval(romdata, charname, 'str', 70)
    modifystatval(romdata, charname, 'agi', 70)
    modifystatval(romdata, charname, 'wis', 70)
    modifystatval(romdata, charname, 'wil', 70)
    modifystatval(romdata, charname, 'hp', 9050)
    modifystatval(romdata, charname, 'maxhp', 9050)
    modifystatval(romdata, charname, 'mp', 9050)
    modifystatval(romdata, charname, 'maxmp', 9050)
    modifystatval(romdata, charname, 'level', 80)

def setcharstats(romdata, argstring):
    charspecs=argstring.split('.')
    for charspec in charspecs:
        charname, statmodstr=charspec.split(':')
        for statmod in statmodstr.split(','):
            statname, statval = statmod.split('=')
            modifystatval(romdata, charname, statname, toint(statval))
