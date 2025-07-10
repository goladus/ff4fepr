from .ff4data import *
from .resource import load
from .core import bytes2int, num2bytes, identity, toint
romoffsets=load('romoffsets')
items=load('items')
from collections import defaultdict
itemcats=load('item-categories')
shoplist=load('shops')['order']
import random
import os
VANILLA_ROM = os.getenv('VANILLA_ROM', False)
if VANILLA_ROM is False:
    shopsoff=romoffsets['shopdata']
else:
    shopsoff=romoffsets['shopdata-vanilla-qol']
from .output import stderr as errormsg
import sys

def getshopoff(shopname):
    shopnum=shoplist.index(shopname)
    return shopsoff + (shopnum * 8)

def getshoplist(romdata, shopname):
    shopoff=getshopoff(shopname)
    return [items[x] for x in romdata[shopoff:shopoff+8]]

def getfreeslotinshop(romdata, shopname):
    shopoff=getshopoff(shopname)
    for slot, itemnum in enumerate(romdata[shopoff:shopoff+8]):
        if items[itemnum] == 'TRASH':
            return slot
    return None

def additems2shop(romdata, shopname, itemnames):
    shopoff=getshopoff(shopname)
    firstslot=getfreeslotinshop(romdata, shopname)
    if firstslot is None:
        errormsg("No free slots in %s\n" % shopname)
        return None
    for newitemnum, itemname in enumerate(itemnames):
        slotnum=firstslot+newitemnum
        if slotnum > 8:
            errormsg("Could not add %s to %s, no free slots\n" % (itemname,
                                                                  shopname))
        else:
            romdata.addmod(shopoff+slotnum, items.index(itemname))


def loadshops(romdata):
    """NOTE: Shop locations seem to be different in qol rom vs free enterprose"""
    loaded_shops = {}
    warned = False
    for shopname in shoplist:
        loaded_shops[shopname] = getshoplist(romdata, shopname)
        if loaded_shops[shopname][0] == 'TRASH' and warned is False:
            sys.stderr.write("Warning: empty shop (%s), should VANILLA_ROM=1 be set?\n" % shopname)
            warned = True
    return loaded_shops


def writeshops(romdata, loaded_shops):
    for shopname, shoplist in loaded_shops.items():
        shopoff=getshopoff(shopname)
        if len(shoplist) == 8:
            for slotnum, itemname in enumerate(shoplist):
                romdata.addmod(shopoff+slotnum, items.index(itemname))
        else:
            sys.stderr.write("Error: shop %s doesn't have 8 slots: [%s](%s)\n" % (shopname, ','.join(shoplist), len(shoplist)))


def testshops(romdata):
    writeshops(romdata, loadshops(romdata))


def dumpshops(romdata):
    loaded_shops = loadshops(romdata)
    for shopname in shoplist:
        print(f"== {shopname} ==")
        for slotnum, itemname in enumerate(loaded_shops[shopname]):
            print(slotnum, itemname)


def modify_shop(romdata, args):
    loaded_shops = loadshops(romdata)
    shopname, remainder = args.split(':')
    for modass in remainder.split(','):
        slotstr, newitem = modass.split('=')
        slotnum = toint(slotstr)
        loaded_shops[shopname][slotnum] = newitem
    writeshops(romdata, loaded_shops)


def tpassbuff(romdata):
    shop='troia-pass-items'
    additems2shop(romdata, shop, ['Bacchus',
                                  'SilkWeb',
                                  'StarVeil',
                                  'Elixir',
                                  'Spoon'])
    additems2shop(romdata, shop, ['Siren'])
