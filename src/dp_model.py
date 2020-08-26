#!/usr/bin/env python

import rospy
from mavros_msgs.msg import OverrideRCIn
from std_msgs.msg import Float64 #the message for compass
from geometry_msgs.msg import PoseStamped
import numpy as np


class Model(object):
    def __init__(self):
        print("hello I'm in Model Now")





class Mavros(object):
    def __init__(self):
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
        """
        self.compass_subscriber = rospy.Subscriber("/mavros/global_position/compass_hdg",Float64,self.compass_callback)
        self.location_X_subscriber = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,self.local_x_callback)
        self.location_Y_subscriber = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,self.local_y_callback)
        self.rc_message = OverrideRCIn()
        self.rc_message.channels = [0,0,0,0,0,0,0,0]
        self.RC_Publisher = rospy.Publisher("/mavros/rc/override",OverrideRCIn,queue_size=10)
        self.DP_compass_flag =0
        self.DP_local_x_flag =0
        self.DP_local_y_flag =0
        self.safe_pwm = 1500
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
        rospy.loginfo("The setpoint compass value is %f",setpoint)
        """
        Logic is to turn on the update only if the flag is true
        Or it means DP system for Compass is turned on.
        """
        compass_pwm_out = 0 #controller_out to be added

        if self.DP_compass_flag:
            self.function_for_rc_publish(compass_pwm_out,self.safe_pwm,self.safe_pwm)
        else:
            rospy.loginfo("DP for compass is turned Off,Compass value is %f",compass_value)
            self.function_for_rc_publish()


    def function_for_rc_publish(self,compass_pwm = 1500,local_x_pwm = 1500,local_y_pwm =1500):
        """
            In this logic,the local_x and local_y can change based on origin
            set automatically.
        """
            
        self.rc_message.channels[0] = compass_pwm
        self.rc_message.channels[2] = local_x_pwm
        self.rc_message.channels[3] = local_y_pwm
        self.RC_Publisher.publish(self.rc_message)

    def local_x_callback(self,msg):
        x = msg.pose.position.x
        local_x_pwm_out = 0 #add controller out here
        if self.DP_local_x_flag:     
            self.function_for_rc_publish(self.safe_pwm,local_x_pwm_out,self.safe_pwm)
        else:
            rospy.loginfo("DP for Local_X turned off,local_x value is %f",x)
            self.function_for_rc_publish()


    def local_y_callback(self,msg):
        y = msg.pose.position.y
        local_y_pwm_out = 0 #add controller out here
        if self.DP_local_y_flag:    
            self.function_for_rc_publish(self.safe_pwm,local_x_pwm_out,self.safe_pwm)
        else:
            rospy.loginfo("DP for Local_Y turned off,local_y value is %f",y)
            self.function_for_rc_publish()
"""
The reference to PID object
1) https://github.com/ivmech/ivPID/blob/master/PID.py
2) https://github.com/m-lundberg/simple-pid
3) Notes by Prof: Guoyuan at NTNU Alesund
"""   
class PID(object):
    "A PID Control"
    def __init__(self,P =0.1,I=0.0,D=0.0,current_time=None):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.sample_time = 0.1
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time
        self.dead_band = 1500
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
        if self.output <-200:
            self.output = -200
        
        elif self.output>200:
            self.output = 200
        else:
            self.output = self.output
        self.output = self.dead_band + self.output
        rospy.loginfo("Output of the PID %d",self.output)