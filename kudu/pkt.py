#!/usr/bin/env python

from antelope import _Pkt as _pkt
from antelope import _stock

from kudu.exc import check_error, AntelopeError

class PktError(AntelopeError): pass
class UnstuffError(PktError): pass


class Pkt(object):
    db = None
    dfile = None
    nchannels = None
    channels = None
    pfdict = None
    string = None
    time = None
    type = None
    version = None
    pkt_raw = None

    _pkttypefields = [ 'content',
                       'name',
                       'suffix',
                       'hdrcode',
                       'bodycode',
                       'desc' ]

    _srcnamefields = [ 'net',
                       'sta',
                       'chan',
                       'loc',
                       'suffix',
                       'subcode' ]

    def __init__(self, srcname=None, time=None, raw_packet=None):
        self.srcnameparts = dict([(k, None) for k in self._srcnamefields])
        self.pkttype = dict([(k, None) for k in self._pkttypefields])
        self.channels = []
        if srcname and time and raw_packet:
            self.unstuff(srcname, time, raw_packet)

    def unstuff(self, srcname, time, raw_packet):
        pkt = None
        try:
            type, pkt = _pkt._unstuffPkt(srcname, time, raw_packet)
            check_error(type, UnstuffError)
            self.string = _pkt._Pkt_string_get(pkt)
            self.pkttype.update(dict(zip(self._pkttypefields,
                _pkt._Pkt_pkttype_get(pkt))))
            if _pkt._Pkt_type_get(pkt) == _pkt.Pkt_pf:
                pfptr = _pkt._Pkt_pfptr_get(pkt)
                if pfptr != None:
                    try:
                        self.pfdict = _stock._pfget(pfptr, None)
                    finally:
                        _stock._pffree(pfptr)
            # do we need to free the PF?
            # will the pfptr at this layer even support a dict interface?
            self.time = time
        finally:
            if pkt is not None:
                _pkt._freePkt(pkt)

#    @classmethod
#    def from_raw(pkt_raw):
#        # am I supposed to unstuff this and set all my fields?
#        self.pkt_raw = pkt_raw
#
#    def stuff(self):
#        # create Packet struct HERE and ALWAYS free it
#        # how does this report failure? I guess the only conceivable failure
#        # mode is OOM.
#        raise Exception("Not implemented")
#        pkt = None
#        try:
#            pkt = _pkt.newPkt()
#            # set pkt fields using raw api
#            # stuff packet
#            return type, packet, srcname, time
#        finally:
#            if pkt is not None:
#                _pkt._freePkt(pkt)
#
#
