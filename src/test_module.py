#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui5.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import sys
from mavros_msgs.srv import *
from mavros_msgs.msg import OverrideRCIn


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 131, 17))
        self.label.setObjectName("label")
        self.ARM = QtWidgets.QPushButton(self.centralwidget)
        self.ARM.setGeometry(QtCore.QRect(8, 60, 101, 51))
        self.ARM.setObjectName("ARM")
        self.DISARM = QtWidgets.QPushButton(self.centralwidget)
        self.DISARM.setGeometry(QtCore.QRect(140, 60, 101, 51))
        self.DISARM.setObjectName("DISARM")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 140, 131, 17))
        self.label_2.setObjectName("label_2")
        self.manual = QtWidgets.QPushButton(self.centralwidget)
        self.manual.setGeometry(QtCore.QRect(10, 170, 121, 51))
        self.manual.setObjectName("manual")
        self.guided = QtWidgets.QPushButton(self.centralwidget)
        self.guided.setGeometry(QtCore.QRect(150, 170, 121, 51))
        self.guided.setObjectName("guided")
        self.modex = QtWidgets.QPushButton(self.centralwidget)
        self.modex.setGeometry(QtCore.QRect(280, 170, 121, 51))
        self.modex.setObjectName("modex")
        self.modey = QtWidgets.QPushButton(self.centralwidget)
        self.modey.setGeometry(QtCore.QRect(420, 170, 121, 51))
        self.modey.setObjectName("modey")
        self.forward_slider = QtWidgets.QSlider(self.centralwidget)
        self.forward_slider.setGeometry(QtCore.QRect(20, 290, 51, 181))
        self.forward_slider.setMinimum(1300)
        self.forward_slider.setMaximum(1700)
        self.forward_slider.setSingleStep(5)
        self.forward_slider.setProperty("value", 1495)
        self.forward_slider.setOrientation(QtCore.Qt.Vertical)
        self.forward_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.forward_slider.setObjectName("forward_slider")
        self.forward_label = QtWidgets.QLabel(self.centralwidget)
        self.forward_label.setGeometry(QtCore.QRect(20, 260, 67, 17))
        self.forward_label.setObjectName("forward_label")
        self.yaw_slider = QtWidgets.QSlider(self.centralwidget)
        self.yaw_slider.setGeometry(QtCore.QRect(100, 290, 51, 181))
        self.yaw_slider.setMinimum(1300)
        self.yaw_slider.setMaximum(1700)
        self.yaw_slider.setSingleStep(5)
        self.yaw_slider.setProperty("value", 1495)
        self.yaw_slider.setOrientation(QtCore.Qt.Vertical)
        self.yaw_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.yaw_slider.setObjectName("yaw_slider")
        self.yaw_label = QtWidgets.QLabel(self.centralwidget)
        self.yaw_label.setGeometry(QtCore.QRect(120, 260, 67, 21))
        self.yaw_label.setObjectName("yaw_label")
        self.lateral_slider = QtWidgets.QSlider(self.centralwidget)
        self.lateral_slider.setGeometry(QtCore.QRect(190, 290, 51, 181))
        self.lateral_slider.setMinimum(1300)
        self.lateral_slider.setMaximum(1700)
        self.lateral_slider.setSingleStep(5)
        self.lateral_slider.setProperty("value", 1495)
        self.lateral_slider.setOrientation(QtCore.Qt.Vertical)
        self.lateral_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.lateral_slider.setObjectName("lateral_slider")
        self.lateral_label = QtWidgets.QLabel(self.centralwidget)
        self.lateral_label.setGeometry(QtCore.QRect(190, 260, 67, 21))
        self.lateral_label.setObjectName("lateral_label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 520, 201, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(430, 520, 201, 31))
        self.label_4.setObjectName("label_4")

        self.x_velocity = QtWidgets.QSlider(self.centralwidget)
        self.x_velocity.setGeometry(QtCore.QRect(430, 290, 51, 181))
        self.x_velocity.setMinimum(0)
        self.x_velocity.setMaximum(10)
        self.x_velocity.setSingleStep(1)
        self.x_velocity.setPageStep(1)
        self.x_velocity.setProperty("value", 0)
        self.x_velocity.setOrientation(QtCore.Qt.Vertical)
        self.x_velocity.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.x_velocity.setObjectName("x_velocity")

        self.lateral_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.lateral_label_2.setGeometry(QtCore.QRect(430, 260, 67, 21))
        self.lateral_label_2.setObjectName("lateral_label_2")
        
        self.y_velocity = QtWidgets.QSlider(self.centralwidget)
        self.y_velocity.setGeometry(QtCore.QRect(530, 290, 51, 181))
        self.y_velocity.setMinimum(0)
        self.y_velocity.setMaximum(10)
        self.y_velocity.setSingleStep(1)
        self.y_velocity.setPageStep(1)
        self.y_velocity.setProperty("value", 0)
        self.y_velocity.setOrientation(QtCore.Qt.Vertical)
        self.y_velocity.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.y_velocity.setObjectName("y_velocity")
       
        self.lateral_label_3 = QtWidgets.QLabel(self.centralwidget)
        self.lateral_label_3.setGeometry(QtCore.QRect(530, 260, 67, 21))
        self.lateral_label_3.setObjectName("lateral_label_3")
        
        self.fwd_text = QtWidgets.QLabel(self.centralwidget)
        self.fwd_text.setGeometry(QtCore.QRect(20, 480, 67, 17))
        self.fwd_text.setObjectName("fwd_text")
        self.yaw_text = QtWidgets.QLabel(self.centralwidget)
        self.yaw_text.setGeometry(QtCore.QRect(100, 480, 67, 17))
        self.yaw_text.setObjectName("yaw_text")
        
        self.lateral_text = QtWidgets.QLabel(self.centralwidget)
        self.lateral_text.setGeometry(QtCore.QRect(180, 480, 67, 17))
        self.lateral_text.setObjectName("lateral_text")
        self.x_vel_text = QtWidgets.QLabel(self.centralwidget)
        self.x_vel_text.setGeometry(QtCore.QRect(430, 480, 67, 17))
        self.x_vel_text.setObjectName("x_vel_text")
        self.y_vel_text = QtWidgets.QLabel(self.centralwidget)
        self.y_vel_text.setGeometry(QtCore.QRect(530, 480, 67, 17))
        self.y_vel_text.setObjectName("y_vel_text")
        self.z_angle_rotation = QtWidgets.QSlider(self.centralwidget)
        self.z_angle_rotation.setGeometry(QtCore.QRect(640, 290, 51, 181))
        self.z_angle_rotation.setMinimum(0)
        self.z_angle_rotation.setMaximum(5)
        self.z_angle_rotation.setSingleStep(1)
        self.z_angle_rotation.setPageStep(1)
        self.z_angle_rotation.setProperty("value", 0)
        self.z_angle_rotation.setOrientation(QtCore.Qt.Vertical)
        self.z_angle_rotation.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.z_angle_rotation.setObjectName("z_angle_rotation")
        self.lateral_label_4 = QtWidgets.QLabel(self.centralwidget)
        self.lateral_label_4.setGeometry(QtCore.QRect(626, 260, 81, 21))
        self.lateral_label_4.setObjectName("lateral_label_4")
        self.z_rot_text = QtWidgets.QLabel(self.centralwidget)
        self.z_rot_text.setGeometry(QtCore.QRect(640, 480, 91, 16))
        self.z_rot_text.setObjectName("z_rot_text")
        self.emergency_btn = QtWidgets.QPushButton(self.centralwidget)
        self.emergency_btn.setGeometry(QtCore.QRect(620, 20, 141, 111))
        self.emergency_btn.setAutoFillBackground(False)
        self.emergency_btn.setObjectName("emergency_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PIXHAWK CONTROLLER"))
        self.label.setText(_translate("MainWindow", "MASTER CONTROL"))
        self.ARM.setText(_translate("MainWindow", "ARM"))
        self.DISARM.setText(_translate("MainWindow", "DISARM"))
        self.label_2.setText(_translate("MainWindow", "MODE CHANGER"))
        self.manual.setText(_translate("MainWindow", "MANUAL MODE"))
        self.guided.setText(_translate("MainWindow", "GUIDED MODE"))
        self.modex.setText(_translate("MainWindow", "MODEX-STAB"))
        self.modey.setText(_translate("MainWindow", "MODEY"))
        self.forward_slider.setToolTip(_translate("MainWindow", "Control throttle"))
        self.forward_label.setText(_translate("MainWindow", "Forward"))
        self.yaw_slider.setToolTip(_translate("MainWindow", "Control yaw"))
        self.yaw_label.setText(_translate("MainWindow", "Yaw"))
        self.lateral_slider.setToolTip(_translate("MainWindow", "Control lateral"))
        self.lateral_label.setText(_translate("MainWindow", "Lateral"))
        self.label_3.setText(_translate("MainWindow", "RC CHANNEL OVERIDE"))
        self.label_4.setText(_translate("MainWindow", "MANUAL CONTROLS"))
        self.x_velocity.setToolTip(_translate("MainWindow", "Control x-velocity"))
        self.lateral_label_2.setText(_translate("MainWindow", "X-VEL"))
        self.y_velocity.setToolTip(_translate("MainWindow", "Control y-velocity"))
        self.lateral_label_3.setText(_translate("MainWindow", "Y-VEL"))
        self.fwd_text.setText(_translate("MainWindow", "1"))
        self.yaw_text.setText(_translate("MainWindow", "2"))
        self.lateral_text.setText(_translate("MainWindow", "3"))
        self.x_vel_text.setText(_translate("MainWindow", "4"))
        self.y_vel_text.setText(_translate("MainWindow", "5"))
        self.z_angle_rotation.setToolTip(_translate("MainWindow", "Control z-angular"))
        self.lateral_label_4.setText(_translate("MainWindow", "Z-ROT"))
        self.z_rot_text.setText(_translate("MainWindow", "6"))
        self.emergency_btn.setText(_translate("MainWindow", "EMERGENCY STOP"))



class Controller(Ui_MainWindow):
    def __init__(self,mainwindow):
        rospy.init_node('GUI',anonymous=True)
        self.setupUi(mainwindow)

        self.talker = rospy.Publisher('/mavros/rc/override',OverrideRCIn,queue_size=10)
        self.forward_slider.valueChanged.connect(self._fwd_speed)
        self.yaw_slider.valueChanged.connect(self._yaw_change)
        self.lateral_slider.valueChanged.connect(self._lateral_change)


        self.flight_mode_changer = rospy.ServiceProxy('/mavros/set_mode',mavros_msgs.srv.SetMode)   
        self.arm_disarm = rospy.ServiceProxy('/mavros/cmd/arming',mavros_msgs.srv.CommandBool)

        self.ARM.clicked.connect(self._arm)
        self.DISARM.clicked.connect(self._disarm)

        self.manual.clicked.connect(self._manual_mode)
        self.guided.clicked.connect(self._guided_mode)
        self.modex.clicked.connect(self._modex_mode)
        self.modey.clicked.connect(self.modey_mode)

        self.rc_channels_msg = OverrideRCIn()
        self.rc_channels_msg.channels = [1495,1495,1495,1495,0,0,1500,982]
        #indexing of rc channels and corresponding functions
        #[0,1,2,3,4,5,6,7]- indexes
        #[1,2,3,4,5,6,7,8]-actual channels
        #[Roll(left,right), Sway,Throtle,Sway,Arm,None,None,Mode]
        

        self.fwd_rc = self.forward_slider.value()
        self.yaw_rc = self.yaw_slider.value()
        self.lateral_rc = self.lateral_slider.value()
        self.emergency_btn.clicked.connect(self._emergency_fn)


        self.timer = QTimer()
        self.timer.timeout.connect(lambda : self._publisher(self.rc_channels_msg))
        self.timer.start(100)

    def _arm(self):
        rospy.wait_for_service('/mavros/cmd/arming')
        try:
            self.arm_disarm(True)
        except rospy.ServiceException:
            print ('arming failed')

    def _disarm(self):
        rospy.wait_for_service('/mavros/cmd/arming')
        try:
            self.arm_disarm(False)
        except rospy.ServiceException:
            print ('Disarm Failed')

    def _emergency_fn(self):
        rospy.wait_for_service('/mavros/cmd/arming')
        self.arm_disarm(False)
        self.rc_channels_msg.channels = [1500,1500,1500,1500,1500,1500,1500,1500]
        print('emergency activated')


    def _fwd_speed(self):
        self.fwd_rc = self.forward_slider.value()
        self.rc_channels_msg.channels[2] = self.fwd_rc



    def _yaw_change(self):
        self.yaw_rc = self.yaw_slider.value()
        self.rc_channels_msg.channels[0] = self.yaw_rc

    
    def _lateral_change(self):        
        self.lateral_rc = self.lateral_slider.value()
        self.rc_channels_msg.channels[1] = self.lateral_rc
        self.rc_channels_msg.channels[3] = self.lateral_rc        

    def _publisher(self,msg_to_send):
        self.talker.publish(msg_to_send)
        
    def _manual_mode(self):
        rospy.wait_for_service('/mavros/set_mode')
        try:
            self.flight_mode_changer(custom_mode = 'MANUAL')
        except rospy.ServiceException:
            print (' failed')


    def _guided_mode(self):
        rospy.wait_for_service('/mavros/set_mode')
        try:
            self.flight_mode_changer(custom_mode = 'GUIDED')
        except rospy.ServiceException:
            print (' failed')


    def _modex_mode(self):
        rospy.wait_for_service('/mavros/set_mode')
        try:
            self.flight_mode_changer(custom_mode = 'STABILIZE')
        except rospy.ServiceException:
            print (' failed')


    def modey_mode(self):
        pass 
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    ui = Controller(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())