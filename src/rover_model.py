#!/usr/bin/env python
import Tkinter as tk
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from geometry_msgs.msg import PoseStamped
import math 
from mavros_msgs.msg import OverrideRCIn

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
        # self.filteredOdomSubscriber=rospy.Subscriber("/mavros/global_position/compass_hdg",Float64,self.state)
        self.filteredRelativeHeight=rospy.Subscriber("/mavros/global_position/rel_alt",Float64,self.state)
        self.controller = controller
        self.setpointPublisher = rospy.Publisher("/setpoint",Float64,queue_size=10)
        self.statepublisher = rospy.Publisher("/state",Float64,queue_size=10)
        self.RCPublisher = rospy.Publisher("/mavros/rc/override",OverrideRCIn,queue_size=10)
        self.controlSignalSubscriber=rospy.Subscriber("/control_effort",Float64,self.controlaction)
        self.rc_msg = OverrideRCIn()
        self.rc_msg.channels =[0,0,0,0,0,0,0,0]


    def controlaction(self,msg):
        control_sig = msg.data 
        rospy.loginfo("Control Signal %f",control_sig)
        # self.rc_msg.channels[2]=1600
        self.rc_msg.channels[2]=control_sig
        self.RCPublisher.publish(self.rc_msg)


    def state(self,msg):
        altitude = msg.data 
        rospy.loginfo("The altitude value is %f",altitude)
        self.statepublisher.publish(altitude)

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
        setpoint_required = 5.0
        self.setpointPublisher.publish(setpoint_required)
    