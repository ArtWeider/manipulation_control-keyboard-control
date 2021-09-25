import json

from SaveClass import Save
from PointClass import Point
import os
import os.path
import random
import numpy.random as rand

class SavesManager:

    saves = {}
    currentSave = ''

    def __init__(self):
        self.loadSaves()

    def loadSaves(self):
        for filename in os.listdir("Saves"):
            if filename[-5::] == ".save":
                fileCont = open(f"Saves/{filename}", 'r')
                decodedCont = json.load(fileCont)
                save = Save().fromDict(decodedCont)
                self.saves[save.name] = save

    def saveAll(self):
        for i in self.saves.values():
            self.save(i)

    def save(self, save):
        file = open(f'Saves/{save.name}.save', 'w')
        file.write(json.dumps(save.toDict()))


if __name__ == "__main__":
    _random = rand.randint(0, 500, 1000)
    for i in range(3):
        with open(f"Saves/Save {i}.save", 'w') as f:
            random.seed(i)
            save = Save()
            save.name = f"Save {i}.save"
            for i2 in range(_random[i*6] % 30):
                i2 += 1
                point = Point()
                point.time = _random[i2*14] % 60
                point.x = _random[i2*1]
                point.y = _random[i2*2]
                point.z = _random[i2*5]
                save.points[point.time] = point
            f.write(json.dumps(save.toDict()))

