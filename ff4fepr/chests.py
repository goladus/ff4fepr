from .ff4data import *
from collections import defaultdict
from .core import toint
from .util import togp, gp2intbyte

vchest_offsets = load('ff2us_manual_chests')


def loadchests(romdata):
    results = {}
    for zone, zonedata in chests.items():
        for chestname, offset in zonedata.items():
            results[chestname] = {}
            chestkey = romdata[offset-1]
            results[chestname]['offset'] = offset
            results[chestname]['_key'] = chestkey
            results[chestname]['trapped'] = (chestkey & 0xc0) == 0xc0
            results[chestname]['gp'] = chestkey == 0
            results[chestname]['contents'] = items[romdata[offset]] if chestkey != 0 else togp(romdata[offset]) 
            results[chestname]['allbytes'] = romdata[offset-1:offset+4]
    return results


def write_chest_contents(romdata, chestdict):
    # NOTE Currently, can only change chest contents.
    for zone, zonedata in chests.items():
        for chestname, offset in zonedata.items():
            contents = chestdict[chestname]['contents']
            if isinstance(contents, str):
                if not chests[chestname]['gp']:
                    item_byte = items.index(contents)
                    romdata.addmod(offset, item_byte)
                else:
                    print("Error: tried to change gp chest to item (not yet implemented)")
            elif isinstance(contents, int):
                if chests[chestname]['gp']:
                    romdata.addmod(offset, contents)
                else:
                    print("Error: tried to change item chest to gp (not yet implemented)")

def xdumpchests(romdata):
    loaded_chests = loadchests(romdata)
    try:
        for chestname in loaded_chests:
            print("- [%s, [%s]]" % (chestname, ', '.join(['0x%x' % x for x in loaded_chests[chestname]['allbytes']])))
        #print(chestname, loaded_chests[chestname]['contents'], '[%s]' % ', '.join(['0x%x' % x for x in loaded_chests[chestname]['allbytes']]))
    except BrokenPipeError:
        import sys
        sys.exit(32)


def dumpchests(romdata):
    loaded_chests = loadchests(romdata)
    try:
        for chestname in loaded_chests:
            offset = loaded_chests[chestname]['offset']
            allbytes_string = ', '.join(['0x%x' % x for x in loaded_chests[chestname]['allbytes']])
            contents = loaded_chests[chestname]['contents']
            print("- [%s, %x, %s, [%s]]" % (chestname,  offset, contents, allbytes_string))
        #print(chestname, loaded_chests[chestname]['contents'], '[%s]' % ', '.join(['0x%x' % x for x in loaded_chests[chestname]['allbytes']]))
    except BrokenPipeError:
        import sys
        sys.exit(32)


def dumpchests2(romdata):
    loaded_chests = loadchests(romdata)
    try:
        for chestname in loaded_chests:
            offset = loaded_chests[chestname]['offset']
            allbytes_string = ', '.join(['0x%x' % x for x in loaded_chests[chestname]['allbytes']])
            contents = loaded_chests[chestname]['contents']
            print("%s: 0x%x, # %s, %s" % (chestname,  offset-1, contents, allbytes_string))
        #print(chestname, loaded_chests[chestname]['contents'], '[%s]' % ', '.join(['0x%x' % x for x in loaded_chests[chestname]['allbytes']]))
    except BrokenPipeError:
        import sys
        sys.exit(32)


def sparse_compare(lst1, lst2, indices):
    for i in indices:
        if lst1[i] != lst2[i]:
            return False
    return True


def sparsefind(romdata, querylist, indices):
    qlen = len(querylist)
    results = []
    for offset in range(0, len(romdata) - qlen):
        if sparse_compare(querylist, romdata[offset:offset+qlen], indices):
            results.append(offset)
    return results


def chestsearch2(romdata, chestdata):
    return sparsefind(romdata, chestdata, [0, 1, 4])
    #return sparsefind(romdata, chestdata, list(range(len(chestdata)-1)))


def vanilla_search(romdata):
    MIN_OFFSET=0xa8300
    from .resource import load
    import yaml
    results = {}
    fe_vanilla_chests = load('fe-vanilla-chests')
    chest_counts = defaultdict(int)
    for chestname, chestdata in fe_vanilla_chests:
        countkey = ','.join(['%x' % x for x in chestdata])
        result = [x for x in chestsearch2(romdata, chestdata) if x >= MIN_OFFSET]
        if len(result) > 0:
            try:
                chest_offset = result[chest_counts[countkey]]
                results[chestname] = chest_offset
                chest_counts[countkey] += 1
            except IndexError:
                results[chestname] = None
        else:
            results[chestname] = None
    for name, offset in results.items():
        if offset is not None:
            print("%s: %x" % (name, offset))
        else:
            print("%s: null" % name)
    return results


def chestsearch(romdata):
    #[0x80, 0xce, X, X, X][0x80, 0xce, X, X, X]
    #[0, 1, 5, 6]
    baronpot_outside_rosa = [0x80, 0xce, 0x18, 0x1b, 0xfe]
    baronpot_outside_inn  = [0x80, 0xce, 0x1b, 0x1a, 0xfe]
    baron2pots = baronpot_outside_rosa + baronpot_outside_inn
    baronpot_indices2check = [0, 1, 5, 6]
    results = sparsefind(romdata, baron2pots, baronpot_indices2check)
    for x in results:
        print("%x" % x)


def vanichest_edit(romdata, arg):
    #chestoffsets = load('ff2us_manual_chests')
    chestoffsets = vchest_offsets
    if isinstance(arg, str):
        chestname, newitem = arg.split('=')
    elif isinstance(arg, list) or isinstance(arg, tuple):
        chestname, newitem = arg
    if isinstance(newitem, int):
        newgp = newitem
    elif newitem.isdigit():
        newgp = gp2intbyte(toint(newitem))
    else:
        newgp = False
    eventoff = chestoffsets[chestname]
    oldgp_flag = (romdata[eventoff] & 0x80) == 0
    if oldgp_flag:
        contents = togp(romdata[eventoff+1])
    else:
        contents = items[romdata[eventoff+1]]
    if newgp is False:
        print(contents, '->', newitem)
        if oldgp_flag:
            romdata.addmod(eventoff, romdata[eventoff] | 0x80)
        romdata.addmod(eventoff+1, items.index(newitem))
    else:
        print(contents, '->', toint(newitem))
        if not oldgp_flag:
            romdata.addmod(eventoff, romdata[eventoff] & ~(0x80))
        romdata.addmod(eventoff+1, newgp)


def dump_vanichests(romdata):
    chestoffsets = load('ff2us_manual_chests')
    for chestname, offset in sorted(chestoffsets.items()):
        if (romdata[offset] & 0x80) == 0:
            contents = "%s GP" % togp(romdata[offset+1])
        else:
            contents = items[romdata[offset+1]]
        print(chestname, hex(offset), '#', contents)


## Cure2
cure2_offsets = [
    0xa8655, # 0x80,0xcf,0x2,0x10,0xfe
    0xa865a, # 0x80,0xcf,0x3,0x10,0xfe
    0xa86fa, # 0x80,0xcf,0x10,0x1d,0xfe
    0xa8835, # 0x80,0xcf,0x6,0x3,0xfe
    0xa88b2, # 0x80,0xcf,0x5,0x3,0xfe
    0xa88b7, # 0x80,0xcf,0x7,0x3,0xfe
    0xa8916, # 0x80,0xcf,0x4,0x6,0xfe
    0xa8952, # 0x80,0xcf,0xe,0x3,0xfe
    0xa8957, # 0x80,0xcf,0xe,0x4,0xfe
    0xa8984, # 0x80,0xcf,0x8,0x8,0xfe
    0xa8989, # 0x80,0xcf,0xa,0x5,0xfe
    0xa89b1, # 0x80,0xcf,0x1,0x6,0xfe
    0xa8af1, # 0x80,0xcf,0xf,0x3,0xfb
    0xa8b96, # 0x80,0xcf,0x2,0x8,0xfe
    0xa8ba5, # 0x80,0xcf,0x16,0xf,0xfe
    0xa8dad, # 0x80,0xcf,0x15,0x14,0xfe
    0xa8e43, # 0x80,0xcf,0x10,0xb,0xfe
    0xa8e4d, # 0x80,0xcf,0x14,0xc,0xfe
    0xa8ec0, # 0x80,0xcf,0xe,0x7,0xfe
    #0xa8f0b, # 0x80,0xcf,0x2,0xa,0xfe
    #0xa8f38, # 0x80,0xcf,0xa,0x4,0xfe
    #0xa8f3d, # 0x80,0xcf,0xb,0x5,0xfe
    #0xa9087, # 0x80,0xcf,0x2,0x14,0x1e
    #0xa909b, # 0x90,0xcf,0x9,0x15,0xff
    0xa913b, # 0x80,0xcf,0xe,0x4,0x27
    #0xa91ae, # 0x80,0xcf,0x3,0x11,0x37
    #0xa91c2, # 0x80,0xcf,0x1c,0x10,0x38
    #0xa91d1, # 0x80,0xcf,0x4,0x15,0xfe
    #0xa9285, # 0x80,0xcf,0x3,0x12,0xfe
    #0xa9299, # 0x80,0xcf,0x1d,0x5,0xfe
    #0xa92b7, # 0x80,0xcf,0x19,0x1c,0xfe
    0xa92cb, # 0x80,0xcf,0x17,0xf,0xfe
    0xa92f8, # 0x80,0xcf,0xb,0x4,0xfe
    0xa937f, # 0x80,0xcf,0x10,0x7,0xfe
    0xa941f, # 0x80,0xcf,0xa,0xa,0xfe
    0xa94ab, # 0x80,0xcf,0x1d,0x7,0xfe
    ]

def set_cure2_chests_for_checking(romdata):
    for index, offset in enumerate(cure2_offsets):
        romdata.addmod(offset+1, index+1) # Set the item value (offset+1) to the next item in the list

def revert_cure2_chests(romdata):
    for index, offset in enumerate(cure2_offsets):
        romdata.addmod(offset+1, 0xcf)


def bulk_edit_vchest(romdata, arg):
    from yaml import safe_load
    changes = safe_load(open(arg))
    for chst, itm in changes.items():
        vanichest_edit(romdata, (chst, itm))

