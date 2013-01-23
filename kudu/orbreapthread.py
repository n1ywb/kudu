#!/usr/bin/env python

import antelope._brttpkt as _brttpkt

class OrbReapThreadError(Exception): pass
class SetToStopError(OrbReapThreadError): pass
class IsStopped(OrbReapThreadError): pass
class GetError(OrbReapThreadError): pass
class DestroyError(OrbReapThreadError): pass

class OrbReapThread(object):
    def __init__(self, orbname, select=None, reject=None,
	            tafter=-1, timeout=-1, queuesize=64):
        self.orbname = orbname
        self._thread = _brttpkt._orbreapthr_new2(orbname, select, reject,
                                                tafter, timeout, queuesize)
        if not self._thread:
            raise OrbReapThreadError()

    def set_to_stop(self):
        rc = _brttpkt._orbreapthr_set_to_stop(self._thread)
        if rc < 0:
            raise SetToStopError()

    def is_stopped(self):
        rc = _brttpkt._orbreapthr_is_stopped(self._thread)
        if rc < 0:
            raise IsStoppedError()
        return bool(rc)

    def get(self):
        rc, pktid, srcname, pkttime, pkt, nbytes = _brttpkt._orbreapthr_get(
                                                                self._thread)
        if rc < 0:
            raise GetError()
        return rc, pktid, srcname, pkttime, pkt, nbytes

    def destroy(self):
        rc = _brttpkt._orbreapthr_destroy(self._thread)
        if rc < 0:
            raise DestroyError()

