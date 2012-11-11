#!/usr/bin/env python

from antelope import _orb

from kudu.exc import check_error, OrbError
from kudu import _crap



class OpenError(OrbError): pass
class CloseError(OrbError): pass
class SelectError(OrbError): pass
class RejectError(OrbError): pass
class SeekError(OrbError): pass
class ReapError(OrbError): pass
class ReapTimeoutError(OrbError): pass
class GetError(OrbError): pass
class PutError(OrbError): pass
class PutXError(OrbError): pass

class Orb(object):
    _fd = None
    def __init__(self, orbname, permissions):
        _fd = _orb._orbopen(orbname, permissions)
        if _fd < 0:
            raise OpenError()
        self._fd = _fd
        self.orbname = permissions
        self.permissions = permissions

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self._fd is not None:
            r = _orb._orbclose(self._fd)
            self._fd = None
            if r < 0:
                raise CloseError()

#    def ping(self):
#        pass

#    def tell(self):
#        pass

    def select(self, match):
        return check_error(_orb._orbselect(self._fd, match), SelectError)

    def reject(self, reject):
        return check_error(_orb._orbreject(self._fd, reject), RejectError)

#    def position(self):
#        pass

    def seek(self, whichpkt):
        return check_error(_orb._orbseek(self._fd, whichpkt), SeekError)

#    def after(self):
#        pass

    def reap(self):
        # Call our internal binding, because it releases the GIL and returns
        # the result code.
        r, pktid, srcname, pkttime, packetstr, nbytes = _crap.orbreap(self._fd)
        check_error(r, ReapError)
        return pktid, srcname, pkttime, packetstr, nbytes

    def reap_timeout(self, maxseconds):
        # Call our internal binding, because it releases the GIL and returns
        # the result code.
        r, pktid, srcname, pkttime, packetstr, nbytes = _crap.orbreap_timeout(self._fd, maxseconds)
        check_error(r, ReapTimeoutError)
        return pktid, srcname, pkttime, packetstr, nbytes

    def get(self, whichpkt):
        # Call our internal binding, because it releases the GIL and returns
        # the result code.
        r, pktid, srcname, pkttime, packetstr, nbytes = _crap.get(self._fd, maxseconds)
        check_error(r, GetError)
        return pktid, srcname, pkttime, packetstr, nbytes

    def put(self, srcname, time, packet, nbytes):
        return check_error(_orb._orbput(self._fd, srcname, time, packet,
            nbytes), PutError)

    def putx(self, srcname, time, packet, nbytes):
        return check_error(_orb._orbputx(self._fd, srcname, time, packet,
            nbytes), PutXError)

#    def lag(self):
#        pass
#    def stat(self):
#        pass
#    def sources(self):
#        pass
#    def clients(self):
#        pass
#    def resurrect(self):
#        pass
#    def bury(self):
#        pass


#def exhume(filename):
#    """Return a new Orb?"""
#    pass

