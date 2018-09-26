import ff4data
from starting_spells import addspells2rom
from learned_spells import replace_learned_spells
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
