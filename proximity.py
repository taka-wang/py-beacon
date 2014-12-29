#
# by Taka Wang
#

import sys, operator, time, threading
from collections import deque
from numpy import average
# require by Scanner class
import blescan
import bluetooth._bluetooth as bluez

class Calculator():
    def __init__(self, queueCapacity = 5, chkTimer = 3, threshold = 10):
        self.qRssi     = {}             # key:id, value:rssi queue
        self.aRssi     = {}             # key:id, value:average rssi
        self.ts        = {}             # key:id, value:expire timestamp
        self.capacity  = queueCapacity  # queue capacity for moving average
        self.threshold = threshold      # missing beacon threshold in seconds
        if chkTimer > 0:
            self.__setInterval(self.sanitize, chkTimer)

    def __setInterval(self, func, sec):
        """Thread based setInterval function - (not safe)"""
        def func_wrapper():
            self.__setInterval(func, sec)
            func()
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t

    def sanitize(self):
        """Remove expire beacons"""
        now = int(time.time())
        for id in self.ts.keys():
            if self.ts[id] < now:
                del self.aRssi[id]
                del self.qRssi[id]
                del self.ts[id]
                print("clean uid: ", str(id))

    def add(self, id, value):
        """Add new rssi for calculation."""
        if (id not in self.qRssi):
            self.qRssi[id] = deque(maxlen = self.capacity)     # size limited queue
            self.aRssi[id] = -sys.maxint - 1                   # init with -inf
            self.ts[id]    = int(time.time() + self.threshold) # init with current timestamp

        self.qRssi[id].append(value)
        self.ts[id] = int(time.time() + self.threshold)       # update expire timestamp
        if (len(self.qRssi[id]) == self.capacity):
            # weighted moving average calculation via numpy's average function
            self.aRssi[id] = average(self.qRssi[id], weights = range(1, self.capacity + 1, 1))
    
    def nearest(self):
        """Find max average rssi beacon"""
        for id, container in self.qRssi.iteritems():
            # at least one beacon satisfy this condition, calculate the max 
            if (len(container) == self.capacity):
                nearest_uid = max(self.qRssi.iteritems(), key = operator.itemgetter(1))[0]
                if (self.aRssi[nearest_uid] > -200):
                    return str(nearest_uid), round(self.aRssi[nearest_uid],1)
        return None, None

    def beacons(self):
        """List visible beacons"""
        return self.qRssi.keys()

    def test(self):
        for i in xrange(1, 10):
            self.add("id-1", i)
        for j in xrange(1, 10, 2):
            self.add("id-2", j)
        ret, val = self.nearest()
        print(ret, val)
        print(self.beacons())

class Scanner():
    def __init__(self, deviceId = 0, loops = 1):
        self.deviceId = deviceId
        self.loops = loops
        try:
            self.sock = bluez.hci_open_dev(self.deviceId)
            blescan.hci_le_set_scan_parameters(self.sock)
            blescan.hci_enable_le_scan(self.sock)
        except Exception, e:
            print e   

    def scan(self):
        return blescan.parse_events(self.sock, self.loops)

    def test(self):
        while True:
            for beacon in self.scan():
                print beacon

if __name__ == '__main__':
    c = Calculator(chkTimer = 1, threshold = 5)
    c.test()
    s = Scanner(loops = 3)
    s.test()

'''
from proximity import *
c = Calculator()
c.test()
s = Scanner(loops = 3)
s.test()    
''' 