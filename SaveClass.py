from PointClass import Point
import json

class Save:

    name = ""
    points = {}

    def fromDict(self, dict):
        self.name = dict['name']
        for i in dict['points']:
            point = Point().fromDict(i)
            self.points[point.time] = point
        return self

    def toDict(self):
        return {'name': self.name, 'points': list(map(Point.toDict, self.points.values()))}

    def addPoint(self, time, x=0, y=0, z=0):
        point = Point()
        point.time = time
        point.x = x
        point.y = y
        point.z = z
        self.points[point.time] = point

