import json

from SaveClass import Save
import os
import os.path

class SavesManager:

    saves = {}
    currentSave = None

    def __init__(self, main):
        self.main = main
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

    def delete(self, save):
        os.remove(f"Saves/{save.name}.save")
        del self.saves[self.currentSave]
        self.currentSave = None
        self.main.savesWidget.fillFromDict(self.saves)
