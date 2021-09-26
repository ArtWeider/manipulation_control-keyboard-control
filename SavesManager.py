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
                save = Save()
                save.fromDict(decodedCont)
                self.saves[save.name] = save

    def saveAll(self):
        for i in self.saves.values():
            self.save(i)

    def save(self, save):
        file = open(f'Saves/{save.name}.save', 'w')
        file.write(json.dumps(save.toDict()))


if __name__ == "__main__":
    savesManager = SavesManager()
    for i in savesManager.saves.values():
        print(i.points)




