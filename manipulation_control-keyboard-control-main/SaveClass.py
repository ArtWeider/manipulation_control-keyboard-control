from PointClass import Point
import json
import tkinter as tk

class Save:

    def __init__(self):
        self.name = ""
        self.points = None

    def fromDict(self, dict):
        self.name = dict['name']
        self.points = {}
        for i in dict['points']:
            point = Point()
            point.fromDict(i)
            self.points[point.time] = point


    def toDict(self):
        return {'name': self.name, 'points': list(map(Point.toDict, self.points.values()))}

    def addPoint(self, time, x=0, y=0, z=0):
        point = Point()
        point.time = time
        point.x = x
        point.y = y
        point.z = z
        self.points[point.time] = point

