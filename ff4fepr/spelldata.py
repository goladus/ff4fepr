from ff4data import *
spelldataoff=romoffsets['spellstats']
sprecord=romoffsets['spellstats-record']
spsize=romoffsets['spellstats-size']
spnum=romoffsets['spellstats-num']
spnames=romoffsets['player-spellnames']
spothernames=romoffsets['other-spellnames']
from ff4text import basicencode, encoding, testencode
from core import mergemaskedvalue, toint
from collections import defaultdict
import re

def splitsprecord(spr):
    results={}
    for key in sprecord:
        index, mask, shift = sprecord[key]
        results.setdefault(key, (spr[index] & mask) >> shift)
    return results

def sprecord2bytes(sprdict):
    bytesd=defaultdict(int)
    for key in sprecord:
        index, mask, shift = sprecord[key]
        bytesd[index] = mergemaskedvalue(bytesd[index], sprdict[key],
                                         [index, mask, shift])
    return [value for i, value in sorted(bytesd.items())]

def sprecords2rom(romdata, spstats):
    writelist=[]
    for index in range(len(spstats)):
        writelist += sprecord2bytes(spstats[index])
    for index, byt in enumerate(writelist):
        offset=spelldataoff+index
        if byt != romdata[offset]:
            romdata.addmod(offset, byt)

def testspelldata(romdata):
    sprecords2rom(romdata, loadspellstats(romdata))

def getspellnameoff(spellnum):
    if spellnum < romoffsets['player-spells']:
        key='player'
        nameindex=spellnum
    else:
        key='other'
        nameindex=spellnum-romoffsets['player-spells']
    offsetkey='%s-spellnames' % key
    sizekey='%s-spellnames-size' % key
    offset=romoffsets[offsetkey] + nameindex * romoffsets[sizekey]
    numbytes=romoffsets[sizekey]
    return (offset, numbytes)

def getspellname_bytes(romdata, spellnum):
    offset, numbytes = getspellnameoff(spellnum)
    return romdata[offset:offset+numbytes]

def getspellname(romdata, spellnum):
    offset, numbytes = getspellnameoff(spellnum)
    return ''.join([encoding[x] for x in romdata[offset:offset+numbytes]])

def birdcall(romdata):
    changespelltext(romdata, 'Cockatrice*', '<gr>Bird')
    changespelltext(romdata, 'DummyCock', 'Cocktric')

def changespelltext(romdata, spellname, newtext):
    spellnum=spells.index(spellname)
    offset, nbytes=getspellnameoff(spellnum)
    newencoding=basicencode(newtext)
    if len(newencoding) >= nbytes:
        newbytes=newencoding[:nbytes]
    else:
        newbytes=newencoding + [255] * (nbytes-len(newencoding))
    for index in range(nbytes):
        romdata.addmod(offset+index, newbytes[index])

def loadspellstats(romdata):
    results={}
    for index in range(spnum):
        offset=spelldataoff+(index * spsize)
        results.setdefault(index, {'bytes':
                                   romdata[offset:offset+spsize]})
        results[index].update(splitsprecord(romdata[offset:offset+spsize]))
        results[index]['text']=getspellname(romdata, index)
        results[index]['text-bytes']=getspellname_bytes(romdata, index)
        txtoff, txtlen=getspellnameoff(index)
        results[index]['text-len']=txtlen
        results[index]['text-offset']=txtoff
    return results

def dumpspellstats(romdata):
    spstats=sorted(loadspellstats(romdata).items())
    for index, spdata in spstats:
        spname="%s%s" % (spells[index], ' ' * (15 - len(spells[index])))
        print "%2x" % index, spname, "|", spdata['text'], spdata['cast-time'], spdata['attack']
        #print "%2x" % index, spname, ' '.join(["%2x" % x for x in spdata['bytes']])

def changebossbit(romdata, hasbossbit=None, nobossbit=None):
    if hasbossbit is None:
        hasbossbit=[]
    if nobossbit is None:
        nobossbit=[]
    spellstats=loadspellstats(romdata)
    for spellname in hasbossbit:
        spellnum=spells.index(spellname)
        spellstats[spellnum]['boss-bit']=1
    for spellname in nobossbit:
        spellnum=spells.index(spellname)
        spellstats[spellnum]['boss-bit']=0
    sprecords2rom(romdata, spellstats)

def setspstat(romdata, spstatname, changes):
    spstats=loadspellstats(romdata)
    for spellname, newvalue in changes:
        spellnum=spells.index(spellname)
        spstats[spellnum][spstatname]=newvalue
    sprecords2rom(romdata, spstats)

def setcasttimes(romdata, argstring):
    changes=[]
    for spec in argstring.split(','):
        spellname, valstr = spec.split('=')
        changes.append((spellname, toint(valstr)))
    setspstat(romdata, 'cast-time', changes)

def ctrebalance(romdata):
    spstats=loadspellstats(romdata)
    changes=[]
    elementals='Fire2* Fire3* Ice-2* Ice-3* Lit-2* Lit-3* Shiva* Indra* Jinn*'.split(' ')
    changes += [(spname, 2) for spname in elementals]
    changes.append(('Titan*', 3))
    changes.append(('Mist*', 1))
    changes.append(('Meteo*', 5))
    changes.append(('Psych*', 2))
    setspstat(romdata, 'cast-time', changes)
