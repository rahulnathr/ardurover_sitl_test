#!/usr/bin/env python


# from dp_view import View
# 
from dp_view import View
from dp_model import Model
class Controller(object):
    def __init__(self):
        self.view = View()
        self.model = Model()



if __name__ == "__main__":
    app = Controller()
    app.view.main()