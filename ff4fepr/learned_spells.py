from .ff4data import *
import yaml
import json

def split_learnspell_list(lslist):
    results=[]
    lspsize=romoffsets['learned-spells-size']
    for i in range(0, len(lslist), lspsize):
        level, spellnum = lslist[i:i+lspsize]
        spellname=spells[spellnum]
        results.append([level, spellname])
    return results

def dump2screen(romdata):
    learned=loadlearnedspells(romdata)
    data=[{chname: learned[chname]} for chname in romoffsets['spells-order']]
    print(yaml.dump(data))
#    for chname, learned in data:
#        for lvl, spname in learned:
#            print "%s  %s %s" % (chname, lvl, spname)

def loadlearnedspells(romdata):
    lsp=romoffsets['learned-spells']
    lsplen=romoffsets['learned-spells-len']
    index=0
    groups={0:[]}
    results={}
    for onebyte in range(lsplen):
        offset=lsp+onebyte
        if romdata[offset] == 0xff:
            if index < len(romoffsets['spells-order']):
                results.setdefault(romoffsets['spells-order'][index],
                                   split_learnspell_list(groups[index]))
            index += 1
            groups.setdefault(index, [])
        else:
            groups[index].append(romdata[offset])
    return results

def learnedspells2bytes(lspd):
    results=[]
    for spellset in romoffsets['spells-order']:
        for level, spellname in lspd[spellset]:
            results.append(level)
            results.append(spells.index(spellname))
        results.append(0xff)
    return results

def update_learned_spells(romdata, learnedspellsdict):
    newbytes=learnedspells2bytes(learnedspellsdict)
    lsp=romoffsets['learned-spells']
    lsplen=romoffsets['learned-spells-len']
    for bytenum, newbyte in zip(range(lsplen), newbytes):
        if newbyte != romdata[lsp+bytenum]:
            romdata.addmod(lsp+bytenum, newbyte)

def replace_learned_spells(romdata, learnedsets):
    learnedspells=loadlearnedspells(romdata)
    for spellset, learninglist in learnedsets.items():
        learnedspells[spellset]=learninglist
    update_learned_spells(romdata, learnedspells)
