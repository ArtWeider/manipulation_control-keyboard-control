from tkinter import *
from tkinter import ttk
from config import Cfg as cfg
from PIL import Image, ImageTk
from SaveClass import Save


class SavesMenuWidget:

    main  = None

    mainFrame = None
    createButton = None
    nameEntry = None
    nameEntryVar = None

    X = 5 * cfg.SIZE_MULT
    Y = 400 * cfg.SIZE_MULT
    WIDTH = 200 * cfg.SIZE_MULT
    HEIGHT = 195 * cfg.SIZE_MULT

    def __init__(self, main):

        self.main = main

        self.mainFrame = ttk.Frame(style="RoundedFrame", height=self.HEIGHT, width=self.WIDTH)
        self.mainFrame.place(x=self.X, y=self.Y)

        self.nameEntryVar = StringVar()
        self.nameEntry = Entry(master=self.mainFrame,
                               width=19,
                               bg=cfg.MAIN_COLOR,
                               bd=0,
                               fg=cfg.TEXT_COLOR,
                               justify=CENTER,
                               textvariable=self.nameEntryVar,
                               validate='focusout',
                               validatecommand=self.onTextEdited
                               )
        self.nameEntry.place(x=13, y=10)

        self.createButton = Button(master=self.mainFrame,
                                   text="Создать",
                                   bg=cfg.BUTTON_COLOR,
                                   bd=0,
                                   fg=cfg.TEXT_COLOR,
                                   width=16,
                                   activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                   activeforeground=cfg.TEXT_COLOR,
                                   command=self.onCreatePressed
                                   )
        self.createButton.place(x=12, y=35)

        self.deleteButton = Button(master=self.mainFrame,
                                   text="Удалить",
                                   bg=cfg.BUTTON_COLOR,
                                   bd=0,
                                   fg=cfg.TEXT_COLOR,
                                   width=16,
                                   activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                   activeforeground=cfg.TEXT_COLOR,
                                   state=DISABLED,
                                   command=self.onDeletePressed
                                   )
        self.deleteButton.place(x=12, y=65)

        self.saveButton = Button(master=self.mainFrame,
                                 text="Сохранить",
                                 bg=cfg.BUTTON_COLOR,
                                 bd=0,
                                 fg=cfg.TEXT_COLOR,
                                 width=16,
                                 activebackground=cfg.BUTTON_ACTIVE_COLOR,
                                 activeforeground=cfg.TEXT_COLOR,
                                 state=DISABLED,
                                 command=self.onSavePressed
                                   )
        self.saveButton.place(x=12, y=95)

    def onSaveSelected(self):
        save = self.main.savesManager.saves[self.main.savesManager.currentSave]
        self.deleteButton.configure(state=NORMAL)
        self.saveButton.configure(state=NORMAL)
        self.nameEntry.delete(0, END)
        self.nameEntry.insert(0, save.name)

    def onSavePressed(self):
        self.main.savesManager.saves[self.main.savesManager.currentSave].name = self.nameEntry.get()
        self.main.savesManager.save(self.main.savesManager.saves[self.main.savesManager.currentSave])

    def onDeletePressed(self):
        self.main.savesManager.delete(self.main.savesManager.saves[self.main.savesManager.currentSave])

    def onCreatePressed(self):
        save = Save()
        save.fromDict({'name': self.nameEntry.get(), 'points': [{'x': 1, 'y': 1, 'z': 1, 'time': 1}]})
        self.main.savesManager.saves[self.nameEntry.get()] = save
        self.main.savesManager.currentSave = self.nameEntry.get()
        self.main.savesWidget.fillFromDict(self.main.savesManager.saves)

    def onTextEdited(self, name='', index='', mode=''):
        pass







