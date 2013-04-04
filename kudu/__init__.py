#!/usr/bin/env python
import sys
import os

sys.path.append(os.environ['ANTELOPE'] + '/data/python')

from antelope import stock


# Monkeypatch auto_convert to work around it interpreting dotted quads as time
# strings.
old_auto_convert = stock.auto_convert

def auto_convert(val):
    try:
        if val.count('.') > 1:
            return val
    except AttributeError:
        pass
    return old_auto_convert(val)

stock.auto_convert = auto_convert

