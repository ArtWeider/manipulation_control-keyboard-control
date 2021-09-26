
class Point:

    x = 0
    y = 0
    z = 0

    time = 0

    def toDict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z, 'time': self.time}

    def fromDict(self, dict):
        self.x = dict['x']
        self.y = dict['y']
        self.z = dict['z']
        self.time = dict['time']
        return self
