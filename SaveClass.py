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

    def getNearestToTime(self, time):
        time = float(time)
        t0, t1 = None, None
        times = sorted([float(i) for i in self.points.keys()])
        t = times[0]
        if time < times[0]:
            t0 = None
            t1 = times[0]
        elif time > times[-1]:
            t0 = times[-1]
            t1 = None
        else:
            for num, i in enumerate(times):
                if time > i:
                    t0 = i
                    t1 = times[num+1]
        if t0 == None and t1 != None:
            t = t1
        elif t0 != None:
            t = t0

        print(t0, t1, t)

        return t

    def toDict(self):
        return {'name': self.name, 'points': list(map(Point.toDict, self.points.values()))}

    def addPoint(self, time, x=0, y=0, z=0, rad=0, a=0, b=0, c=0, q=0, e=0, f=90, gMode=False, **kwargs):
        if 'useLast' in kwargs.keys():
            if kwargs['useLast']:
                lastPoint = self.points[self.getNearestToTime(time)]
                if lastPoint != None:
                    x, y, z, q, e, f, gMode = lastPoint.x, lastPoint.y, lastPoint.z, lastPoint.q, lastPoint.e, lastPoint.f, lastPoint.gMode

        print('create point', x, y, z, q, e, f, gMode)
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
