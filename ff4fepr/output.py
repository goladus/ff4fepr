import sys

def nullfunc(*args, **kwargs):
    'this function accepts any arguments, does nothing, and returns None'
    return None

stdout=sys.stdout.write
stderr=sys.stderr.write

error=stderr
warning=stderr

def optional_output(args):
    return (stderr if args.debug else nullfunc,
            stdout if args.verbose else nullfunc)
