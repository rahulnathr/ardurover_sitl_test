#!/usr/bin/env python
from rover_rc import View
from rover_model import Model
from rover_model import LocationMavros
from rover_model import PID
import Tkinter as tk
import rospy 
import numpy as np 
class Controller(object):
    def __init__(self):
        self.view = View(self)
        self.model = Model()
        self.location = LocationMavros(self)
        self.PID_CONTROL = PID(5.5,0.2,0.2)
        self.PID_CONTROL.setPoint = 50.0
        self.x1 = 0
        self.y1 = 0
        self.view.P_scale.set(0.1)
        self.wp_count = 0
        # self.array = np.arange(15).reshape(3,5)
        # print(self.array)
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
        self.wp_count = self.wp_count + 1
        self.conversion_to_integers_one()
        self.update_mission_one()
        coords = [self.model.missionx1,self.model.missiony1,
                  self.model.missionx1+5,self.model.missiony1+5]
        tag = str(self.wp_count)
        self.view.canvas_plot.create_rectangle(coords,fill ='red',tags =tag)
        self.view.canvas_plot.create_text(self.model.missionx1,self.model.missiony1,text=tag)
    def update_mission_one(self):
        points = np.array([self.model.x,self.model.y,0,1])
        # print(points)
        points_to_canvas = self.model.mapping_array.dot(points)
        print(points_to_canvas)
        print("The x ",points_to_canvas.item(0))
        # self.model.missionx1 = self.model.originx+self.model.x
        # self.model.missiony1 = self.model.originy+self.model.y
        self.model.missionx1 = points_to_canvas.item(0)
        self.model.missiony1 = points_to_canvas.item(1)

    def conversion_to_integers_two(self):
        self.x1 = float(self.view.entry2x.get())
        self.y1 = float(self.view.entry2y.get())
        self.model.x = self.x1
        self.model.y = self.y1

    def update_mission_two(self):
        self.model.missionx2 = self.model.originx + self.model.x
        self.model.missiony2 = self.model.originy + self.model.y

    def delete_waypoints(self):
        wayp = int(self.view.delentry.get())
        wayp2 = wayp+1
        # wayp = self.view.delentry.get()
        # wayp2 = str(int(wayp)+1)

        # self.view.canvas_plot.delete(str(wayp))
        # self.view.canvas_plot.delete(str(wayp2))
        self.view.canvas_plot.delete(tk.ALL)
        # self.view.canvas_plot.delete(str(wayp2))
        
    def plotter_function(self,x,y):


        points = np.array([x,y,0,1])
        # print(points)
        points_to_canvas = self.model.mapping_array.dot(points)
        # print(points_to_canvas)
        # print("The x ",points_to_canvas.item(0))
        # self.model.missionx1 = self.model.originx+self.model.x
        # self.model.missiony1 = self.model.originy+self.model.y
        # self.model.missionx1 = points_to_canvas.item(0)
        # self.model.missiony1 = points_to_canvas.item(0)
        
        
        new_x =points_to_canvas.item(0)
        new_y = points_to_canvas.item(1)
        coords = [new_x,new_y,new_x+5,new_y+5]
        self.view.canvas_plot.create_rectangle(coords,fill='red')

    def change_P_value(self,v):
        value_slider = self.view.P_scale.get()
        self.PID_CONTROL.Kp = value_slider
        rospy.loginfo("The P value is %f",self.PID_CONTROL.Kp)
        
    def change_I_value(self,v):
        value_slider = self.view.I_scale.get()
        
        self.PID_CONTROL.Ki = value_slider
        rospy.loginfo("The I value is %f",self.PID_CONTROL.Ki)

    def change_D_value(self,v):
        value_slider = self.view.D_scale.get()
        self.PID_CONTROL.Kd = value_slider
        rospy.loginfo("The D value is %f",self.PID_CONTROL.Kd)

    def change_setPoint(self,v):
        value_slider = self.view.compass_scale.get()
        self.PID_CONTROL.setPoint = value_slider
        rospy.loginfo("The setpoint is %f",self.PID_CONTROL.setPoint)

if __name__ == "__main__":
    rospy.init_node("location_node")
    app = Controller()
    
    app.view.mainloop()