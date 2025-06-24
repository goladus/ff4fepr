from ff4data import *
from core import num2bytes, bytes2int
from datatypes import getbytesfortype
from resource import load, csv_dumper
import sys
import drops
from collections import defaultdict
monster_offsets=load('monster-offsets')
monster_names=[name for name, offset in monster_offsets]
nummonsters=romoffsets['number-of-monsters']
varbytekeys=[key for key in romoffsets['monster-record'] if key.startswith('has-')]
extrakeys=romoffsets['monster-extra-order']
febosses=load('fe-bosses')

def checkmonrecord(abyte):
    """Populat the 'has-*' values from the 'extra' byte in the monster record"""
    results={}
    for key in varbytekeys:
        x, mask, rshift = romoffsets['split-monster'][key]
        results.setdefault(key, ((abyte & mask) >> rshift) == 1)
    return results

def num_extra_bytes(extraflags):
    result=0
    for key in varbytekeys:
        if extraflags[key]:
            result += len(romoffsets['monster-extra'][key[4:]])
    return result

def getmaskedvalue(abyte, bitinfo):
    return (abyte & bitinfo[1]) >> bitinfo[2]

def mergemaskedvalue(existing_byte, byte_to_merge, bitinfo):
    return (existing_byte & ~ bitinfo[1]) | (byte_to_merge << bitinfo[2])

def parsemonrecord(mondict, monbytes):
    monoffs=romoffsets['monster-record']
    monextra=romoffsets['monster-extra']
    splits=romoffsets['split-monster']
    for key in monoffs:
        if key not in extrakeys:
            nbytes=getbytesfortype(key)
            if nbytes == 1:
                index, mask, rshift = splits.get(key, [monoffs[key], 0xff, 0])
                mondict.setdefault(key, ((monbytes[index] & mask) >> rshift))
            else:
                index=monoffs[key]
                mondict.setdefault(key, bytes2int(monbytes[index:index+nbytes]))
    index=9
    for ebyte in extrakeys:
        if mondict["has-%s" % ebyte]:
            mondict.setdefault(ebyte, {})
            for bdata in monextra[ebyte]:
                index += 1
                for bitname, bitinfo in bdata.values()[0].items():
                    mondict[ebyte][bitname]=getmaskedvalue(monbytes[index],
                                                           bitinfo)
    return mondict

def splitmonsters(romdata, offset=romoffsets['monsterdata'], count=0, monsters=None, monsters_left=nummonsters, jadjust=False):
    if monsters is None:
        monsters={}
    if monsters_left == 0:
        return monsters
    else:
        extraflags=checkmonrecord(romdata[offset+9])
        nbytes=10+num_extra_bytes(extraflags)
        nextrecord_bytes=romdata[offset:offset+nbytes]
        monsters.setdefault(count, {'offset': offset,
                                    'local-offset': offset-romoffsets['monsterdata'],
                                    'index': count,
                                    'flags': extraflags,
                                    'name': monster_names[count],
                                    'numbytes': nbytes,
                                    'bytes': nextrecord_bytes})
        monsters[count].update(parsemonrecord(monsters[count],
                                              nextrecord_bytes))
        for xpgp in ['xp', 'gp']:
            xgoffset=romoffsets['monster%s' % xpgp]+count*2
            monsters[count].setdefault(xpgp, bytes2int(romdata[xgoffset:xgoffset+2]))
        # Hack for Japanese version, which seems to have an extra byte here
        if (offset == 0x7312a) and jadjust:
            njadjust=1
        else:
            njadjust=0
        return splitmonsters(romdata,
                             offset=offset+nbytes + njadjust,
                             count=count+1,
                             monsters=monsters,
                             monsters_left=monsters_left-1,
                             jadjust=jadjust)

def monrecord2bytes(monrecord):
    bytesd=defaultdict(int)
    for key, index in romoffsets['monster-record'].items():
        nbytes=getbytesfortype(key)
        if nbytes == 1:
            bitinfo=romoffsets['split-monster'].get(key, [0, 0xff, 0])
            bytesd[index]=mergemaskedvalue(bytesd[index],
                                           monrecord[key],
                                           bitinfo)
        else:
            for xindex, value in enumerate(num2bytes(monrecord[key], nbytes)):
                bytesd[index+xindex]=value
    extra_index=9 #start at 9 and increment before
    for extrakey in romoffsets['monster-extra-order']:
        if monrecord['flags']['has-%s' % extrakey]:
            for bdata in romoffsets['monster-extra'][extrakey]:
                extra_index += 1
                for bitname, bitinfo in bdata.values()[0].items():
                    bytesd[extra_index]=mergemaskedvalue(bytesd[extra_index],
                                                         monrecord[extrakey][bitname],
                                                         bitinfo)
    return [y for (x, y) in sorted(bytesd.items())]

def mondict2bytes(mondict):
    results=[]
    for monster in range(len(mondict)):
        results += monrecord2bytes(mondict[monster])
    return results

def mondict2xgbytes(mondict):
    bytesd={'xp': [], 'gp': []}
    for xg in bytesd:
        for index in range(len(mondict)):
            bytesd[xg] += num2bytes(mondict[index][xg], 2)
    return bytesd

def mondict2rom(romdata, mondict):
    startoff=romoffsets['monsterdata']
    for index, mbyte in enumerate(mondict2bytes(mondict)):
        if romdata[startoff+index] != mbyte:
            romdata.addmod(startoff+index, mbyte)
    monxpgp=mondict2xgbytes(mondict)
    for xg in ['xp', 'gp']:
        xgoff=romoffsets['monster%s' % xg]
        for index, xbyte in enumerate(monxpgp[xg]):
            if romdata[xgoff+index] != xbyte:
                romdata.addmod(xgoff+index, xbyte)

def bkeysstr(adict, key, astringtmp="%s"):
    return astringtmp % '|'.join([x for x, y
                                  in adict.get(key, {}).items()
                                  if y==1])

def test_monsters(romdata, jadjust=False):
    mondict2rom(romdata, splitmonsters(romdata, jadjust=jadjust))

def monsearch(mondict, key, query_value):
    return [k for k, value in mondict.items()
            if value[key]==query_value]

def dumpitemtables(romdata, jadjust=False):
    results=splitmonsters(romdata, jadjust=jadjust)
    for monster in results:
        #print monster, results[monster]['name'], results[monster]['item-table'],
        print("- [%s, %s] #%s" % (results[monster]['item-table'],
                                  results[monster]['item-rate'],
                                  results[monster]['name']))

def paditm(astr, fw):
    return "%s%s" % (astr, ' ' * (fw - len(astr)))

def dumpmonsterdrops(romdata, jadjust=False):
    results=splitmonsters(romdata, jadjust=jadjust)
    droptables=drops.loaddroptables(romdata)
    for monster in results:
        droptable=results[monster]['item-table']
        itemstring=[paditm(x, 16) for x in droptables[droptable]]
        print(paditm(results[monster]['name'], 10), ''.join(itemstring))

def statperstat(mrecord, divkey):
    k1, k2 = divkey.split('/')
    return (mrecord[k1]*1.0)/mrecord[k2]

def dump2csv(romdata, jadjust=False, bosses=False):
    allm=splitmonsters(romdata, jadjust=jadjust)
    from pprint import pprint as pp
    keys='name boss level hp xp gp'.split()
    additional_keys='xp/hp gp/hp xp/level gp/level'.split()
    outputdata={'header': ['index'] + keys + additional_keys,
                'rows' : []}
    for monster in allm:
        if not allm[monster]['name'].startswith('Dummy'):
            if (bosses or allm[monster]['name'] not in febosses):
                dat1=[allm[monster][key] for key in keys]
                dat2=[statperstat(allm[monster], key) for key in additional_keys]
                outputdata['rows'].append([monster] + dat1+dat2)
    csv_dumper(sys.stdout, outputdata)

def dumpkeys(romdata, keys, jadjust=False):
    allm=splitmonsters(romdata, jadjust=jadjust)
    for monster in allm:
        mname=monster_offsets[monster][0]
        opstr=' '.join(["%s" % allm[monster][key] for key in keys])
        print(opstr, mname)

fieldpads=dict(level=3,
               hp=6,
               xp=6,
               gp=5)

def monvalstr(results, monster, key):
    value="%s" % results[monster][key]
    padding = ' ' * (fieldpads[key] - len(value))
    prefix='lv' if key=='level' else key
    return "(%s:%s)%s" % (prefix, value, padding)

def dumpsplits(romdata, jadjust=False):
    results=splitmonsters(romdata, jadjust=jadjust)
    for monster in results:
        test=results[monster]['local-offset'] == monster_offsets[monster][1]
        mname=monster_offsets[monster][0]
        moff=monster_offsets[monster][1]
        #print monster, results[monster]['local-offset'], test, mname, moff,
        print("%3d" % monster, hex(results[monster]['offset']), "%10s" % mname, end=' ')
        #print "%2d" % len(results[monster]['bytes']), results[monster]['bytes'],
        key='defense-traits'
        defense=bkeysstr(results[monster], 'defense-traits', '(immune:%s)')
        attacks=bkeysstr(results[monster], 'attack-traits', '<%s>')
        weakness=bkeysstr(results[monster], 'element-weakness', '(weak:%s)')
        spower="(sp:%s)" % results[monster].get('spell-power', {}).get('spell-power', None)
        print("Boss     " if results[monster]['boss']==1 else "Underling", end=' ')
        print("%s%s%s%s" % (monvalstr(results, monster, 'level'),
                            monvalstr(results, monster, 'hp'),
                            monvalstr(results, monster, 'xp'),
                            monvalstr(results, monster, 'gp')), end=' ')
        print(spower, defense, weakness)
