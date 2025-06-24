from . import ff4data
from .starting_spells import addspells2rom

def rydiacalls(romdata, args):
    n=toint(args.rydia_starting_calls)
    n=4 if n > 4 else n
    spellset, spells2add = ff4data.modding['spellsets']['rydia-bonus-calls']
    random.shuffle(spells2add)
    addspells2rom(romdata, [(spellset, spells2add)])
