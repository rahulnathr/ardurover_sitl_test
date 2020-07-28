#!/usr/bin/env python
import Tkinter as tk
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from geometry_msgs.msg import PoseStamped
import math 
from mavros_msgs.msg import OverrideRCIn
import time
class Model(object):
    def __init__(self):
        
        self.originx = 200
        self.originy = 250
        self.x = 0
        self.y = 0
        self.missionx1 = self.originx+self.x
        self.missiony1 = self.originy+self.y
        self.missionx2 = self.originx+self.y
        self.missiony2 = self.originy+self.y

class LocationMavros(object):
    def __init__(self,controller):
        self.locationSubscriber = rospy.Subscriber("/mavros/global_position/local",Odometry,self.print_location)
        #format is (topic name,topic type,callback)
        # self.filteredOdomSubscriber = rospy.Subscriber("/mavros/local_position/pose",PoseStamped,self.state)
        self.filteredOdomSubscriber=rospy.Subscriber("/mavros/global_position/compass_hdg",Float64,self.state)
        self.PID_CONTROL = PID(5,0.1,0.2)
        # self.filteredRelativeHeight=rospy.Subscriber("/mavros/global_position/rel_alt",Float64,self.state)
        self.controller = controller
        # self.setpointPublisher = rospy.Publisher("/setpoint",Float64,queue_size=10)
        # self.statepublisher = rospy.Publisher("/state",Float64,queue_size=10)
        self.RCPublisher = rospy.Publisher("/mavros/rc/override",OverrideRCIn,queue_size=10)
        # self.controlSignalSubscriber=rospy.Subscriber("/control_effort",Float64,self.controlaction)
        self.rc_msg = OverrideRCIn()
        self.rc_msg.channels =[0,0,0,0,0,0,0,0]
        self.PID_CONTROL.setPoint = 50.0
        



    # def controlaction(self,msg):
    #     control_sig = msg.data 
    #     rospy.loginfo("Control Signal %f",control_sig)
    #     # self.rc_msg.channels[2]=1600
    #     self.rc_msg.channels[2]=int(control_sig)
    #     self.RCPublisher.publish(self.rc_msg)


    def state(self,msg):
        compass = msg.data 
        rospy.loginfo("The compass value is %f",compass)
        self.PID_CONTROL.update(compass,None)
        self.rc_msg.channels[2]=1700
        self.rc_msg.channels[0]=self.PID_CONTROL.output
        self.RCPublisher.publish(self.rc_msg)

    # def state(self,msg):
    #     # required_x = 74.63
    #     # required_y = 100.51
    #     # odomx = msg.pose.position.x
    #     odomy = msg.pose.position.y
    #     # q= required_x-odomx
    #     # p = required_y-odomy
    #     # angle1 =math.atan2(required_y,required_x)
    #     # angle2 = math.atan2(q,p)
    #     # state_rad = angle1-angle2
    #     # state_deg = math.degrees(state_rad)
    #     # rospy.loginfo("state rad %f",state_rad)
    #     # rospy.loginfo("state degree %f",state_deg)
    #     rospy.loginfo("Odomx %f",odomy)
    #     self.statepublisher.publish(odomy)



    def print_location(self,msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        # rospy.loginfo("X value %f",x)
        # rospy.loginfo("Y value %f",y)

        x_round = int(round(x))
        y_round = int(round(y))
        # rospy.loginfo("X value %f",x_round)
        # rospy.loginfo("Y value %f",y_round)
        self.controller.plotter_function(x_round,y_round)
        # setpoint_required = 5.0
        # self.setpointPublisher.publish(setpoint_required)


class PID(object):
    "A PID Control"
    def __init__(self,P =0.5,I=0.0,D=0.0,current_time=None):
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
        self.setPoint = 50.0
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

