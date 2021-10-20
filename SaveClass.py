from PointClass import Point

def tryGetValue(key, dict, default):
    try:
        return dict[key]
    except KeyError:
        return default

class Save:

    def __init__(self):
        self.name = ""
        self.points = None

    def fromDict(self, dict):
        self.name = tryGetValue('name', dict, 'Название')
        self.points = {}
        for i in tryGetValue('points', dict, []):
            point = Point()
            point.fromDict(i)
            self.points[point.time] = point

    def toDict(self):
        return {'name': self.name, 'points': list(map(Point.toDict, self.points.values()))}

    def addPoint(self, time, x=0, y=0, z=0, rad=0, a=0, b=0, c=0, q=0, e=0, f=90, g=90):
        point = Point()
        point.time = time

        point.x = x
        point.y = y
        point.z = z

        point.rad = rad
        point.a = a
        point.b = b
        point.c = c

        point.q = q
        point.e = e
        point.f = f
        point.g = g

        self.points[point.time] = point
