from .ff4data import *
from .resource import load
from .core import bytes2int, num2bytes, identity
romoffsets=load('romoffsets')
items=load('items')
from collections import defaultdict
itemcats=load('item-categories')
shoplist=load('shops')['order']
import random
shopsoff=romoffsets['shopdata']
from .output import stderr as errormsg

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

def tpassbuff(romdata):
    shop='troia-pass-items'
    additems2shop(romdata, shop, ['Bacchus',
                                  'SilkWeb',
                                  'StarVeil',
                                  'Elixir',
                                  'Spoon'])
    additems2shop(romdata, shop, ['Siren'])
