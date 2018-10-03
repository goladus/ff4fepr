import ff4data
from starting_spells import addspells2rom
from learned_spells import replace_learned_spells
from learned_spells import loadlearnedspells, update_learned_spells
from core import toint
import random

def rydiacalls_random(romdata, args):
    n=toint(args)
    n=4 if n > 4 else n
    spellset, spells2add = ff4data.modding['spellsets']['rydia-bonus-calls'][0]
    random.shuffle(spells2add)
    addspells2rom(romdata, [(spellset, spells2add)])

def rydiacalls(romdata, args):
    splist=args.split(',')
    addspells2rom(romdata, [('rydia-call', splist)])

def addspellset(romdata, spellsetname):
    addspells2rom(romdata,
                  ff4data.modding['spellsets'][spellsetname])

def replacelearnedsets(romdata, learnedspellskey):
    replace_learned_spells(romdata,
                           ff4data.modding['learnedsets'][learnedspellskey])

def randomlevelfunc1(splevel, minlevel, maxlevel=70, extra=None):
    for lev in range(maxlevel):
        chance=1000/(splevel*1.5)
        if chance >= random.randint(1, 1000):
            return max(lev, minlevel)
    return maxlevel

def randomize_learned_spells1(romdata, spellsetnames, fn=randomlevelfunc1):
    learned=loadlearnedspells(romdata)
    for spellsetname in spellsetnames:
        newset=[]
        if len(learned[spellsetname]) > 0:
            minlev=learned[spellsetname][0][0]
        for level, spname in learned[spellsetname]:
            newlevel = fn(level, minlev, extra={'spellname': spname})
            newset.append([newlevel, spname])
        learned[spellsetname]=sorted(newset)
    update_learned_spells(romdata, learned)

