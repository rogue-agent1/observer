#!/usr/bin/env python3
"""observer: Observer/pub-sub pattern implementation."""
import sys
from collections import defaultdict

class EventBus:
    def __init__(self):
        self._subs = defaultdict(list)
        self._history = []

    def on(self, event, callback):
        self._subs[event].append(callback)
        return lambda: self._subs[event].remove(callback)

    def once(self, event, callback):
        def wrapper(*args, **kwargs):
            callback(*args, **kwargs)
            self._subs[event].remove(wrapper)
        self._subs[event].append(wrapper)

    def emit(self, event, *args, **kwargs):
        self._history.append((event, args, kwargs))
        for cb in list(self._subs[event]):
            cb(*args, **kwargs)
        for cb in list(self._subs["*"]):
            cb(event, *args, **kwargs)

    def off(self, event=None):
        if event: self._subs[event].clear()
        else: self._subs.clear()

class Observable:
    def __init__(self, value):
        self._value = value; self._watchers = []
    @property
    def value(self): return self._value
    @value.setter
    def value(self, new):
        old = self._value; self._value = new
        for w in self._watchers: w(new, old)
    def watch(self, fn): self._watchers.append(fn)

def test():
    bus = EventBus()
    log = []
    bus.on("click", lambda x: log.append(("click", x)))
    bus.emit("click", 1)
    bus.emit("click", 2)
    assert log == [("click",1),("click",2)]
    # Once
    bus.once("ping", lambda: log.append("pong"))
    bus.emit("ping"); bus.emit("ping")
    assert log.count("pong") == 1
    # Wildcard
    all_events = []
    bus.on("*", lambda evt, *a: all_events.append(evt))
    bus.emit("test")
    assert "test" in all_events
    # Unsubscribe
    unsub = bus.on("x", lambda: None)
    assert len(bus._subs["x"]) == 1
    unsub()
    assert len(bus._subs["x"]) == 0
    # Observable
    obs = Observable(10)
    changes = []
    obs.watch(lambda new, old: changes.append((old, new)))
    obs.value = 20
    obs.value = 30
    assert changes == [(10,20),(20,30)]
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: observer.py test")
