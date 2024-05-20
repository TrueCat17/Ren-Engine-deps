"""
Common functions for providing cross-python version compatibility.
"""
import sys
import re
import binascii


def str_idx_as_int(string, index):
    """Take index'th byte from string, return as integer"""
    val = string[index]
    if isinstance(val, int):
        return val
    return ord(val)


def hmac_compat(data):
    return data

def normalise_bytes(buffer_object):
    """Cast the input into array of bytes."""
    return memoryview(buffer_object).cast("B")

def compat26_str(val):
    return val

def remove_whitespace(text):
    """Removes all whitespace from passed in string"""
    return re.sub(r"\s+", "", text, flags=re.UNICODE)

def a2b_hex(val):
    try:
        return bytearray(binascii.a2b_hex(bytearray(val, "ascii")))
    except Exception as e:
        raise ValueError("base16 error: %s" % e)

# pylint: disable=invalid-name
# pylint is stupid here and doesn't notice it's a function, not
# constant
bytes_to_int = int.from_bytes
# pylint: enable=invalid-name

def bit_length(val):
    """Return number of bits necessary to represent an integer."""
    return val.bit_length()

def int_to_bytes(val, length=None, byteorder="big"):
    """Convert integer to bytes."""
    if length is None:
        length = byte_length(val)
    # for gmpy we need to convert back to native int
    if not isinstance(val, int):
        val = int(val)
    return bytearray(val.to_bytes(length=length, byteorder=byteorder))


def byte_length(val):
    """Return number of bytes necessary to represent an integer."""
    length = bit_length(val)
    return (length + 7) // 8
