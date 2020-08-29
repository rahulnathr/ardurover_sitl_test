#!/usr/bin/env python


# from dp_view import View
import rospy
from dp_view import View
from dp_model import Model
from dp_model import PID
from dp_model import Control_Mavros
# from matplotlib import animation as animation
# import matplotlib.pyplot as plt

class Controller(object):
    def __init__(self):
        self.view = View(self)
        self.model = Model()
        self.compass_PID = PID(4,0,0,None) #PID for compass
        self.local_x_PID = PID(0.1,0,0,None) #PID for local_x
        self.local_y_PID = PID(0.1,0,0,None) #PID for local_y
        self.mavros_module = Control_Mavros(self,self.view)
        self.compass_setpoint_placeholder = []
        self.compass_value_placeholder = []
        # self.animation()
    """
    The code to update the Compass Matplot
    1. First clear the plot
    2. Using the callback from the Model compass subscriber,
       update the whole values
    3. Add a list to hold the values--this is named as compass_placeholder 
       in the Mavros class
    """
    def change_compass_matplot(self,compass_value_list,compass_SP_list):
        self.view.compass_axis.clear()
        self.view.compass_axis.plot(compass_value_list,label="Compass Value")
        self.view.compass_axis.plot(compass_SP_list,label="Compass SP")
        self.view.compass_axis.legend()
        plt.show()


    def change_compass_P(self,v):
        value_slider = self.view.compass_P.get()
        self.compass_PID.Kp = value_slider
        rospy.loginfo("the P value is changed to %f",value_slider)

    def change_compass_setpoint(self,v):
        value_slider = self.view.compass_setpoint.get()
        self.compass_PID.setPoint = value_slider
        rospy.loginfo("THE compass SP is %f",value_slider)
    
    def compass_DP_ON(self):
        self.mavros_module.DP_compass_flag=1
        self.view.compass_control_status.configure(text="Status:ON",fg='green')
        
    def compass_DP_OFF(self):
        self.mavros_module.DP_compass_flag=0
        self.view.compass_control_status.configure(text="Status:OFF",fg='red')

    """
    Create an animation function for the plotting
    """
    # def animation(self):
    #     self.ani = animation.FuncAnimation(self.view.compass_fig,self.animate,interval=1000)
    #     plt.show()

    # def animate(self,i):
    #     print("Hi I am in animate")
    #     self.compass_axis.clear()
    #     self.compass_axis.plot(self.compass_value_placeholder,label="Compass")
    #     self.compass_axis.plot(self.compass_setpoint_placeholder,label = "SP")
    #     self.compass_axis.legend()
if __name__ == "__main__":
    rospy.init_node("DP_1") #important to initalise the node
    app = Controller()
    app.view.main()