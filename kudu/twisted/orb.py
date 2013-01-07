#!/usr/bin/env python

from twisted.internet.threads import deferToThread

from kudu.exc import OrbIncomplete
import kudu.orb


class Orb(kudu.orb.Orb):
    """Twisted compatible Orb class.

    Usage is basically the same as the kudu.orb.Orb class, except the methods
    overridden here return deferreds.

    Only the slowest and most frequently called methods are overridden here.

    Users maybe want to use the twisted maybeDeferred to avoid having to
    remember which methods return deferreds.
    """

# NOTE: Async connect breaks Antelope such that it sends us corrupted packets.
#    def connect(self):
#        """Returns a deferred connect."""
#        d = deferToThread(
#                super(Orb, self).connect)
#        return d

    def _reap_eb(self,failure):
        """Orbreap errback method."""
        failure.trap(OrbIncomplete)
        return self.reap()

    def reap(self):
        """Returns a deferred Orb.reap.

        The OrbIncomplete exception is trapped and the reap is automatically
        restarted."""
        d = deferToThread(
                super(Orb, self).reap)
        d.addErrback(self._reap_eb)
        return d

    def reap_timeout(self, maxseconds):
        """Returns a deferred Orb.reap_timeout.

        The OrbIncomplete exception is NOT trapped, so the errback will be
        called if the reap times out, or if any other error occurs."""
        d = deferToThread(
                super(Orb, self).reap_timeout,
                maxseconds)
        return d

    def get(self, whichpkt):
        """Returns a deferred Orb.get."""
        d = deferToThread(
                super(Orb, self).get,
                whichpkt)
        return d

