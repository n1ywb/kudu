#!/usr/bin/env python

from twisted.internet.threads import deferToThread

import antelope.brttpkt

class OrbReapThread(antelope.brttpkt.OrbreapThr):
    def get(self):
        d = deferToThread(
                super(OrbReapThread, self).get)
        return d

