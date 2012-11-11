#!/usr/bin/env python
"""Antelope C api wRAPper."""

from pprint import pprint

from ctypes import CDLL, create_string_buffer, string_at
from ctypes import c_bool, c_char, c_wchar, c_byte, c_ubyte, c_short, c_ushort
from ctypes import c_int, c_uint, c_long, c_ulong, c_longlong, c_ulonglong
from ctypes import c_float, c_double, c_longdouble, c_char_p, c_wchar_p
from ctypes import c_void_p, POINTER, pointer, byref

__all__ = ['orbreap_timeout']

ORBSRCNAME_SIZE = 64

libc = CDLL('libc.so.6')

liborb = CDLL("liborb.so.3")

# orbreap_timeout
liborb.orbreap_timeout.argtypes = [c_int, c_double, POINTER(c_int),
            c_char_p, POINTER(c_double), POINTER(POINTER(c_char)),
            POINTER(c_int), POINTER(c_int)]
liborb.orbreap_timeout.restype = c_int

# orbreap
liborb.orbreap.argtypes = [c_int, POINTER(c_int),
            c_char_p, POINTER(c_double), POINTER(POINTER(c_char)),
            POINTER(c_int), POINTER(c_int)]
liborb.orbreap.restype = c_int

# orbget
liborb.orbget.argtypes = [c_int, c_int, POINTER(c_int), 
            c_char_p, POINTER(c_double), POINTER(POINTER(c_char)), 
            POINTER(c_int), POINTER(c_int)]
liborb.orbget.restype = c_int

def orbreap_timeout(orbfd, maxseconds=0.0):
    """r, pktid, srcname, time, packet, nbytes = orb.orbreap_timeout(orbfd,
    maxseconds)

    Unlike the stock Antelope python bindings, this releases the GIL, and
    returns the result code.
    """
    pktid = c_int()
    pkttime = c_double()
    srcname = create_string_buffer(ORBSRCNAME_SIZE)
    packet = POINTER(c_char)()
    nbytes = c_int()
    bufsize = c_int(0)
    print "Calling into c orbreap_timeout"
    r = liborb.orbreap_timeout(orbfd, maxseconds, byref(pktid), srcname, byref(pkttime),
                byref(packet), byref(nbytes), byref(bufsize))
    if r < 0:
        pktid, srcname, pkttime, packetstr, nbytes = None, None, None, None, None
    else:
        pktid = pktid.value
        srcname = string_at(srcname)
        pkttime = pkttime.value
        packetstr = string_at(packet, nbytes)
        nbytes = nbytes.value
        libc.free(packet)
    return r, pktid, srcname, pkttime, packetstr, nbytes


def orbreap(orbfd):
    """r, pktid, srcname, time, packet, nbytes = orb.orbreap_(orbfd)

    Unlike the stock Antelope python bindings, this releases the GIL, and
    returns the result code.
    """
    pktid = c_int()
    pkttime = c_double()
    srcname = create_string_buffer(ORBSRCNAME_SIZE)
    packet = POINTER(c_char)()
    nbytes = c_int()
    bufsize = c_int(0)
    r = liborb.orbreap(orbfd, byref(pktid), srcname, byref(pkttime),
                byref(packet), byref(nbytes), byref(bufsize))
    # The stock bindings swallow r; we could return it...
    if r < 0:
        pktid, srcname, pkttime, packetstr, nbytes = None, None, None, None, None
    else:
        pktid = pktid.value
        srcname = string_at(srcname)
        pkttime = pkttime.value
        packetstr = string_at(packet, nbytes)
        nbytes = nbytes.value
        libc.free(packet)
    return r, pktid, srcname, pkttime, packetstr, nbytes


def orbget(orbfd, whichpkt):
    """r, pktid, srcname, time, packet, nbytes = orb.orbget(orbfd, whichpkt)

    Unlike the stock Antelope python bindings, this releases the GIL, and
    returns the result code.
    """
    pktid = c_int()
    pkttime = c_double()
    srcname = create_string_buffer(ORBSRCNAME_SIZE)
    packet = POINTER(c_char)()
    nbytes = c_int()
    bufsize = c_int(0)
    r = liborb.orbget(orbfd, whichpkt, byref(pktid), srcname, byref(pkttime),
                byref(packet), byref(nbytes), byref(bufsize))
    if r < 0:
        pktid, srcname, pkttime, packetstr, nbytes = None, None, None, None, None
    else:
        pktid = pktid.value
        srcname = string_at(srcname)
        pkttime = pkttime.value
        packetstr = string_at(packet, nbytes)
        nbytes = nbytes.value
        libc.free(packet)
    return r, pktid, srcname, pkttime, packetstr, nbytes

