from rover_rc import View
from rover_model import Model
import tkinter as tk
class Controller:
    def __init__(self):
        self.view = View(self)
        self.model = Model()
        self.x1 = 0
        self.y1 = 0

    def sent_coords2(self):
        self.conversion_to_integers()
        self.update_mission()
        coords = [self.model.missionx2,self.model.missiony2,
                  self.model.missionx2+5,self.model.missiony2+5]
        self.view.canvas_plot.create_rectangle(coords,fill ='red')

    def conversion_to_integers(self):
        self.x1 = float(self.view.entry11x.get())
        self.y1 = float(self.view.entry22y.get())
        self.model.x = self.x1
        self.model.y = self.y1

    def update_mission(self):
        self.model.missionx2 = self.model.originx + self.model.x
        self.model.missiony2 = self.model.originy + self.model.y




if __name__ == "__main__":
    app = Controller()
    app.view.mainloop()