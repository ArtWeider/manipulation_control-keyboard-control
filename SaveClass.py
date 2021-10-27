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

    def addPoint(self, time, x=0, y=0, z=0, rad=0, a=0, b=0, c=0, q=0, e=0, f=90, gMode=False, **kwargs):
        if 'useLast' in kwargs.keys():
            if kwargs['useLast']:
                lastPoint = None

                keys = list(self.points.keys())
                for num, key in enumerate(keys):
                    if time > self.points[keys[-1]].time:
                        lastPoint = self.points[keys[-1]]
                    elif num > 0:
                        if float(key) > time and float(keys[num-1]) < time:
                            lastPoint = self.points[key]
                    else:
                        if float(key) > time:
                            lastPoint = self.points[key]

                if lastPoint != None:
                    x, y, z, q, e, f, gMode = lastPoint.x, lastPoint.y, lastPoint.z, lastPoint.q, lastPoint.e, lastPoint.f, lastPoint.gMode

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
        point.gMode = gMode

        self.points[point.time] = point
