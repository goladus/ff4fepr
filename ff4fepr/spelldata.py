from ff4data import *
spelldataoff=romoffsets['spellstats']
sprecord=romoffsets['spellstats-record']
spsize=romoffsets['spellstats-size']
spnum=romoffsets['spellstats-num']
spnames=romoffsets['player-spellnames']
spothernames=romoffsets['other-spellnames']
encoding=load('text-encoding')
from core import mergemaskedvalue
from collections import defaultdict

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

def getspellname(romdata, spellnum):
    "doesn't work yet"
    if spellnum < romoffsets['player-spells']:
        key='player'
    else:
        key='other'
    offsetkey='%s-spellnames' % key
    sizekey='%s-spellnames-size' % key
    offset=romoffsets[offsetkey] + spellnum * romoffsets[sizekey]
    numbytes=romoffsets[sizekey]
    return ''.join([encoding[x] for x in romdata[offset:offset+numbytes]])

def loadspellstats(romdata):
    results={}
    for index in range(spnum):
        offset=spelldataoff+(index * spsize)
        results.setdefault(index, {'bytes':
                                   romdata[offset:offset+spsize]})
        results[index].update(splitsprecord(romdata[offset:offset+spsize]))
    return results

def dumpspellstats(romdata):
    spstats=sorted(loadspellstats(romdata).items())
    for index, spdata in spstats:
        spname="%s%s" % (spells[index], ' ' * (15 - len(spells[index])))
        print "%2x" % index, spname, spdata
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
