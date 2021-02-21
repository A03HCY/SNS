from Core import *
import sys

__verson__ = '0.1.2'

class Runner(Network):
    Contin = True
    t_id = None

    def __init__(self, port, token):
        super().__init__(port, token)
        pass

    def Getcmd(self):
        head = self.t_id
        if self.t_id == None:
            head = 'Terminal'
        else:
            head = head.split('-')[0]
        print(head+' # ', end='')
        cmd  = []
        for part in input('').split(' '):
            for final in part.split(':'):
                cmd.append(final)
        return cmd

    def run(self):
        while self.Contin:
            cmd = self.Getcmd()
            if cmd[0] in ['sns'] and len(cmd) == 3:
                ip = cmd[1]
                try:port = int(cmd[2])
                except:continue
                token = input('Token > ')
                rs = self.Connect((ip, port), token)
                if 'Error' in rs:
                    print(rs)
                    continue
                self.t_id = rs
            if cmd[0] in ['ter']:
                ter = self.GetTerminal()
                for key in ter:
                    print(key + ':', end=' ')
                    if ter[key] == []:
                        print('None')
                        continue
                    print('')
                    for value in ter[key]:
                        print('    ' + value)
                    

a = Runner(1010, 'F6987ij42')
a.run()