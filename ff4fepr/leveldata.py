from .ff4data import *
from .core import getbitvalue, mergebitvalue, bytes2int, num2bytes
from .datatypes import getbytesfortype
from collections import defaultdict

ludata=romoffsets['levelupdata']
lusize=romoffsets['levelupdata-size']
luchars=romoffsets['starting-stats-order'][:-1] # -1 for uptco ed

m1=[None, 0xf, 0]
stats='str agi vit wis wil'.split()

def numlevels(charname):
    sl=romoffsets['starting-level'][charname]
    return 70-sl

def calcoffsets():
    """Returns a map where
    results[charname] -> <offset of first entry in level-up table>"""
    results={}
    current=0
    for charname in luchars:
        results.setdefault(charname, ludata+current)
        current += (numlevels(charname) * lusize) + 3 + lusize
    return results

luoffsets=calcoffsets()

def dump2screen(romdata):
    for charname in luchars:
        charoffset=luoffsets[charname]
        for x in range(numlevels(charname)):
            offset=charoffset + x * lusize
            level=romoffsets['starting-level'][charname]+x
            print(charname, level, renderluentry(
                parseluentry(romdata[offset:offset+lusize])))

def renderluentry(rec):
    lustat=' '.join([stat if rec[stat] == 1 else '   ' for stat in stats])
    # A value of 7 is -1
    return "%s %s hp:%s mp:%s tnl %s " % (lustat, rec['bonus'],
                                          rec['hpup'],
                                          rec['mpup'],
                                          rec['tnl'])

def parseluentry(fivebytes):
    lur=romoffsets['leveluprecord']
    results={}
    for key in lur:
        index, mask, bshift = lur[key]
        bvalue=getbitvalue(fivebytes[index], [0, mask, bshift])
        if (not key.startswith('tnl') and key != 'bonus'):
            results[key]=bvalue
        elif key == 'bonus':
            results[key]=((bvalue+1) % 8) - 1
        elif key == 'tnl':
            results[key]=bytes2int(fivebytes[index+1:index+3] + [bvalue])
    return results

def getleveloffset(charname, level):
    charoffset=luoffsets[charname]
    x=level-romoffsets['starting-level'][charname]
    return charoffset + x*lusize

def loadlevelupdata(romdata):
    'todo'
    results=defaultdict(dict)
    for charname in luchars:
        charoffset=luoffsets[charname]
        for x in range(numlevels(charname)):
            offset=charoffset + x*lusize
            level=romoffsets['starting-level'][charname]+x
            results[charname].setdefault(
                level, parseluentry(romdata[offset:offset+lusize]))
    return dict(results)

def ludata2rom(romdata, levelupdict):
    for charname in luchars:
        for level, rec in levelupdict[charname].items():
            offset=getleveloffset(charname, level)
            for index, newbyte in enumerate(luentry2bytes(rec)):
                if romdata[offset+index] != newbyte:
                    romdata.addmod(offset+index, newbyte)

def luentry2bytes(rec):
    lur=romoffsets['leveluprecord']
    results=defaultdict(int)
    for key in lur:
        if key == 'bonus':
            results[0] = mergebitvalue(results[0], rec[key] % 8, lur[key])
        elif key == 'tnl':
            tnlbytes=num2bytes(rec['tnl'], 3)
            results[3]=tnlbytes[0]
            results[4]=tnlbytes[1]
            results[2]=mergebitvalue(results[2], tnlbytes[2], lur[key])
        else:
            index=lur[key][0]
            results[index]=mergebitvalue(results[index],
                                         rec[key], lur[key])
    return [y for x, y in sorted(results.items())]

def testludata(romdata):
    lud=loadlevelupdata(romdata)
    ludata2rom(romdata, lud)

def dump2screenx(romdata):
    for x in range(60):
        offset=ludata + x*lusize
        t1=getbitvalue(romdata[offset+2], m1)
        sts='.'.join([stat for stat in stats
                      if getbitvalue(romdata[offset],
                                     romoffsets['leveluprecord'][stat]) == 1])
        print(x+10, hex(offset), sts, romdata[offset+1], t1)
    for y in range(61, 121):
        offset=ludata + y*lusize + 3
        print(y, hex(offset), romdata[offset:offset+lusize])
    print("----")
    for y in range(122, 194):
        offset=ludata + y*lusize + 6
        print(y, hex(offset), romdata[offset:offset+lusize])

def yangpost60hp(romdata):
    lud=loadlevelupdata(romdata)
    for level in range(60, 69):
        lud['Yang'][level]['hpup']=152
    lud['Yang'][69]['hpup']=160
    ludata2rom(romdata, lud)
