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
