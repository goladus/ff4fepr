import yaml
from pprint import pprint as pp
def dumpall(romdata, args):
    args.string_of_args=None
    args.string_of_flags=None
    pp(args.__dict__)
    pp(romdata.mdiff())
