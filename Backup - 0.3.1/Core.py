#-*- coding:utf-8 -*-

import threading as td
import socket    as line
import time

__verson__ = '0.3.1'

'''Don't ask me why I write like this, I just like this style.'''

def HostIP():
    try:
        s = line.socket(line.AF_INET, line.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

class Execute(td.Thread):
    def __init__(self, cli, **kwargs):
        td.Thread.__init__(self)
        self.alive = True
        self.cli = cli
        self.kw = kwargs

    def run(self):
        ''' Used to process requests '''
        while True:
            # The client exited unexpectedly
            try:
                data = self.cli.recv(128).decode("utf-8")
            except:
                data = '<disconnect>'
            if data == '<disconnect>':
                self.cli.close()
                break
            if data == '<alive>':
                self.cli.send('<True>'.encode('utf-8'))
                continue
            
        self.alive = False

class Network:
    Blacklog = 20
    InspectionFreq = 5

    def __init__(self, port, token, ):
        self.token = token
        self.__port = port
        self.__Terminal = {'con':{},'net':{}}
        self.__acce = line.socket(line.AF_INET, line.SOCK_STREAM)
        self.__acce.bind((HostIP(),self.__port))
        self.__TCP = td.Thread(target=self.__Accept)
        self.__TCP.start()
        self.__ats = td.Timer(0, self.__Abnormal)
        self.__ats.start()
    
    def OPED(self, ip, state):
        if not ip in self.__Terminal['con']:
            return False
        self.__Terminal['con'][ip]['use'] = state
        return True
    
    def Alive(self, ip):
        ''' Used to check connection survivability '''
        if not ip in self.__Terminal['con']:
            return False
        
        if self.__Terminal['con'][ip]['use'] == True:
            return True

        self.OPED(ip, True)
        try:
            self.__Terminal['con'][ip]['exa'].send('<alive>'.encode('utf-8'))
            self.__Terminal['con'][ip]['exa'].recv(16).decode("utf-8")
            self.OPED(ip, False)
            return True
        except:
            self.__Terminal['con'][ip]['exa'].close()
            del self.__Terminal['con'][ip]
            return False 
        
    def __Abnormal(self):
        # The server exited unexpectedly
        for ip in list(self.__Terminal['con'].keys()):
            self.Alive(ip)
        time.sleep(self.InspectionFreq)
        self.__ats = td.Timer(0, self.__Abnormal)
        self.__ats.start()
    
    def __Detection(self, ip):
        ''' Used to receive feedback from threads '''
        exe = Execute(self.__Terminal['net'][ip])
        exe.run()
        while True:
            if exe.alive == False:
                break
        del self.__Terminal['net'][ip]

    def __Accept(self):
        ''' Used to process connection requests '''
        self.__acce.listen(self.Blacklog)
        while True:
            cli, addr = self.__acce.accept()
            token = cli.recv(256).decode('utf-8')
            if len(self.token) > 256:
                cli.send('<ServerError>'.encode("utf-8"))
                cli.close()
                continue
            if token != self.token:
                cli.send('<TokenError>'.encode("utf-8"))
                cli.close()
                continue
            cli.send('<Accepted>'.encode("utf-8"))
            self.__Terminal['net'][addr[0]] = cli

            td.Thread(target=self.__Detection, args=(addr[0],)).start()
    
    def Connect(self, addr, token):
        ''' Used to connect to the target node '''
        if type(addr) == dict:
            addr = (addr['ip'],addr['port'])
        cli = line.socket(line.AF_INET, line.SOCK_STREAM)
        try:
            cli.connect(addr)
        except:
            return '<IPError>'
        cli.send(token.encode("utf-8"))
        rezult = cli.recv(64).decode('utf-8')
        if 'Error' in rezult:
            cli.close()
            return rezult
        self.__Terminal['con'][addr[0]] = {'exa':cli,'use':False}
        return True
    
    def Dis(self, ip):
        ''' Used to disconnect from the target node '''
        if not self.Alive(ip):
            return False

        self.OPED(ip, True)
        exa = self.__Terminal['con'][ip]['exa']
        exa.send('<disconnect>'.encode('utf-8'))
        exa.close()
        self.OPED(ip, False)

        del self.__Terminal['con'][ip]
        return True
    
    def File(self):
        print(self.__Terminal['con'])

a = Network(1010, 'F6987ij42')

rz = a.Connect({'ip':HostIP(),'port':1030,'name':'A03HCY_Aiden'}, 'F6987ij42')
print(rz)

print(a.Alive(HostIP()))

while True:
    input('>>> ')
    a.File()