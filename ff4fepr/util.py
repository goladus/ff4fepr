
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
