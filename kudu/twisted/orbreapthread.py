#!/usr/bin/env python

from twisted.internet.threads import deferToThread

from kudu.exc import OrbIncomplete
import kudu.orbreapthread


class OrbReapThread(kudu.orbreapthread.OrbReapThread):
    def get(self):
        d = deferToThread(
                super(OrbReapThread, self).get)
        return d

