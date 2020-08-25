#!/usr/bin/env python


# from dp_view import View
# 
from dp_view import View

class Controller(object):
    def __init__(self):
        self.view = View()




if __name__ == "__main__":
    app = Controller()
    app.view.main()