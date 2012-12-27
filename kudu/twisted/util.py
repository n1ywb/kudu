#!/usr/bin/env python

from collections import defaultdict

from twisted.internet.defer import Deferred

class ObservableDict(dict):
    """Like a dict, but can return deferreds which fire when a key's value
    changes."""

    def __init__(self, *args, **kwargs):
        self._listeners = defaultdict(lambda: [])
        super(ObservableDict, self).__init__(*args, **kwargs)

    def deferred_getitem(self, key, immediate=False):
        """Like dict[], but returns a deferred.

	Setting 'immediate=True' causes the callback to fire immediately. This
	could result in a KeyError.

        Setting 'immediate=False' (the default) causes the callback to fire
        when the value stored at the key changes. If the key is not in the
        dict, the deferred will not fire until the key is added to the dict,
        hence KeyError cannot be raised.
        """
        d = Deferred()
        # add d to list for that key
        self._add_listener(key, d)
        d.addCallback(lambda r: self[key])
        if immediate:
            d.callback()
        return d

    def deferred_get(self, key, default=None, immediate=False):
        """Like dict.get() but returns a deferred.

	Setting 'immediate=True' causes the callback to fire immediately; the
        default value will be returned if the key is not in the dict.

        Setting 'immediate=False' (the default) causes the callback to fire
        when the value stored at the key changes. If the key is not in the
        dict, the deferred will not fire until the key is added to the dict,
        hence the default value will never be returned.
        """
        d = Deferred()
        # add d to list for that key
        self._add_listener(key, d)
        d.addCallback(lambda r: super(ObservableDict, self).get(key, default))
        if immediate:
            d.callback()
        return d

    def _add_listener(self, key, d):
        """Adds listener d to the list of listeners for key."""
        self._listeners[key].append(d)

    def __setitem__(self, key, val):
        """Like dict.__setitem__ but also notifies listeners of the change."""
        super(ObservableDict, self).__setitem__(key, val)
        # notify listeners and reset list for k
        listeners = self._listeners[k]
        del self._listeners[k]
        for listener in listeners:
            listener.callback(val)

