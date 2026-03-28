#!/usr/bin/env python3
"""observer - Observer/pub-sub design pattern."""
import sys
from collections import defaultdict
class Subject:
    def __init__(s):s._observers=defaultdict(list)
    def subscribe(s,topic,observer):s._observers[topic].append(observer)
    def unsubscribe(s,topic,observer):s._observers[topic].remove(observer)
    def notify(s,topic,data=None):
        for obs in s._observers[topic]:obs.update(topic,data)
class Observer:
    def __init__(s,name):s.name=name;s.messages=[]
    def update(s,topic,data):s.messages.append((topic,data));print(f"  [{s.name}] {topic}: {data}")
if __name__=="__main__":
    pub=Subject();alice=Observer("Alice");bob=Observer("Bob")
    pub.subscribe("news",alice);pub.subscribe("news",bob);pub.subscribe("sports",bob)
    pub.notify("news","Breaking: AI builds 600 tools in a day")
    pub.notify("sports","Giants win 5-3")
    print(f"\n  Alice got {len(alice.messages)} messages, Bob got {len(bob.messages)}")
