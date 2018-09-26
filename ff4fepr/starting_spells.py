from ff4data import *

def groupspells(romdata):
    index=0
    spellcount=1
    spellslen=romoffsets['starting-spells-len']
    results={0:[]}
    for spellnum in range(spellslen):
        offset = romoffsets['starting-spells'] + spellnum
        spell=spells[romdata[offset]]
        if spell == '255':
            index += 1
            spellcount=1
            if spellnum < (spellslen -1):
                results.setdefault(index, [])
        elif spellcount == 24:
            results[index].append(spell)
            index += 1
            spellcount=1
            results.setdefault(index, [])
        else:
            spellcount += 1
            results[index].append(spell)
    return [m for i, m in sorted(dict(results).items())]

def spellgroups2list(spellsbygroup):
    results=[]
    for spellgroup in spellsbygroup:
        for sp in spellgroup:
            results.append(sp)
        if len(spellgroup) < 24:
            results.append('255')
    return results        

def spellgroups2bytes(spellsbygroup):
    return [spells.index(sp) for sp in spellgroups2list(spellsbygroup)]

def update_starting_spells(romdata, spellsbygroup):
    stoffset=romoffsets['starting-spells']
    newlist=spellgroups2bytes(spellsbygroup)
    for spellnum, newbyte in zip(range(romoffsets['starting-spells-len']),
                                 newlist):
        offset=stoffset + spellnum
        if romdata[offset] != newbyte:
            romdata.addmod(offset, newbyte)

def addspells(spellsbygroup, spellset, spells2add):
    spellset_index=romoffsets['spells-order'].index(spellset)
    splist=spellsbygroup[spellset_index]
    empty_slots = 24 - len(splist)
    for spell in spells2add[:empty_slots]:
        spellsbygroup[spellset_index].append(spell)

def addspells2rom(romdata, changesets):
    spg=groupspells(romdata)
    for spellset, spells2add in changesets:
        addspells(spg, spellset, spells2add)
    update_starting_spells(romdata, spg)

def dumpspells(romdata):
    results=[]
    for spellnum in range(romoffsets['starting-spells-len']):
        offset = romoffsets['starting-spells'] + spellnum
        spell=spells[romdata[offset]]
        results.append((offset, spell))
    return results
