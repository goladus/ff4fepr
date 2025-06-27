from .ff4data import *
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
