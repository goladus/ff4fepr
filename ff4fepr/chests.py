from .ff4data import *
from collections import defaultdict

def togp(intbyte):
    if intbyte < 0x80:
        small=(intbyte & 0x7f) * 10
        large = 0
    else:
        small = 0#(intbyte & 0x80) * 10
        large = (intbyte - 0x80) * 1000
    return (large + small)


def gp2intbyte(gp):
    if gp <= 1270:
        return gp // 10
    else:
        return (0x80 | (gp // 1000))


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
