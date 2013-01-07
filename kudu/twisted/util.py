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
        deferred = Deferred()
        deferred.addCallback(lambda r: self[key])
        if immediate:
            deferred.callback(None)
        else:
            self._add_listener(key, deferred)
        return deferred

    def deferred_get(self, key, default=None, immediate=False):
        """Like dict.get() but returns a deferred.

	Setting 'immediate=True' causes the callback to fire immediately; the
        default value will be returned if the key is not in the dict.

        Setting 'immediate=False' (the default) causes the callback to fire
        when the value stored at the key changes. If the key is not in the
        dict, the deferred will not fire until the key is added to the dict,
        hence the default value will never be returned.
        """
        deferred = Deferred()
        deferred.addCallback(lambda r: super(ObservableDict, self).get(key, default))
        if immediate:
            deferred.callback(None)
        else:
            self._add_listener(key, deferred)
        return deferred

    def _add_listener(self, key, deferred):
        """Adds listener d to the list of listeners for key."""
        self._listeners[key].append(deferred)

    def __setitem__(self, key, val):
        """Like dict.__setitem__ but also notifies listeners of the change."""
        super(ObservableDict, self).__setitem__(key, val)
        # notify listeners and reset list for key
        listeners = self._listeners[key]
        del self._listeners[key]
        for listener in listeners:
            listener.callback(val)

