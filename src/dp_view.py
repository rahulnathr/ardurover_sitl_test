#!/usr/bin/env python
import Tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk

class View(tk.Tk):
    """
    The GUI of the application.
    """
    def __init__(self,controller):
        tk.Tk.__init__(self)
        self.controller = controller
        self.title("DP System V1")
        self.geometry("870x950")
        self.wm_resizable(0,0)
        self.s = ttk.Style()
        self.create_figure_frame()
        self.create_control_frame()
        self.create_control_frame_compass()
        self.create_control_frame_localX()
        self.create_control_frame_localY()
        self.create_controller_for_compass()
        self.create_controller_for_local_X()
        self.create_controller_for_local_Y()        
        self.create_control_frame_master()
        self.create_controller_for_master()
        self.create_canvas_frame()
        self.plotter_compass()
        self.plotter_local_x()
        self.plotter_local_y()
        self.create_canvas_for_path()
        
        
    """
    Create a Frame to hold the Matplot figures
    1. Create a style configuration
    2. Add the Tk frame
    3. Place frame using grid manager,row 0 ,col 0
    4. Add the func back to the init.
    """
    def create_figure_frame(self):
        self.s.configure('TFrame',background = 'gray')
        self.figure_frame = ttk.Frame(self,padding = 10,style='TFrame')
        self.figure_frame.grid(column=0,row=0,sticky=(tk.N, tk.S, tk.E, tk.W))


    """
    Create a Frame to hold the PID Controllers
    1. Create a style configuration
    2. Add the Tk frame
    3. Place frame using grid manager,row 0,col 1
    4. Add the func back to the init.
    """
    def create_control_frame(self):
        self.s.configure('Control.TFrame',background = 'light salmon')
        self.control_frame = ttk.Frame(self,padding = 10,style='Control.TFrame')
        self.control_frame.grid(column=1,row=0,sticky=(tk.N, tk.S, tk.E, tk.W))
    
    """Create Subframes for the PID for three axes
        col - 0
        row 0 
    
    """

    def create_control_frame_compass(self):
        self.s.configure('Compass.TFrame',background = 'honeydew2')
        self.control_frame_compass = ttk.Frame(self.control_frame,padding = 10,style='Compass.TFrame')
        self.control_frame_compass.grid(column=0,row=0,sticky=(tk.N, tk.S, tk.E, tk.W))

    
    """
    Create Subframe for PID -local_x
    col-0
    row-1
    """
    def create_control_frame_localX(self):
        self.s.configure('localX.TFrame',background = 'honeydew2')
        self.control_frame_localX = ttk.Frame(self.control_frame,padding = 10,style='localX.TFrame')
        self.control_frame_localX.grid(column=0,row=1,sticky=(tk.N, tk.S, tk.E, tk.W))
    
      
    """
    Create Subframe for PID -local_y
    col-0
    row-2
    """

    def create_control_frame_localY(self):
        self.s.configure('localY.TFrame',background = 'honeydew2')
        self.control_frame_localY = ttk.Frame(self.control_frame,padding = 10,style='localY.TFrame')
        self.control_frame_localY.grid(column=0,row=2,sticky=(tk.N, tk.S, tk.E, tk.W))
    
    
    """
    Create Subframe for Master Control
    col-0
    row-3
    """

    def create_control_frame_master(self):
        self.s.configure('master.TFrame',background = 'gray')
        self.control_frame_master = ttk.Frame(self.control_frame,padding = 10,style='master.TFrame')
        self.control_frame_master.grid(column=0,row=3,sticky=(tk.N, tk.S, tk.E, tk.W))
    
    """
    Create a Frame to hold the Canvas for plotting
    1. Create a style configuration
    2. Add the Tk frame
    3. Place frame using grid manager,row 0,col 2
    4. Add the func back to the init.
    """
    def create_canvas_frame(self):
        self.s.configure('canvas.TFrame',background = 'honeydew2')
        self.canvas_frame = ttk.Frame(self.control_frame,padding = 10,style='canvas.TFrame')
        self.canvas_frame.grid(column=0,row=4,sticky=(tk.N, tk.S, tk.E, tk.W)) 
    
    
    
    """
    Create a Matplot for compass values
    """
    def plotter_compass(self):
        self.compass_fig = Figure(figsize=(4,3),facecolor='white') 
        self.compass_axis = self.compass_fig.add_subplot(111)  
        self.compass_plot = FigureCanvasTkAgg(self.compass_fig,master = self.figure_frame)
        self.compass_plot.get_tk_widget().grid(column=0,row=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.compass_axis.set_title("Compass")

    
    """
    Create a Matplot for X-axis or Local_X values
    """
    def plotter_local_x(self):
        self.local_x = Figure(figsize=(4,3),facecolor='white')
        self.local_x_axis = self.local_x.add_subplot(111)
        
        self.local_x_plot = FigureCanvasTkAgg(self.local_x,master = self.figure_frame)
        self.local_x_plot.get_tk_widget().grid(column=0,row=1,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.local_x_axis.set_title("Local_X")
    
    """
    Create a Matplot for Y-axis or Local_Y values
    """
    def plotter_local_y(self):
        self.local_y = Figure(figsize=(4,3),facecolor='white')
        self.local_y_axis = self.local_y.add_subplot(111)
        self.local_y_plot = FigureCanvasTkAgg(self.local_y,master = self.figure_frame)
        self.local_y_plot.get_tk_widget().grid(column=0,row=2,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.local_y_axis.set_title("Local_Y")

    """
    Create the controllers
    1.include P,I,D
    2. buttons-activate,deactivate
    3. setpoint slider
    """
    def create_controller_for_compass(self):
        #scale for Compass P value
        self.compass_P = tk.Scale(self.control_frame_compass,orient=tk.HORIZONTAL,
                                  length=100,from_=0,to=20.0,
                                  resolution = 0.1,bg='black',fg='white',
                                  command = self.controller.change_compass_P)
        self.compass_P.grid(column=0,row=0)
        #scale for Compass I value
        self.compass_I = tk.Scale(self.control_frame_compass,orient=tk.HORIZONTAL,
                                  length=100,from_=0,to=20.0,
                                  resolution = 0.1,bg='black',fg='white',command = self.controller.change_compass_I)
        self.compass_I.grid(column=0,row=1)
        #scale for Compass D value
        self.compass_D = tk.Scale(self.control_frame_compass,orient=tk.HORIZONTAL,
                                  length=100,from_=0,to=20.0,
                                  resolution = 0.1,bg='black',fg='white',command = self.controller.change_compass_D)
        self.compass_D.grid(column=0,row=2)
        #set point scale for the compass
        self.compass_setpoint = tk.Scale(self.control_frame_compass,orient=tk.HORIZONTAL,
                                  length=100,from_=0,to=360.0,
                                  resolution = 1,bg='black',fg='white',
                                  command=self.controller.change_compass_setpoint)
        
        self.compass_setpoint.grid(column=0,row=3)

        #text for the controls
        compass_P_text = tk.Label(self.control_frame_compass,text = "P",font=(16),bg='honeydew2')
        compass_P_text.grid(row=0,column=1,sticky='ew')

        compass_I_text = tk.Label(self.control_frame_compass,text = "I",font=(16),bg='honeydew2')
        compass_I_text.grid(row=1,column=1,sticky='ew')

        compass_D_text = tk.Label(self.control_frame_compass,text = "D",font=(16),bg='honeydew2')
        compass_D_text.grid(row=2,column=1,sticky='ew')

        compass_setpoint_text = tk.Label(self.control_frame_compass,text = "Angle SP",font=(16),bg='honeydew2')
        compass_setpoint_text.grid(row=3,column=1,sticky='ew')

        #control buttons for activate and deactivate PID control
        self.compass_control_activate = ttk.Button(self.control_frame_compass,
                                                    text="Activate",command = self.controller.compass_DP_ON)
        self.compass_control_activate.grid(row=0,column=2,sticky='ew')

        self.compass_control_deactivate = ttk.Button(self.control_frame_compass,
                                                    text="Deactivate",command=self.controller.compass_DP_OFF)
        self.compass_control_deactivate.grid(row=1,column=2,sticky='ew')

        self.compass_control_status = tk.Label(self.control_frame_compass,text="Status:OFF",fg='red')
        self.compass_control_status.grid(row=2,column=2,sticky='ew')



    """
        The local_x controllers
    """
    def create_controller_for_local_X(self):
        #scale for Compass P value
        self.local_X_P = tk.Scale(self.control_frame_localX,orient=tk.HORIZONTAL,
                                  length=100,from_=0,to=20.0,
                                  resolution = 0.1,bg='black',fg='white',command = self.controller.change_local_x_P)
        self.local_X_P.grid(column=0,row=0)
        #scale for Compass I value
        self.local_X_I = tk.Scale(self.control_frame_localX,orient=tk.HORIZONTAL,
                                  length=100,from_=0,to=20.0,
                                  resolution = 0.1,bg='black',fg='white',command = self.controller.change_local_x_I)
        self.local_X_I.grid(column=0,row=1)
        #scale for Compass D value
        self.local_X_D = tk.Scale(self.control_frame_localX,orient=tk.HORIZONTAL,
                                  length=100,from_=0,to=20.0,
                                  resolution = 0.1,bg='black',fg='white',command = self.controller.change_local_x_D)
        self.local_X_D.grid(column=0,row=2)

        self.local_X_setpoint_text = tk.Label(self.control_frame_localX,text = "SP X:",font=(16),bg='honeydew2')
        self.local_X_setpoint_text.grid(row=3,column=0,sticky='ew')
        # #set point scale for the compass
        # self.local_X_setpoint = tk.Button(self.control_frame_localX,orient=tk.HORIZONTAL,
        #                           length=100,from_=0,to=360.0,
        #                           resolution = 1,bg='black',fg='white')
        # self.local_X_setpoint.grid(column=0,row=3)

        #text for the controls
        local_X_P_text = tk.Label(self.control_frame_localX,text = "P",font=(16),bg='honeydew2')
        local_X_P_text.grid(row=0,column=1,sticky='ew')

        local_X_I_text = tk.Label(self.control_frame_localX,text = "I",font=(16),bg='honeydew2')
        local_X_I_text.grid(row=1,column=1,sticky='ew')

        local_X_D_text = tk.Label(self.control_frame_localX,text = "D",font=(16),bg='honeydew2')
        local_X_D_text.grid(row=2,column=1,sticky='ew')

        

        #control buttons for activate and deactivate PID control
        self.local_X_control_activate = ttk.Button(self.control_frame_localX,
                                                    text="Activate",command = self.controller.local_x_DP_ON)
        self.local_X_control_activate.grid(row=0,column=2,sticky='ew')

        self.local_X_control_deactivate = ttk.Button(self.control_frame_localX,
                                                    text="Deactivate",command = self.controller.local_x_DP_OFF)
        self.local_X_control_deactivate.grid(row=1,column=2,sticky='ew')

        self.local_X_control_status = tk.Label(self.control_frame_localX,text="Status:OFF",fg='red')
        self.local_X_control_status.grid(row=2,column=2,sticky='ew')

        self.local_X_control_current_X = tk.Label(self.control_frame_localX,text="Current X:",fg='red')
        self.local_X_control_current_X.grid(row=3,column=2,sticky='ew')

    
    def create_controller_for_local_Y(self):
        #scale for Compass P value
        self.local_Y_P = tk.Scale(self.control_frame_localY,orient=tk.HORIZONTAL,
                                  length=100,from_=0,to=20.0,
                                  resolution = 0.1,bg='black',fg='white',command = self.controller.change_local_y_P)
        self.local_Y_P.grid(column=0,row=0)
        #scale for Compass I value
        self.local_Y_I = tk.Scale(self.control_frame_localY,orient=tk.HORIZONTAL,
                                  length=100,from_=0,to=20.0,
                                  resolution = 0.1,bg='black',fg='white',command = self.controller.change_local_y_I)
        self.local_Y_I.grid(column=0,row=1)
        #scale for Compass D value
        self.local_Y_D = tk.Scale(self.control_frame_localY,orient=tk.HORIZONTAL,
                                  length=100,from_=0,to=20.0,
                                  resolution = 0.1,bg='black',fg='white',command = self.controller.change_local_y_D)
        self.local_Y_D.grid(column=0,row=2)

        self.local_Y_setpoint_text = tk.Label(self.control_frame_localY,text = "SP Y:",font=(16),bg='honeydew2')
        self.local_Y_setpoint_text.grid(row=3,column=0,sticky='ew')
        # #set point scale for the compass
        # self.local_X_setpoint = tk.Button(self.control_frame_localX,orient=tk.HORIZONTAL,
        #                           length=100,from_=0,to=360.0,
        #                           resolution = 1,bg='black',fg='white')
        # self.local_X_setpoint.grid(column=0,row=3)

        #text for the controls
        local_Y_P_text = tk.Label(self.control_frame_localY,text = "P",font=(16),bg='honeydew2')
        local_Y_P_text.grid(row=0,column=1,sticky='ew')

        local_Y_I_text = tk.Label(self.control_frame_localY,text = "I",font=(16),bg='honeydew2')
        local_Y_I_text.grid(row=1,column=1,sticky='ew')

        local_Y_D_text = tk.Label(self.control_frame_localY,text = "D",font=(16),bg='honeydew2')
        local_Y_D_text.grid(row=2,column=1,sticky='ew')

        

        #control buttons for activate and deactivate PID control
        self.local_Y_control_activate = ttk.Button(self.control_frame_localY,
                                                    text="Activate",command = self.controller.local_y_DP_ON)
        self.local_Y_control_activate.grid(row=0,column=2,sticky='ew')

        self.local_Y_control_deactivate = ttk.Button(self.control_frame_localY,
                                                    text="Deactivate",command = self.controller.local_y_DP_OFF)
        self.local_Y_control_deactivate.grid(row=1,column=2,sticky='ew')

        self.local_Y_control_status = tk.Label(self.control_frame_localY,text="Status:OFF",fg='red')
        self.local_Y_control_status.grid(row=2,column=2,sticky='ew')

        self.local_Y_control_current_Y = tk.Label(self.control_frame_localY,text="Current X:",fg='red')
        self.local_Y_control_current_Y.grid(row=3,column=2,sticky='ew')
    
    
    def create_controller_for_master(self):
        self.master_controller_stop = tk.Button(self.control_frame_master,text="Deactivate All DP",command = self.controller.deactivate_all_dp_systems)
        self.master_controller_stop.grid(row=0,column=1,sticky='ew')

        self.master_controller_on = tk.Button(self.control_frame_master,text="Activate All DP",command = self.controller.activate_all_dp_systems)
        self.master_controller_on.grid(row=0,column=0,sticky='ew')

        self.master_controller_arm = tk.Button(self.control_frame_master,text="ARM",command = self.controller.arming_via_mavros)
        self.master_controller_arm.grid(row=0,column=2,sticky='ew')
        
        self.master_controller_disarm = tk.Button(self.control_frame_master,text="DISARM",command =self.controller.disarm_via_mavros)
        self.master_controller_disarm.grid(row=0,column=3,sticky='ew')


    def create_canvas_for_path(self):
        self.canvas_path_plot = tk.Canvas(self.canvas_frame,width=400,height=330,bg='white')
        self.canvas_path_plot.grid(row=0,column=0,sticky='nsew')
              
  
    def main(self):
        
        self.mainloop()




   