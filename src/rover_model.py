import tkinter as tk

class Model:
    def __init__(self):
        self.originx = 175
        self.originy = 250
        self.x = 0
        self.y = 0
        self.missionx1 = self.originx+self.x
        self.missiony1 = self.originy+self.y
        self.missionx2 = self.originx+self.y
        self.missiony2 = self.originy+self.y
