from ff4data import *
from resource import load
from core import bytes2int, num2bytes, identity, toint
romoffsets=load('romoffsets')
items=load('items')
from collections import defaultdict
itemcats=load('item-categories')
import random

def weaponrecord(bytevalue, record):
    if record in romoffsets['split-weapondata']:
        x, mask, rshift = romoffsets['split-weapondata'][record]
        return (bytevalue & mask) >> rshift
    else:
        return bytevalue

def tobytelist(wd_record):
    dresults=defaultdict(int)
    for record, splitrecord in romoffsets['split-weapondata'].items():
        index, mask, lshift = splitrecord
        dresults[index]=(dresults[index] & ~ mask) | (wd_record[record] << lshift)
    for index, record in enumerate(romoffsets['weapondata-record']):
        if record not in romoffsets['split-weapondata']:
            dresults[index]=wd_record[record]
    result=[byteval for index, byteval in sorted(dict(dresults).items())]
    return result

def loadweapons(romdata):
    results={}
    weapondata=romoffsets['weapondata']
    wsize=romoffsets['weapondata-size']
    weaponspellpower=romoffsets['weaponspellpower']
    weaponspellvisual=romoffsets['weaponspellvisual']
    for windex in range(romoffsets['numweapons']):
        dataoff=weapondata+windex*wsize
        sppoff=weaponspellpower + windex
        spvoff=weaponspellvisual + windex
        weaponname=items[windex]
        results.setdefault(weaponname, {})
        for index, record in enumerate(romoffsets['weapondata-record']):
            record_offset=dataoff+index
            value=weaponrecord(romdata[record_offset], record)
            results[weaponname].setdefault(record, value)
        results[weaponname]['uktohit']=weaponrecord(romdata[dataoff+1],
                                                    'uktohit')
        results[weaponname]['spellpower']=romdata[sppoff]
        results[weaponname]['spellvisual']=romdata[spvoff]
    return results

def list2romwkey(romdata, datalist, offset_key):
    for index, byteval in enumerate(datalist):
        offset=romoffsets[offset_key]+index
        if romdata[offset] != byteval:
            romdata.addmod(offset, byteval)

def weapon2rom(romdata, weapondict):
    weapondata_list=[]
    weaponsp_list=[]
    weaponsv_list=[]
    for weapon in items[:romoffsets['numweapons']]:
        weapondata_list += tobytelist(weapondict[weapon])
        weaponsp_list.append(weapondict[weapon]['spellpower'])
        weaponsv_list.append(weapondict[weapon]['spellvisual'])
    list2romwkey(romdata, weapondata_list, 'weapondata')
    list2romwkey(romdata, weaponsp_list, 'weaponspellpower')
    list2romwkey(romdata, weaponsv_list, 'weaponspellvisual')

def dump2screen(romdata):
    import sys
    wdata=loadweapons(romdata)
    for w, records in wdata.items():
        sys.stdout.write("%15s " % w)
        sys.stdout.write(' '.join(["%s:%s" % (record, records[record])
                                   for record in records]))
        sys.stdout.write('\n')

def addspell2weapon(romdata, weaponame, spellname, spellpower, spellvisual=None):
    addspells2weapons(romdata, [(weaponname, spellname, spellvisual, spellpower)])

def replaceweaponspell(romdata, weaponname, spellname):
    wdata=loadweapons(romdata)
    wdata[weaponname]['casts']=spells[spellname]
    weapon2rom(romdata, wdata)

def addspells2weapons(romdata, changes):
    wdata=loadweapons(romdata)
    for wname, spname, spvisual, sppower in changes:
        wdata[wname]['casts']=spells.index(spname)
        wdata[wname]['spellvisual']=spells.index(spvisual)
        wdata[wname]['spellpower']=toint(sppower)
    weapon2rom(romdata, wdata)

def addspells2weapons_arg(romdata, arglist):
    wspecs=arglist.split(',')
    changes=[]
    for wspec in wspecs:
        wname, spdata = wspec.split('=')
        spname, spvisual, sppower = spdata.split(':')
        changes.append((wname, spname, spvisual, sppower))
    addspells2weapons(romdata, changes)

def hitcalc(atk, tohit, charbackrow=False, jump=False, stats=None,
            enemybackrow=False,
            basemult=None,
            enemy_defense=0,
            enemy_defmult=0,
            enemy_evasion=0):
    'unfinished'
    if stats is None:
        stats={'level': 50}
    hitrate=min((tohit + stats['level']/4), 99)
    if jump:
        hitrate += stats['level']/4
    if charbackrow:
        hitrate = hitrate * 0.5
    if enemybackrow:
        hitrate = hitrate * 0.5
    if basemult is None:
        basemult=stats.get('str', 50)/8 + stats.get('agi', 20)/16 + 1
    basedef=enemy_defense
    if enemybackrow:
        defense = basedef * 2

def hitrating(romdata):
    import sys
    wdata=loadweapons(romdata)
    for w, records in wdata.items():
        hitest=int(100 * (records['attack'] * ((records['tohit']+13)/100.0)))
        sys.stdout.write('%5d ' % hitest)
        sys.stdout.write("%15s " % w)
        sys.stdout.write(' '.join(["%s:%s" % (record, records[record])
                                   for record in ['attack', 'tohit']]))
        sys.stdout.write('\n')


def combine_categories(categories):
    if (categories is None or categories == ['ALL']):
        return items[1:romoffsets['numweapons']]
    else:
        return reduce(lambda x, y: x + y, [itemcats[category]
                                           for category in categories])

def shuffle_weaponstat(romdata, weaponstat, categories=None):
    """Shuffles the attack power of all weapons within the specified categories with each other"""
    weapondict=loadweapons(romdata)
    weapon_list=combine_categories(categories)
    oldvalues=[weapondict[weapon][weaponstat] for weapon in weapon_list]
    values=[weapondict[weapon][weaponstat] for weapon in weapon_list]
    random.shuffle(values)
    changes=zip(weapon_list, oldvalues, values)
    for weapon, value in zip(weapon_list, values):
        weapondict[weapon][weaponstat]=value
    weapon2rom(romdata, weapondict)
    return changes

def between(b0, value, b1):
    return max(b0, min(b1, value))

def vary_weaponstat(romdata, weaponstat, variance, categories=None):
    lower, upper = variance
    def variancefunc(statvalue):
        newval = statvalue + random.randint(lower, upper)
        if newval > 255:
            return 255
        elif newval < 0:
            return 0
        else:
            return newval
    return modify_weaponstat(romdata, weaponstat, categories, modfunc=variancefunc)

def modify_weaponstat(romdata, weaponstat, categories=None, modfunc=identity):
    weapondict=loadweapons(romdata)
    weapon_list=combine_categories(categories)
    oldvalues=[weapondict[weapon][weaponstat] for weapon in weapon_list]
    values=[modfunc(weapondict[weapon][weaponstat]) for weapon in weapon_list]
    changes=zip(weapon_list, oldvalues, values)
    for weapon, value in zip(weapon_list, values):
        weapondict[weapon][weaponstat]=value
    weapon2rom(romdata, weapondict)
    return changes

def modup_weaponatk(romdata):
    changes=[]
    vwfn=lambda c, vl, vu: vary_weaponstat(romdata, 'attack', (vl, vu), categories=c)
    changes += shuffle_weaponstat(romdata, 'attack', categories=['longswords', 'axes1h'])
    
    changes += shuffle_weaponstat(romdata, 'attack', categories=['spears'])
    changes += vwfn(['rods', 'staves'], 0, 30)
    changes += vwfn(['darkswords'], 10, 100)
    changes += modify_weaponstat(romdata, 'attack', categories=['harps'],
                                 modfunc=lambda x: between(0, x*random.randint(2,5), 210))
    changes += vwfn(['hammers', 'axes2h'], -10, 35)
    changes += vwfn(['boomerangs'], -20, 40)
    return changes
