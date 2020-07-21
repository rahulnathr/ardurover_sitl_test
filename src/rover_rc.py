import tkinter as tk
from tkinter import ttk

class View(tk.Tk):
    """The GUI View of the application"""
    def __init__(self):

        super().init()



        self.title("Way Point Plotter")
        self.geometry("800x600")
        self.s = ttk.Style()
        self.s.configure('TFrame',background ='white')

        
    def main(self):
        self.mainloop()
