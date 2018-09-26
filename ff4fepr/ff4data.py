from resource import load
from pprint import pprint as pp

items=load('items')
spells=load('spells')
romoffsets=load('romoffsets')
shops=load('shops')
types=load('types')
monsters=load('monster-offsets')
eqindexes=load('equip-indexes')

modding={
    'weapon-spell': load('rando-weapon-spells'),
    'spellsets': load('rando-spellsets'),
    'learnedsets': load('rando-learnedsets')
    }

if __name__ == '__main__':
    pp(items)
    pp(spells)
    pp(romoffsets)
    pp(shops)
    pp(types)
    pp(monsters)
    pp(eqindexes)
    pp(modding)
