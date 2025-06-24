from . import ff4data
from .starting_spells import addspells2rom
from .learned_spells import replace_learned_spells
from .learned_spells import loadlearnedspells, update_learned_spells
from .resource import load
from .core import toint
import random
romoffsets=load('romoffsets')

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

def randomlevelfunc2(splevel, minlevel, maxlevel=70, extra=None,
                     level_modifier=100):
    for lev in range(maxlevel):
        chance=1000/(splevel * (level_modifier/100.0))
        if chance >= random.randint(1,1000):
            return max(lev, minlevel)
    return maxlevel

def randomize_learned_spells1(romdata, spellsetnames, fn=randomlevelfunc1, **kwargs):
    learned=loadlearnedspells(romdata)
    for spellsetname in spellsetnames:
        newset=[]
        if len(learned[spellsetname]) > 0:
            minlev=learned[spellsetname][0][0]
        for level, spname in learned[spellsetname]:
            newlevel = fn(level, minlev, extra={'spellname': spname}, **kwargs)
            newset.append([newlevel, spname])
        learned[spellsetname]=sorted(newset)
    update_learned_spells(romdata, learned)

def randomize_learned_spells2(romdata, level_modifier=100):
    '''randomizes all learned spells for all spellsets'''
    randomize_learned_spells1(romdata, romoffsets['spells-order'],
                              fn=randomlevelfunc2,
                              level_modifier=level_modifier)

def randomize_learned_spells3(romdata, difficulty_ratio=None):
    randomize_learned_spells1(romdata, romoffsets['spells-order'],
                              fn=randomlevelfunc3,
                              difficulty_ratio=difficulty_ratio)

oddslst=[(0, 5) for x in range(1,101) if x<=50]
oddslst+=[(6, 10) for x in range(1,101) if 50<x<=75]
oddslst+=[(11, 20) for x in range(1,101) if 75<x<=91]
oddslst+=[(21, 40) for x in range(1,101) if 91<x<=99]
oddslst+=[(41, 60) for x in range(1,101) if x==100] #could just write [(41,60)]

def randomlevelfunc3(splev, minlevel, difficulty_ratio=None, extra=None):
    if difficulty_ratio is None:
        negative_adjust=1
        positive_adjust=1
    else:
        if isinstance(difficulty_ratio, str):
            negative_adjust, positive_adjust=map(toint, difficulty_ratio.split(':'))
        else:
            negative_adjust, positive_adjust=difficulty_ratio
    absdiff=random.randint(*random.choice(oddslst))
    sign=random.choice([-1] * negative_adjust + [1] * positive_adjust)
    return max(splev + (sign * absdiff), minlevel)
