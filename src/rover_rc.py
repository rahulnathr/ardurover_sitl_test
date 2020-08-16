#!/usr/bin/env python

import Tkinter as tk
import ttk as ttk

class View(tk.Tk):
    """The GUI View of the application"""
    def __init__(self,controller):
        tk.Tk.__init__(self)
        self.controller = controller
        self.wm_resizable(0,0)


        self.title("Way Point Plotter")
        self.geometry("800x600")
        self.s = ttk.Style()
        self.s.configure('TFrame',background ='green')
        self.s.configure('Frame1.TFrame',background = 'grey93')
        self.content = ttk.Frame(self,height = 800,width=600,style ='Frame1.TFrame')
        self.content.grid(column=0,row =0,sticky=(tk.N,tk.S,tk.E,tk.W))
        self.content.columnconfigure(0,weight =1)
        self.content.columnconfigure(1,weight =2)
        self.createLeftFrame()
        self.createRightFrame()
        self.createCanvas()
        self.createButton1Layer()
        self.createButton2Layer()
        self.createPIDControlLayer()
        
        self.createCompassControlLayer()
        self.createWaypointDeleteLayer()
        self.createMission1()
        self.createMission2()
        self.PID_control_layer()
        self.compass_control_slider()
        self.wayptDelele()

    def createLeftFrame(self):
        self.s.configure('Frame2.TFrame',background='light gray')
        self.leftframe = ttk.LabelFrame(self.content, text='Controls',style='Frame2.TFrame')
        self.leftframe.grid(column=0,row=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        # self.leftframe.rowconfigure(0,weight=1)
        # self.leftframe.rowconfigure(1,weight=1)



    def createRightFrame(self):
        self.s.configure('Frame3.TFrame',background='light gray')
        self.rightframe = ttk.LabelFrame(self.content, text='Canvas', style='Frame3.TFrame')
        self.rightframe.grid(column=1, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    def createCanvas(self):
        self.canvas_plot = tk.Canvas(self.rightframe,bg='white',height=500,width =400)
        self.canvas_plot.grid(row=0,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))

    def createButton1Layer(self):
        self.button_one_layer = tk.Frame(self.leftframe,bg = 'gray')
        self.button_one_layer.grid(row=0,column=0,sticky=(tk.N, tk.S, tk.E, tk.W),padx=5,pady=5)

    def createButton2Layer(self):
        self.button_two_layer = tk.Frame(self.leftframe, bg='white')
        self.button_two_layer.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W),padx=5,pady=5)
    
    def createPIDControlLayer(self):
        self.pid_layer = tk.Frame(self.leftframe,bg='white')
        self.pid_layer.grid(row=2, column=0, sticky=(tk.N, tk.S, tk.E, tk.W),padx=5,pady=5)    

    def createCompassControlLayer(self):
        self.compass_controllayer = tk.Frame(self.leftframe,bg='white')
        self.compass_controllayer.grid(row=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W),padx=5,pady=5)

    def createWaypointDeleteLayer(self):
        self.wpdeletelayer = tk.Frame(self.leftframe,bg ='white')
        self.wpdeletelayer.grid(row=4,column=0,sticky=(tk.N, tk.S, tk.E, tk.W),padx=5,pady=5)

    def createMission1(self):
        self.labelx = tk.Label(self.button_one_layer,text='X')
        self.labelx.grid(row=0,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.labely = tk.Label(self.button_one_layer,text='Y')
        self.labely.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.labelsentx = tk.Label(self.button_one_layer, text='Sent X')
        self.labelsentx.grid(row=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.labelsenty = tk.Label(self.button_one_layer, text='Sent Y')
        self.labelsenty.grid(row=3, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        """Entry for X coordinate and Y coordinate of mIssion 1"""
        self.entry1x = tk.Entry(self.button_one_layer)
        self.entry1x.grid(row=1,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.entry1y = tk.Entry(self.button_one_layer)
        self.entry1y.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.sentbtn = tk.Button(self.button_one_layer,text="Send Values",command = self.controller.sent_coordinates_one)
        self.sentbtn.grid(row=2,column=0,columnspan=2,sticky=(tk.N, tk.S, tk.E, tk.W))

        self.go_button = tk.Button(self.button_one_layer,text="Start Mission")
        self.go_button.grid(row=4,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))

        self.labelStatus = tk.Label(self.button_one_layer, text='Status')
        self.labelStatus.grid(row=4, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        

        self.progress_bar = ttk.Progressbar(self.button_one_layer,mode='determinate',orient=tk.HORIZONTAL)
        self.progress_bar.grid(row =5,column=0,columnspan=2,sticky=(tk.N, tk.S, tk.E, tk.W))

    def createMission2(self):
        self.labelx = tk.Label(self.button_two_layer,text='X')
        self.labelx.grid(row=0,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.labely = tk.Label(self.button_two_layer,text='Y')
        self.labely.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.labelsentx = tk.Label(self.button_two_layer, text='Sent X')
        self.labelsentx.grid(row=3, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.labelsenty = tk.Label(self.button_two_layer, text='Sent Y')
        self.labelsenty.grid(row=3, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        """Entry for X coordinate and Y coordinate of mIssion 1"""
        self.entry2x = tk.Entry(self.button_two_layer)
        self.entry2x.grid(row=1,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.entry2y = tk.Entry(self.button_two_layer)
        self.entry2y.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.sentbtn = tk.Button(self.button_two_layer,text="Send Values",command = self.controller.sent_coordinates_two)
        self.sentbtn.grid(row=2,column=0,columnspan=2,sticky=(tk.N, tk.S, tk.E, tk.W))

        self.go_button = tk.Button(self.button_two_layer,text="Start Mission")
        self.go_button.grid(row=4,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))

        self.labelStatus = tk.Label(self.button_two_layer, text='Status')
        self.labelStatus.grid(row=4, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        
        self.progress_bar = ttk.Progressbar(self.button_two_layer,mode='determinate',orient=tk.HORIZONTAL)
        self.progress_bar.grid(row =5,column=0,columnspan=2,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.progress_bar['value'] =50
    
    
    def wayptDelele(self):
        self.delentry = tk.Entry(self.wpdeletelayer)
        self.delentry.grid(row =0,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))

        self.deltebtn = tk.Button(self.wpdeletelayer,text="Delete WP",command=self.controller.delete_waypoints)
        self.deltebtn.grid(row=0,column=1,sticky=(tk.N, tk.S, tk.E, tk.W))
    def PID_control_layer(self):
        self.P_scale = tk.Scale(self.pid_layer,from_=0,to=20.0,orient=tk.HORIZONTAL,
                                resolution=0.1, command = self.controller.change_P_value)
        self.P_scale.grid(row=0,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.P_scale_label = tk.Label(self.pid_layer,text="P value")
        self.P_scale_label.grid(row=0,column=1,sticky=(tk.N, tk.S, tk.E, tk.W))

        self.I_scale = tk.Scale(self.pid_layer,from_=0,to=5,orient=tk.HORIZONTAL,
                                resolution=0.01,command = self.controller.change_I_value)
        self.I_scale.grid(row=1,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.I_scale_label = tk.Label(self.pid_layer,text="I value")
        self.I_scale_label.grid(row=1,column=1,sticky=(tk.N, tk.S, tk.E, tk.W))

        self.D_scale = tk.Scale(self.pid_layer,from_=0,to=5,orient=tk.HORIZONTAL,
                        resolution=0.01,command = self.controller.change_D_value)
        self.D_scale.grid(row=2,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.D_scale_label = tk.Label(self.pid_layer,text="D value")
        self.D_scale_label.grid(row=2,column=1,sticky=(tk.N, tk.S, tk.E, tk.W))

    def compass_control_slider(self):
        self.compass_scale = tk.Scale(self.compass_controllayer,from_=0,to=360.0,
                            orient=tk.HORIZONTAL,resolution=0.1,
                             command = self.controller.change_setPoint)
        self.compass_scale.grid(row=0,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        
    def main(self):
        self.mainloop()
