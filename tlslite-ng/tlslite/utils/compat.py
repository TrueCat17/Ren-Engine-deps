# Author: Trevor Perrin
# See the LICENSE file for legal information regarding use of this file.

"""Miscellaneous functions to mask Python version differences."""

import sys
import re
import os
import platform
import math
import binascii
import traceback
import time
import ecdsa

def compat26Str(x): return x

# Python 3.3 requires bytes instead of bytearrays for HMAC
# So, python 2.6 requires strings, python 3 requires 'bytes',
# and python 2.7 and 3.5 can handle bytearrays...
# pylint: disable=invalid-name
# we need to keep compatHMAC and `x` for API compatibility
def compatHMAC(x):
    """Convert bytes-like input to format acceptable for HMAC."""
    return x
# pylint: enable=invalid-name

def compatAscii2Bytes(val):
    """Convert ASCII string to bytes."""
    if isinstance(val, str):
        return bytes(val, 'ascii')
    return val

def compat_b2a(val):
    """Convert an ASCII bytes string to string."""
    return str(val, 'ascii')

def raw_input(s):
    return input(s)

# So, the python3 binascii module deals with bytearrays, and python2
# deals with strings...  I would rather deal with the "a" part as
# strings, and the "b" part as bytearrays, regardless of python version,
# so...
def a2b_hex(s):
    try:
        b = bytearray(binascii.a2b_hex(bytearray(s, "ascii")))
    except Exception as e:
        raise SyntaxError("base16 error: %s" % e) 
    return b  

def a2b_base64(s):
    try:
        if isinstance(s, str):
            s = bytearray(s, "ascii")
        b = bytearray(binascii.a2b_base64(s))
    except Exception as e:
        raise SyntaxError("base64 error: %s" % e)
    return b

def b2a_hex(b):
    return binascii.b2a_hex(b).decode("ascii")    
        
def b2a_base64(b):
    return binascii.b2a_base64(b).decode("ascii") 

def readStdinBinary():
    return sys.stdin.buffer.read()        

def compatLong(num):
    return int(num)

int_types = tuple([int])

def formatExceptionTrace(e):
    """Return exception information formatted as string"""
    return str(e)

def time_stamp():
    """Returns system time as a float"""
    return time.perf_counter()

def remove_whitespace(text):
    """Removes all whitespace from passed in string"""
    return re.sub(r"\s+", "", text, flags=re.UNICODE)

# pylint: disable=invalid-name
# pylint is stupid here and deson't notice it's a function, not
# constant
bytes_to_int = int.from_bytes
# pylint: enable=invalid-name

def bit_length(val):
    """Return number of bits necessary to represent an integer."""
    return val.bit_length()

def int_to_bytes(val, length=None, byteorder="big"):
    """Return number converted to bytes"""
    if length is None:
        length = byte_length(val)
    # for gmpy we need to convert back to native int
    if type(val) != int:
        val = int(val)
    return bytearray(val.to_bytes(length=length, byteorder=byteorder))


def byte_length(val):
    """Return number of bytes necessary to represent an integer."""
    length = bit_length(val)
    return (length + 7) // 8


try:
    # Fedora and Red Hat Enterprise Linux versions have small curves removed
    getattr(ecdsa, 'NIST192p')
except AttributeError:
    ecdsaAllCurves = False
else:
    ecdsaAllCurves = True
