from ff4data import *
import ff4data
from resource import load
from core import bytes2int, num2bytes, identity, toint
romoffsets=load('romoffsets')
items=load('items')
from collections import defaultdict
itemcats=load('item-categories')
import random
from ff4text import basicencode, encoding
from allitems import changeitemname, dumpnames

rando_element=load('rando-weapon-element')

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
        for record in romoffsets['weapondata-record']:
            index=romoffsets['weapondata-record-dict'][record]
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

def bytypeindex(romdata, keytype):
    wd=loadweapons(romdata)
    byindex=defaultdict(list)
    key='%s-index' % keytype
    for w, records in wd.items():
        if records[key] != 0:
            byindex[records[key]].append(w)
    return dict(byindex)

def dumpby(romdata, keytype):
    bei=bytypeindex(romdata, keytype)
    for thing in bei:
        print(thing, bei[thing])

def dumpracial(romdata):
    wd=loadweapons(romdata)
    key='racial-bit'
    for w, records in wd.items():
        if records[key]:
            print(w, bin(records[key]))

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
        hitest=int(100 * (records['attack'] * ((records['tohit'])/100.0)))
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

def modify_single_weapon(romdata, weapon, stat, newvalue):
    weapondict=loadweapons(romdata)
    weapondict[weapon][weaponstat]=newvalue
    weapon2rom(romdata, weapondict)

def anyweapon(romdata):
    wd=loadweapons(romdata)
    for weapon in wd:
        wd[weapon]['equip-index']=0
    weapon2rom(romdata, wd)

def edspoon(romdata):
    wd=loadweapons(romdata)
    wd['Spoon']['equip-index']=ff4data.eqindexes['harps']
    #wd['Spoon']['attack']=235
    weapon2rom(romdata, wd)

def edweaponbuff(romdata):
    wd=loadweapons(romdata)
    charmharp=232
    dreamerharp=231
    silverdagger=230
    dancingdagger=240
    wd['Charm Harp']['attack']=charmharp
    wd['Dreamer Harp']['attack']=dreamerharp
    wd['Silver Dagger']['attack']=silverdagger
    wd['Dancing Dagger']['attack']=dancingdagger
    weapon2rom(romdata, wd)
    changeitemname(romdata, "Charm Harp",    "<harp>Charm%s" % charmharp)
    changeitemname(romdata, "Dreamer Harp",  "<harp>Dream%s" % dreamerharp)
    changeitemname(romdata, "Silver Dagger", "<knife>Silv%s" % silverdagger)
    changeitemname(romdata, "Dancing Dagger", "<knife>Danc%s" % dancingdagger)

def staffcheat(romdata):
    addspells2weapons(romdata, [('Staff', 'Comet*', "Shell*", 200),
                                ('Silver Staff', 'MegaNuke', 'Bersk*', 100),
                                ('Silver Dagger', 'Storm', 'Storm', 10),
                                ('Assassin', 'Disrupt', 'Venom*', 10)])

def medusa2x(romdata):
    wd=loadweapons(romdata)
    etypes=[x for x in rando_element['element-types'].keys()
            if ((x != 'Medusa') and
                (x != 'Curse') and
                ('-Air' not in x) and
                ('-Whip' not in x))]
    special1=random.choice(etypes)
    atk=random.randint(20, 150)
    tohit=random.randint(75, 95)
    wname='Medusa Sword'
    wd[wname]['equip-index']=6 #Axes
    wd[wname]['element-index']=rando_element['element-types'][special1]
    wd[wname]['attack']=atk
    wd[wname]['tohit']=tohit
    weapon2rom(romdata, wd)
    newtag=special1 + (5-len(special1)) * ' '
    atkstr="%s" % atk
    newname="<sword>%s%s" % (newtag[:5], atkstr)
    print("Medusa Sword -> %s" % newname)
    changeitemname(romdata, "Medusa Sword", newname)

def spoonjoke(romdata):
    wd=loadweapons(romdata)
    changeitemname(romdata, 'Spoon', '<ring>Spoon')
    weapon2rom(romdata, wd)

def ancient2coral(romdata):
    ## Still need to change attack visual to dragoon spear animation
    wd=loadweapons(romdata)
    wd['Ancient Sword']['element-index']=3
    wd['Ancient Sword']['tohit']=80
    wd['Ancient Sword']['attack']=39
    weapon2rom(romdata, wd)
    changeitemname(romdata, "Ancient Sword", "<sword>Coral")
