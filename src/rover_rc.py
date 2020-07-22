import tkinter as tk
from tkinter import ttk

class View(tk.Tk):
    """The GUI View of the application"""
    def __init__(self,controller):
        super().__init__()
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
        self.createMission1()
    def createLeftFrame(self):
        self.s.configure('Frame2.TFrame',background='light gray')
        self.leftframe = ttk.LabelFrame(self.content, text='Controls',style='Frame2.TFrame')
        self.leftframe.grid(column=0,row=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        self.leftframe.rowconfigure(0,weight=1)
        self.leftframe.rowconfigure(1,weight=1)



    def createRightFrame(self):
        self.s.configure('Frame3.TFrame',background='light gray')
        self.rightframe = ttk.LabelFrame(self.content, text='Canvas', style='Frame3.TFrame')
        self.rightframe.grid(column=1, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    def createCanvas(self):
        self.canvas_plot = tk.Canvas(self.rightframe,bg='white',height=500,width =350)
        self.canvas_plot.grid(row=0,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))

    def createButton1Layer(self):
        self.button_one_layer = tk.Frame(self.leftframe,bg = 'gray')
        self.button_one_layer.grid(row=0,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))

    def createButton2Layer(self):
        self.button_two_layer = tk.Frame(self.leftframe, bg='white')
        self.button_two_layer.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    def createMission1(self):
        self.labelx = tk.Label(self.button_one_layer,text='X')
        self.labelx.grid(row=0,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.labely = tk.Label(self.button_one_layer,text='Y')
        self.labely.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.labelsentx = tk.Label(self.button_one_layer, text='Sent X')
        self.labelsentx.grid(row=0, column=3, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.labelsenty = tk.Label(self.button_one_layer, text='Sent Y')
        self.labelsenty.grid(row=0, column=4, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.entryx = tk.Entry(self.button_one_layer)
        self.entryx.grid(row=1,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.entryy = tk.Entry(self.button_one_layer)
        self.entryy.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.sentbtn = tk.Button(self.button_one_layer,text="Send Values")
        self.sentbtn.grid(row=1,column=2,sticky=(tk.N, tk.S, tk.E, tk.W))

        self.labelgotx = tk.Label(self.button_one_layer, text='Got X')
        self.labelgotx.grid(row=1, column=3, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.labelgoty = tk.Label(self.button_one_layer, text='Got Y')
        self.labelgoty.grid(row=1, column=4, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.go_button = tk.Button(self.button_one_layer,text="Start Mission")
        self.go_button.grid(row=2,column=0,sticky=(tk.N, tk.S, tk.E, tk.W))

        self.progress_bar = ttk.Progressbar(self.button_one_layer,mode='determinate',orient=tk.HORIZONTAL)
        self.progress_bar.grid(row =2,column=1,columnspan=4,sticky=(tk.N, tk.S, tk.E, tk.W))


    def main(self):
        self.mainloop()
