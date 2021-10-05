
class Point:

    x = 0
    y = 0
    z = 0
    q = 0
    e = 0
    f = 0

    time = 0

    def toDict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z, 'q': self.q, 'e': self.e, 'f': self.f, 'time': self.time}

    def fromDict(self, dict):
        self.x = dict['x']
        self.y = dict['y']
        self.z = dict['z']
        self.q = dict['q']
        self.e = dict['e']
        self.f = dict['f']
        self.time = dict['time']
        return self
