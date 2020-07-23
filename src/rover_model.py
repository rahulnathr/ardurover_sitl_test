#!/usr/bin/env python
import Tkinter as tk
import rospy
from nav_msgs.msg import Odometry



class Model(object):
    def __init__(self):
        # self.controller = controller
        self.originx = 200
        self.originy = 250
        self.x = 0
        self.y = 0
        self.missionx1 = self.originx+self.x
        self.missiony1 = self.originy+self.y
        self.missionx2 = self.originx+self.y
        self.missiony2 = self.originy+self.y

class LocationMavros(object):
    def __init__(self):
        self.locationSubscriber = rospy.Subscriber("/mavros/global_position/local",Odometry,self.print_location)
        #format is (topic name,topic type,callback)
    

    def print_location(self,msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        rospy.loginfo("X value %f",x)
        rospy.loginfo("Y value %f",y)



    