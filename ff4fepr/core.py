import sys
import gzip
import copy

def nullfunc(*args, **kwargs):
    'this function accepts any arguments, does nothing, and returns None'
    return None

def identity(arg):
    return arg
#
#  Some intentially basic functions suitable for doing simple
#  scripted manipulations on binary files.
#  This works with both SNES roms and save state files.
#
#  Some Notes:
#    - Snes9x save states are gzip-compressed.
#    - Many Roms are zip-compressed and this framework
#      doesn't have a zipfile option yet.  But you can
#      always manually unzip a rom for editing.
#    - Sometimes I refer to "bytes" though they are
#      actually stored as python integers that are always
#      less than 256.  I find python bytes type to be more difficult
#      to use and not necessary for simple rom and savestate
#      hacking.

def simple_load(fname):
    """Reads an entire binary file into a list of integers
    and returns the list.  This is not intended for very large
    files or when memory is limited."""
    with open(fname, 'rb') as file_handle:    # Open file for binary reading
        integer_list=map(ord, file_handle.read())   # Read the file and convert each byte to an integer value
    return integer_list

def gzip_load(fname):
    """Reads a gzip-compressed binary file into a list of integers
    and returns the list.  This is not intended for very large
    files or when memory is limited."""
    with open(fname, 'rb') as file_handle:    # Open file for binary reading
        file_contents=map(ord, file_handle.read())   # Read the file and convert each byte to an integer value
    return file_contents

def simple_write(integer_list, fname):
    """Converts a list of integers to a string and writes to file
    specified by the second argument.
    """
    with open(fname, 'wb') as file_handle:
        file_handle.write(''.join(map(chr, integer_list)))

def gzip_write(integer_list, fname):
    "simple write, but writes a gzip-compressed file"
    with gzip.open(fname, 'wb') as file_handle:
        file_handle.write(''.join(map(chr, integer_list)))

def findfirstsublist(any_list, sublist):
    "Returns the index of the first sublist in a list"
    for index, item in enumerate(any_list):
        if list1[index:index+(len(sublist))] == sublist:
            return index

def findallsublists(any_list, sublist):
    """returns a list of all starting offsets for the given sublist.
    This can be used to find simple byte patters in a binary file."""
    results=[]
    for index, item in enumerate(any_list):
        if list1[index:index+(len(sublist))] == sublist:
            results.append(index)
    return results

def snes9x_offset(integer_list, adjust=0):
    """Snes9x save states include the full path to the
    related rom in the file header.  This is a huge pain if you're trying to
    modify binary files using offsets, as it means the offsets will change
    depending on the length of the ROM's filename even if the ROM itself
    is the same."""
    #specifically, this searches for a string that appears to be in every
    # snes9x save state and then 
    MAGIC=[67, 80, 85, 58, 48, 48, 48] #'CPU:000'
    return firstsublist(integer_list, MAGIC) + adjust #I use 0xff60 for compatibility with zsnes

class BinaryList(list):
    """Extends the basic python list object with methods
    for editing binary files.  This isn't necessary for basic editing,
    but I find it very convenient.  This object
    1.  Wraps the basic loading and writing functions.
    2.  Keeps a copy of the original, unmodified state.
    3.  Keeps a track of modified bytes for easy verification before writes are performed"""
    def __init__(self, fname, output_fname=None, is_gzip=False, verbose=nullfunc, debug=nullfunc, keep_original_state=True):
        self.is_gzip=is_gzip
        self.verbose=verbose
        self.debug=debug
        debug("loading %s ..." % fname)
        if is_gzip:
            self += gzip_load(fname)
        else:
            self += simple_load(fname)
        debug(" done.\n")
        # Set default output file to be the same as input file.
        if output_fname is None:
            self.output_fname=fname
        else:
            self.output_fname=output_fname
        if keep_original_state:
            self.original_state=copy.deepcopy(list(self))
        self.modification_list=[]
    def write(self, output_fname=None):
        if output_fname is None:
            output_fname=self.output_fname
        if self.is_gzip:
            gzip_write(list(self), output_fname)
        else:
            simple_write(list(self), output_fname)
            self.verbose('Wrote %s\n' % output_fname)
    def addmod(self, offset, value):
        "Adds a modification to the list and updates the list value"
        self.modification_list.append((offset, value))
        self[offset]=value
    def addmods(self, *modlist):
        "Adds a list of modifications"
        self.modification_list += modlist
        for offset, value in modlist:
            self[offset]=value
    def showmods(self):
        for offset, value in self.modification_list:
            sys.stdout.write("0x%x 0x%x (%d) -> 0x%x (%s)\n" % (offset,
                                                  self.original_state[offset],
                                                  self.original_state[offset],
                                                  value,
                                                  self[offset]))
    def swrite(self):
        if self.verbose is not nullfunc:
            self.showmods()
        self.verbose("writing to file: %s\n" % self.output_fname)
        self.write(self.output_fname)

    def find(self, sequence):
        return findallsublists(self, sequence)

def firstbyte(lst):
    for byt in lst:
        if byt != 0:
            break
    return lst.index(byt)

def trunczeroes(bytes):
    return bytes[firstbyte(bytes):]

## These functions are used for turning
## positive integers into little endian
## byte sequences.

# The first function converts any number to an
# 8-bit integer list
# without needing to know the type in advance.
# This is bad for numbers with a fixed type,
# such as the number "25" stored as a 16-bit integer.
# The second function, "number2bytes," is the one
# you should be using.

def val2bytes(val, result=[], power=8, base=256):
    """Recursively converts a number
    into a maximum of 'power' bytes (256 base).
    """
    if power==8:
        result=[]
    if power==0:
        result.append(int(val))
        trim_result=trunczeroes(result)
        trim_result.reverse()
        return trim_result
    result.append(int(val/(base**power)))
    return val2bytes(val % (base**power), result, power-1)

def num2bytes(number, number_of_bytes):
    """Accepts a number and returns a list of bytes
    of the specified length in little endian format."""
    num = number
    if num > 0:
        bytes=val2bytes(num)
    else:
        bytes = [0]
    if isinstance(number_of_bytes, int):
        if len(bytes)>number_of_bytes:
            print "%s %s %s" % (bytes, number_of_bytes, num)
            raise ValueError
        else:
            return bytes + [0] * (number_of_bytes-len(bytes))
    else:
        return bytes

def int2bytes(number):
    return number2bytes(number, 2)

def bytes2int(bytelist):
    """the reverse of the previous functions. (little endian)
    >>> bytes2int([0xff, 10])
    2815"""
    _intermediate=zip(bytelist, range(len(bytelist)))
    return sum([t[0]*256**t[1] for t in _intermediate])

def toint(astr):
    """converts a decimal or hexidecimal string to integer,
    unless it's aready an integer in which case it just returns
    the value.  I use this mainly to enable hex notation in
    command line arguments."""
    if isinstance(astr, int):
        return astr
    elif astr.startswith('0x'):
        return int(astr, 16)
    else:
        return int(astr)

#Functions for extracting or writing to specific bits in a byte.
def mergemaskedvalue(existing_byte, byte_to_merge, bitinfo):
    #index_in_record is ignored for this function
    index_in_record, bitmask, bitshift = bitinfo
    return (existing_byte & ~ bitmask) | (byte_to_merge << bitshift)

def getmaskedvalue(intvalue, bitinfo):
    #index_in_record is ignored for this function
    index_in_record, bitmask, bitshift = bitinfo
    return (intvalue & bitmask) >> bitshift

mergebitvalue=mergemaskedvalue
getbitvalue=getmaskedvalue
