from .ff4data import *
from .core import toint
encoding=load('text-encoding')
import re
token=re.compile('(<.*>)')

def basicencode(astring):
    results=[]
    encodingitems=encoding.items()
    encodemap=dict([(v, k) for k, v in encodingitems])
    for segment in re.split(token, astring):
        if segment.startswith('<'):
            results.append(encodemap[segment])
        else:
            for ch in segment:
                results.append(encodemap[ch])
    return results

def testencode(astring):
    encoded=basicencode(astring)
    print(encoded, end=' ')
    print(''.join([encoding[x] for x in encoded]))


def encode(arg):
    encoded = basicencode(arg)
    print(','.join([hex(x) for x in encoded]))


def decode(arg):
    print(dodecode([toint(x) for x in arg.split(',')]))


def dodecode(lst):
    return ''.join([encoding[x] for x in lst])
