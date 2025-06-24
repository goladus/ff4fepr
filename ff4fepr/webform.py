from .util import parse_string_args_nodashes as psa
from .ff4data import *

def checkbox(flagname, helptext):
    return '<input type="checkbox" name="%s">%s' % (flagname, helptext)

def genform1(args):
    print("<form>")
    dt=[checkbox(itm[0], itm[1]['help']) for itm in psa(args.string_of_flags)
        if not (itm[0].startswith('dump') or itm[0].startswith('test'))]
    print('<br>\n'.join(dt))
    print('<br>\n')
    print('<input type="button" onclick="alert(\'Boo\')" value="Submit">')
    print("</form>")
