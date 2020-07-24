#!/usr/bin/env python
from rover_rc import View
from rover_model import Model
from rover_model import LocationMavros
import Tkinter as tk
import rospy 

class Controller(object):
    def __init__(self):
        self.view = View(self)
        self.model = Model()
        self.location = LocationMavros(self)
        self.x1 = 0
        self.y1 = 0

    def sent_coordinates_two(self):
        self.conversion_to_integers_two()
        self.update_mission_two()
        coords = [self.model.missionx2,self.model.missiony2,
                  self.model.missionx2+5,self.model.missiony2+5]
        self.view.canvas_plot.create_rectangle(coords,fill ='red')

    def conversion_to_integers_one(self):
        self.x1 = float(self.view.entry1x.get())
        self.y1 = float(self.view.entry1y.get())
        self.model.x = self.x1
        self.model.y = self.y1
    
    def sent_coordinates_one(self):
        self.conversion_to_integers_one()
        self.update_mission_one()
        coords = [self.model.missionx1,self.model.missiony1,
                  self.model.missionx1+5,self.model.missiony1+5]
        self.view.canvas_plot.create_rectangle(coords,fill ='red')
    
    def update_mission_one(self):
        self.model.missionx1 = self.model.originx+self.model.x
        self.model.missiony1 = self.model.originy+self.model.y


    def conversion_to_integers_two(self):
        self.x1 = float(self.view.entry2x.get())
        self.y1 = float(self.view.entry2y.get())
        self.model.x = self.x1
        self.model.y = self.y1

    def update_mission_two(self):
        self.model.missionx2 = self.model.originx + self.model.x
        self.model.missiony2 = self.model.originy + self.model.y


    def plotter_function(self,x,y):
        new_x =self.model.originx+x
        new_y = self.model.originy+y
        coords = [new_x,new_y,new_x+5,new_y+5]
        self.view.canvas_plot.create_rectangle(coords,fill='red')

if __name__ == "__main__":
    rospy.init_node("location_node")
    app = Controller()
    
    app.view.mainloop()