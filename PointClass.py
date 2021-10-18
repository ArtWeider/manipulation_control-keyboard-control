
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

    time = 0

    def toDict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z, 'rad': self.rad, 'a': self.a, 'b': self.b, 'c': self.c, 'q': self.q, 'e': self.e, 'f': self.f, 'time': self.time}

    def fromDict(self, dict):
        self.x = dict['x']
        self.y = dict['y']
        self.z = dict['z']
        self.rad = dict['rad']
        self.a = dict['a']
        self.b = dict['b']
        self.c = dict['c']
        self.q = dict['q']
        self.e = dict['e']
        self.f = dict['f']
        self.time = dict['time']
        return self
