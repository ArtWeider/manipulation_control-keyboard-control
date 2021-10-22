
def tryGetValue(key, dict, default):
    try:
        return dict[key]
    except KeyError:
        return default

class Point:

    x = 0
    y = 0
    z = 0
    rad = 0
    a = 0
    b = 0
    c = 0
    q = 0
    e = 0
    f = 0
    gMode = False

    time = 0

    def toDict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z, 'rad': self.rad, 'a': self.a, 'b': self.b, 'c': self.c, 'q': self.q, 'e': self.e, 'f': self.f, 'gMode': self.gMode, 'time': self.time}

    def fromDict(self, dict):
        self.x = tryGetValue('x', dict, 0)
        self.y = tryGetValue('y', dict, 0)
        self.z = tryGetValue('z', dict, 0)
        self.rad = tryGetValue('rad', dict, 0)
        self.a = tryGetValue('a', dict, 0)
        self.b = tryGetValue('b', dict, 0)
        self.c = tryGetValue('c', dict, 0)
        self.q = tryGetValue('q', dict, 0)
        self.e = tryGetValue('e', dict, 0)
        self.f = tryGetValue('f', dict, 90)
        self.gMode = tryGetValue('gMode', dict, False)

        self.time = tryGetValue('time', dict, 1)
        return self
