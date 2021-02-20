from Core import *
import sys

__verson__ = '0.1.2'

class Runner(Network):
    t_id = None

    def __init__(self, port, token):
        super().__init__(port, token)
        pass

    def Getcmd(self):
        print('Terminal # ')
        return

    def run(self):
        pass

a = Runner(1010, 'F6987ij42')
a.run()