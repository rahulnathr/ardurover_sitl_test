#!/usr/bin/env python

import rospy
from mavros_msgs.msg import OverrideRCIn
from std_msgs.msg import Float64 #the message for compass
from geometry_msgs.msg import PoseStamped #the message for the location data
from nav_msgs.msg import Odometry #the message type for the global local data into NED
import numpy as np
import time
import math
from matplotlib import animation as animation
import matplotlib.pyplot as plt
from mavros_msgs.srv import *

class Model(object):
    def __init__(self):
        print("hello I'm in Model Now")

        """
        Things to do

        1. Homogenous transformation matrix for the canvas plotting.
        2. 
        
        """
        self.originx = 200
        self.originy = 150
        self.originz = 0
        self.mapping_array = np.array([[1,0,0,self.originx],
                                        [0,1,0,self.originy],
                                        [0,0,1,self.originz],
                                        [0,0,0,1]])




class Control_Mavros(object):
    def __init__(self,controller,view):
        """
        The class for the MAVROS Module
        """
        print("Hello I am in Mavros Now")
        """
        In this class following things are required
        1. Subscriber for Compass heading
        2. Subscriber for Local_X
        3. Subscriber for Local_Y
        4. Publisher for RC_commands.
        5. Definition of RC_channel_msgs
        6. Add service for Arm and Disarm commands.
        7. Controller object       
        """
        self.view = view
        self.compass_subscriber = rospy.Subscriber("/mavros/global_position/compass_hdg",Float64,self.compass_callback)
        """
        # this was the previous fused Kalman filter data which proved to be unreliable. Now we are using 
        the global gps values as written in the subsequent lines.

        # self.location_X_subscriber = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,self.local_x_callback)
        # self.location_Y_subscriber = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,self.local_y_callback)
        """
        self.location_X_subscriber = rospy.Subscriber("/mavros/global_position/local",Odometry,self.local_x_callback)
        self.location_Y_subscriber = rospy.Subscriber("/mavros/global_position/local",Odometry,self.local_y_callback)
                                                                                            
        self.rc_message = OverrideRCIn()
        self.rc_message.channels = [0,0,0,0,0,0,0,982] #[1500,1500,1500,1500,0,0,1500,982]
        self.RC_Publisher = rospy.Publisher("/mavros/rc/override",OverrideRCIn,queue_size=10)
        self.DP_compass_flag = 0 #flag to turn on/off compass_dp,main flag
        self.DP_local_x_flag = 0 #flag to turn on/off local_x_dp,main flag
        self.DP_local_y_flag = 0 #flag to turn on/off local_y_dp,main flag
        self.safe_pwm = 1495
        self.controller = controller #passing the controler object
        self.compass_value_placeholder = []
        self.compass_value_SP_placeholder = []
        self.local_x_placeholder = []
        self.local_x_value_SP_placeholder = []
        self.local_y_placeholder = []
        self.local_y_value_SP_placeholder = []
        self.local_x_value = 0  #placeholder to update the subscribed x values
        self.local_y_value = 0  #placeholder to update the subscribed y values
        self.arm_disarm = rospy.ServiceProxy('/mavros/cmd/arming',mavros_msgs.srv.CommandBool)
        self.animation_main_for_matplot()

        """Experimental--almost approved""" 
        self.counter_local_x = 0 #internal counter for local X
        self.counter_local_y = 0 #internal counter for local Y
        self.internal_local_x_dp_flag = 0 #internal flag
        self.internal_local_y_dp_flag = 0 #internal flag
        self.local_x_pwm = 1495 
        self.local_y_pwm = 1495 
        self.compass_pwm_out = 1495
        """
        The rc channels are as follows:
        Channel 1 -- Yaw ---equivalent to 0 in the list
        Channel 3 -- Throttle -- equal to 2 in the list
        Channel 4 -- Sway -- equal to 3 in the list

        """

    def compass_callback(self,msg):
        compass_value = msg.data #retrieve compass data from ros
        
        """
        uncomment to add logging feature for compass value 
        uncomment to add logging feature for setpoint value from controller
        """
        rospy.loginfo("The compass value is %f",compass_value)
        rospy.loginfo("The setpoint compass value is %f",self.controller.compass_PID.setPoint)
        """
        Logic is to turn on the update only if the flag is true
        Or it means DP system for Compass is turned on.
        ---->Similarly add a list to append COmpass value for dynamic plot-SP and compass
        ---->Also the plot is updated no matter if DP is on or not.
        """
        self.compass_value_placeholder.append(int(compass_value))
        self.compass_value_SP_placeholder.append(int(self.controller.compass_PID.setPoint))
        
        self.controller.compass_PID.update(compass_value,None) #this calls the update function of PID which computes the PWM
    
        self.compass_pwm_out = self.controller.compass_PID.output #return the updated value of PWM
        if self.DP_compass_flag:
            # self.function_for_rc_publish(self.compass_pwm_out,self.safe_pwm,self.safe_pwm)
            # print(compass_pwm_out)
            self.publish_limiter(self.compass_pwm_out,self.local_x_pwm,self.local_y_pwm,
                        self.internal_local_x_dp_flag,self.internal_local_y_dp_flag)
        else:
            self.compass_pwm_out = 1500 #reset to 1500 or natural state.
            rospy.loginfo("DP for compass is turned Off,Compass value is %f",compass_value)
            # self.function_for_rc_publish(self.safe_pwm,1500,self.safe_pwm)
    

    def publish_limiter(self,compass_pwm = 1495,local_x_pwm = 1495,local_y_pwm = 1495,DP_internal_local_x_flag=0,DP_internal_local_y_flag=0):
        int_x_flag = DP_internal_local_x_flag
        int_y_flag = DP_internal_local_y_flag
        if (int_x_flag == 1 and int_y_flag == 0): #x on and y off,publish only x
            self.function_for_rc_publish(compass_pwm,local_x_pwm,1495)
            rospy.loginfo("The channels are  X %f and Y %f",local_x_pwm,local_y_pwm)
        elif (int_y_flag == 1 and int_x_flag ==0): #x off and y on,publish only y
            self.function_for_rc_publish(compass_pwm,1495,local_y_pwm)
            rospy.loginfo("The channels are  Y %f and X %f",local_y_pwm,local_x_pwm)
        elif (int_x_flag == 1 and int_y_flag == 1):
            self.function_for_rc_publish(compass_pwm,self.safe_pwm,self.safe_pwm)
            rospy.loginfo("Both ON,so cancelling both X and Y")
        else:
            self.function_for_rc_publish(compass_pwm,self.safe_pwm,self.safe_pwm)
            rospy.loginfo("Both OFF")

    def function_for_rc_publish(self,compass_pwm = 1495,local_x_pwm = 1495,local_y_pwm =1495):
        """
            In this logic,the local_x and local_y can change based on origin
            set automatically.
        """
        self.rc_message.channels[0] = compass_pwm
        self.rc_message.channels[2] = local_x_pwm
        self.rc_message.channels[3] = local_y_pwm
        self.rc_message.channels[1] = local_y_pwm
        print(self.rc_message)
        self.RC_Publisher.publish(self.rc_message)

    def local_x_callback(self,msg):

        # self.local_x_value = msg.pose.position.x # live X coordinate from Mavros
        self.local_x_value = msg.pose.pose.position.x
        plot_x = round(self.local_x_value,2)
        plot_y = round(msg.pose.pose.position.y,2)
        self.counter_local_x = self.counter_local_x + 1 #counter to assess the optimum PWM Delivery
        x_string = "Current X: " + str(round(self.local_x_value,2))
        self.view.local_X_control_current_X.configure(text = x_string)
        # rospy.loginfo("X counter %f",self.counter_local_x)

        if self.counter_local_x < 6:
            print("Channel 2 ON "+str(self.counter_local_x))
            self.internal_local_x_dp_flag = 1
        elif self.counter_local_x == 11: #counter getting reset here 
            self.counter_local_x = 0 #reset value to zero
        else:
            print("Channel 2 OFF"+str(self.counter_local_x))
            self.internal_local_x_dp_flag = 0

        self.local_x_placeholder.append(self.local_x_value) #this list goes for live plotting of the local_x_value
        self.controller.plotter_function_for_path(plot_x,plot_y)
        if self.DP_local_x_flag: #checking for the main toggle flag
            """
                Logic here is to check if the new_x value is within +/- 1 m from the setpoint
                If greater than 0.8m from current SP, give new value for update
                if less than 0.8 m from current SP, give new value for update
                else, give current SP  for update.
            """
            if self.local_x_value > (self.controller.local_x_PID.setPoint + 1):
                self.controller.local_x_PID.update(self.local_x_value,None)
            elif self.local_x_value < (self.controller.local_x_PID.setPoint - 1):
                self.controller.local_x_PID.update(self.local_x_value,None)
            else:
                self.controller.local_x_PID.update(self.controller.local_x_PID.setPoint)
            
            self.local_x_pwm = self.controller.local_x_PID.output   #add controller out here
            # self.local_x_pwm = 1600
            print("local_x_works")     
            # self.function_for_rc_publish(self.safe_pwm,local_x_pwm_out,self.safe_pwm)
            self.publish_limiter(self.compass_pwm_out,self.local_x_pwm,self.local_y_pwm,
                        self.internal_local_x_dp_flag,self.internal_local_y_dp_flag)
            
        else:
            # rospy.loginfo("DP for Local_X turned off,local_x value is %f",self.local_x_value)
            self.local_x_pwm = 1495
            # self.publish_limiter(1500,self.local_x_pwm,self.local_y_pwm,
            #             self.internal_local_x_dp_flag,self.internal_local_y_dp_flag)
            
            # self.function_for_rc_publish(self.safe_pwm,1700,self.safe_pwm)
        

    def local_y_callback(self,msg):
        self.local_y_value = msg.pose.pose.position.y
        
        self.counter_local_y = self.counter_local_y + 1
        # rospy.loginfo("Y counter %f",self.counter_local_y)
        y_string = "Current Y: " + str(round(self.local_y_value,2))
        self.view.local_Y_control_current_Y.configure(text = y_string)
        
        if self.counter_local_y == 11:
            self.counter_local_y = 0
        elif self.counter_local_y > 5:
            print("Channel 3 ON"+str(self.counter_local_y))
            self.internal_local_y_dp_flag = 1
        else:
            print("Channel 3 OFF"+str(self.counter_local_y))
            self.internal_local_y_dp_flag = 0
        
        
        self.local_y_placeholder.append(self.local_y_value) #this list goes for the live plotting of the local_y_value
        if self.DP_local_y_flag:
            """
                Logic here is to check if the new_x value is within +/- 1 m from the setpoint
                If greater than 0.8m from current SP, give new value for update
                if less than 0.8 m from current SP, give new value for update
                else, give current SP  for update
            """
            if self.local_y_value > (self.controller.local_y_PID.setPoint + 1):
                self.controller.local_y_PID.update(self.local_y_value,None)
            elif self.local_y_value < (self.controller.local_y_PID.setPoint - 1):
                self.controller.local_y_PID.update(self.local_y_value,None)
            else:
                self.controller.local_y_PID.update(self.controller.local_y_PID.setPoint)
            
            self.local_y_pwm = self.controller.local_y_PID.output   #add controller out here
            # self.local_y_pwm = 1600
            print("local_y_works")
            self.publish_limiter(self.compass_pwm_out,self.local_x_pwm,self.local_y_pwm,
                        self.internal_local_x_dp_flag,self.internal_local_y_dp_flag)     
        else:
            self.local_y_pwm = 1495
            # self.publish_limiter(1500,self.local_x_pwm,self.local_y_pwm,
            #             self.internal_local_x_dp_flag,self.internal_local_y_dp_flag)
        #     rospy.loginfo("DP for Local_Y turned off,local_y value is %f",self.local_y_value)
        #     # self.function_for_rc_publish(self.safe_pwm,1700,self.safe_pwm)

    def _arm(self):
        rospy.wait_for_service('/mavros/cmd/arming')
        try:
            self.arm_disarm(True)
            rospy.loginfo("Armed")
        except rospy.ServiceException:
            rospy.loginfo('arming failed')

    def _disarm(self):
        rospy.wait_for_service('/mavros/cmd/arming')
        try:
            self.arm_disarm(False)
            rospy.loginfo("Disarmed")
        except rospy.ServiceException:
            rospy.loginfo('Disarm Failed')

    def animation_main_for_matplot(self):
        self.ani = animation.FuncAnimation(self.view.compass_fig,self.animate_sub,interval=300)
        self.ani2 = animation.FuncAnimation(self.view.local_x,self.animate_sub,interval = 300)
        self.ani3 = animation.FuncAnimation(self.view.local_y,self.animate_sub,interval = 300)
        plt.show()

    def animate_sub(self,i):
        # print("Hi I am in animate")
        self.view.compass_axis.clear()
        self.view.compass_axis.plot(self.compass_value_placeholder,label="Compass")
        self.view.compass_axis.plot(self.compass_value_SP_placeholder,label = "SP")
        self.view.compass_axis.legend()
        self.view.local_x_axis.clear()
        self.view.local_x_axis.plot(self.local_x_placeholder,label = "LocalX")
        self.view.local_x_axis.legend()
        self.view.local_y_axis.clear()
        self.view.local_y_axis.plot(self.local_y_placeholder,label = "LocalY")
        self.view.local_y_axis.legend()


    

"""
The reference to PID object
1) https://github.com/ivmech/ivPID/blob/master/PID.py
2) https://github.com/m-lundberg/simple-pid
3) Notes by Prof: Guoyuan at NTNU Alesund
"""   
class PID(object):
    "A PID Control Module"
    def __init__(self,P =0.1,I=0.0,D=0.0,current_time=None):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.sample_time = 0.1
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time
        self.dead_band = 1495
        self.clear()

    def clear(self):
        "Clears computations and coefficients"
        self.setPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        #windup Guard
        self.int_error = 0.0
        self.windup_guard = 200
        self.output = 0 #for the controller dead region
    
    def update(self,feedback_value,current_time=None):
        "The PID update computation"
        # self.setPoint = 0.0
        error = feedback_value - self.setPoint
        self.current_time = current_time if current_time is not None else time.time()
        
        delta_time = self.current_time-self.last_time
        delta_error = error - self.last_error
        if (delta_time >=self.sample_time):
            self.PTerm = self.Kp * error
            self.int_error = self.int_error+error
            self.ITerm = self.Ki*self.int_error *delta_time
            # self.ITerm = self.int_error *delta_time
            if (self.ITerm < -200): 
                self.ITerm = -200
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard
            

        if (delta_time>0):
            self.DTerm = delta_error / delta_time
        self.last_time = self.current_time
        self.last_error = error
        self.output = -1*int(self.PTerm+(self.ITerm)+(self.Kd*self.DTerm))
        if self.output <-200:#changing it here to -100
            self.output = -200
        
        elif self.output>200: #changing it here to 100
            self.output = 200
        else:
            self.output = self.output
        self.output = self.dead_band + self.output
        rospy.loginfo("Output of the PID %d",self.output)