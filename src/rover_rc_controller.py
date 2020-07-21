from rover_rc import View

class Controller:
    def __init__(self):
        self.view = View(self)



if __name__ == "__main__":
    app = Controller()
    app.view.mainloop()