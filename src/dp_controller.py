#!/usr/bin/env python


# from dp_view import View
import rospy
from dp_view import View
from dp_model import Model
from dp_model import PID
from dp_model import Control_Mavros
import numpy as np
# from matplotlib import animation as animation
# import matplotlib.pyplot as plt

class Controller(object):
    def __init__(self):
        self.view = View(self)
        self.model = Model()
        self.compass_PID = PID(2,0,0,None) #PID for compass
        print(self.compass_PID.Kp)
        self.local_x_PID = PID(0.1,0,0,None) #PID for local_x
        self.local_y_PID = PID(0.1,0,0,None) #PID for local_y
        self.mavros_module = Control_Mavros(self,self.view)
        self.compass_setpoint_placeholder = []
        self.compass_value_placeholder = []
        # self.animation()
    """
    The code to update the Compass Matplot
    1. First clear the plot.
    2. Using the callback from the Model compass subscriber,
       update the whole values.
    3. Add a list to hold the values--this is named as compass_placeholder 
       in the Mavros class.
    """
    def change_compass_matplot(self,compass_value_list,compass_SP_list):
        self.view.compass_axis.clear()
        self.view.compass_axis.plot(compass_value_list,label="Compass Value")
        self.view.compass_axis.plot(compass_SP_list,label="Compass SP")
        self.view.compass_axis.legend()
        plt.show()

    
    def change_compass_P(self,v):
        """Changes the compass PID P-value"""
        value_slider = self.view.compass_P.get()
        self.compass_PID.Kp = value_slider
        rospy.loginfo("the P value is changed to %f",value_slider)
    
    def change_compass_setpoint(self,v):
        """Changes the compass PID Compass Setpoint Value"""
        value_slider = self.view.compass_setpoint.get()
        self.compass_PID.setPoint = value_slider
        rospy.loginfo("THE compass SP is %f",value_slider)
    
    def change_compass_I(self,v):
        """Changes the compass PID I-value"""
        value_slider = self.view.compass_I.get()
        self.compass_PID.Ki = value_slider
        rospy.loginfo("THE Compas Kp is changed to %f",value_slider)

    def change_compass_D(self,v):
        """Changes the compass PID D-value"""
        value_slider = self.view.compass_D.get()
        self.compass_PID.Kd = value_slider
        rospy.loginfo("THE Compas Kd is changed to %f",value_slider)
    

    def compass_DP_ON(self):
        self.mavros_module.DP_compass_flag=1
        self.view.compass_control_status.configure(text="Status:ON",fg='green')
        
    def compass_DP_OFF(self):
        self.mavros_module.DP_compass_flag=0
        self.view.compass_control_status.configure(text="Status:OFF",fg='red')


    """
    The functions that change the PID Control for the Local_x start here
    """            
    def change_local_x_P(self,v):
        """Change the local_x Kp value"""
        value_slider = self.view.local_X_P.get()
        self.local_x_PID.Kp = value_slider
        rospy.loginfo("The local_x Kp value is changed to %f",value_slider)

    def change_local_x_I(self,v):
        """Change the local_x Ki value"""
        value_slider = self.view.local_X_I.get()
        self.local_x_PID.Ki = value_slider
        rospy.loginfo("The local_x Ki value is changed to %f",value_slider)

    def change_local_x_D(self,v):
        """Change the local_y Kd value"""
        value_slider = self.view.local_X_D.get()
        self.local_x_PID.Kd = value_slider
        rospy.loginfo("The local_x Kd value is changed to %f",value_slider)

    def local_x_DP_ON(self):
        self.mavros_module.DP_local_x_flag = 1
        self.local_x_PID.setPoint = self.mavros_module.local_x_value
        sp_text = "SP X:" + str(round(self.local_x_PID.setPoint,2))
        self.view.local_X_setpoint_text.configure(text = sp_text)
        self.view.local_X_control_status.configure(text ="Status:ON",fg='green')
    
    def local_x_DP_OFF(self):
        self.mavros_module.DP_local_x_flag = 0
        self.view.local_X_control_status.configure(text="Status:OFF",fg='red')
    
    """
    The functions that change the PID Control for the Local_y start here"""

    def change_local_y_P(self,v):
        """Change the local_y Kp value"""
        value_slider = self.view.local_Y_P.get()
        self.local_y_PID.Kp = value_slider
        rospy.loginfo("The local_y Kp value is changed to %f",value_slider)

    def change_local_y_I(self,v):
        """Change the local_y Kp value"""
        value_slider = self.view.local_Y_I.get()
        self.local_y_PID.Ki = value_slider
        rospy.loginfo("The local_y Ki value is changed to %f",value_slider)

    def change_local_y_D(self,v):
        """Change the local_y Kp value"""
        value_slider = self.view.local_Y_D.get()
        self.local_y_PID.Kd = value_slider
        rospy.loginfo("The local_y Kd value is changed to %f",value_slider)

    def local_y_DP_ON(self):
        self.mavros_module.DP_local_y_flag = 1
        self.local_y_PID.setPoint = self.mavros_module.local_y_value
        sp_text = "SP Y:" + str(round(self.local_y_PID.setPoint,2))
        self.view.local_Y_setpoint_text.configure(text = sp_text)
        self.view.local_Y_control_status.configure(text ="Status:ON",fg='green')
    
    def local_y_DP_OFF(self):
        self.mavros_module.DP_local_y_flag = 0
        self.view.local_Y_control_status.configure(text="Status:OFF",fg='red')
    

    def arming_via_mavros(self):
        """
        Arm the device
        Logic of button: Green indicate the button that could be pressed and red is pressed before
        Logic of button toggles back and forth
        """
        self.mavros_module._arm()
        self.view.master_controller_arm.configure(bg='red') 
        self.view.master_controller_disarm.configure(bg='green')
    
    def disarm_via_mavros(self):
        self.mavros_module._disarm()
        self.view.master_controller_arm.configure(bg='green')
        self.view.master_controller_disarm.configure(bg='red')

    def activate_all_dp_systems(self):
        self.mavros_module.DP_compass_flag = 1
        self.mavros_module.DP_local_x_flag = 1
        self.mavros_module.DP_local_y_flag = 1
    
    def deactivate_all_dp_systems(self):
        self.mavros_module.DP_compass_flag = 0
        self.mavros_module.DP_local_x_flag = 0
        self.mavros_module.DP_local_y_flag = 0


    def plotter_function_for_path(self,x,y):
        points = np.array([x,y,0,1]) #points as a matrix
        points_to_canvas = self.model.mapping_array.dot(points)
        new_x = points_to_canvas.item(0)
        new_y = points_to_canvas.item(1)
        coords = [new_x,new_y,new_x+5,new_y+5]
        self.view.canvas_path_plot.create_rectangle(coords,fill='red')

if __name__ == "__main__":
    rospy.init_node("DP_1") #important to initalise the node
    app = Controller()
    app.view.main()