#!/usr/bin/env python
"""
Twisted-Friendly Orb Reap Threads
---------------------------------
"""

from twisted.internet.threads import deferToThread

import antelope.brttpkt

class OrbreapThr(antelope.brttpkt.OrbreapThr):
    """Twisted-compatible subclass of ``antelope.brttpkt.OrbreapThr``."""

    def get(self):
        """Defer ``get`` to a thread.

        :rtype: ``Deferred``
        """
        d = deferToThread(
                super(OrbreapThr, self).get)
        return d

