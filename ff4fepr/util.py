
def parse_string_args(longstring):
    lines=longstring.split('\n')
    results=[]
    for line in lines:
        ln=line.strip()
        if ln != '':
            if ' ' in line:
                firstspace=ln.index(' ')
                arg = ln[:firstspace]
                helptext = ln[firstspace+1:].strip()
                results.append(("--%s" % arg, {'help':helptext}))
            else:
                results.append(("--%s" % ln, {}))
    return results

def parse_string_args_nodashes(longstring):
    lines=longstring.split('\n')
    results=[]
    for line in lines:
        ln=line.strip()
        if ln != '':
            if ' ' in line:
                firstspace=ln.index(' ')
                arg = ln[:firstspace]
                helptext = ln[firstspace+1:].strip()
                results.append(("%s" % arg, {'help':helptext}))
            else:
                results.append(("%s" % ln, {}))
    return results

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


def dumpaddrs(start, count, increment):
    for x in range(start, start+(count*increment), increment):
        print(hex(x))
