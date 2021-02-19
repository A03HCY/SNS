#-*- coding:utf-8 -*-

import threading as td
import socket    as line
import os
import shutil
import json
import time
import datetime
import random

__verson__ = '0.4.3'

'''Don't ask me why I write like this, I just like this style.'''

def Rmtree(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def Ranstr(num):
    ran_str = ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', num))
    return ran_str

def HostIP():
    try:
        s = line.socket(line.AF_INET, line.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def Sizeset(B):
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2)
   GB = float(KB ** 3)
   TB = float(KB ** 4)
   if B < KB:
      return '{0} {1}'.format(B,'B' if 0 == B > 1 else 'B')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)

class Cbar:
    char = '█'
    text = '\r|{b}| {done}/{size} [{sp} {ft} eta {dt}]'

    def __init__(self, size, head, lon=50):
        self.time = time.time()
        self.start = time.time()
        self.done = 0
        self.size = size
        self.lon = lon
        self.head = head
        print(' '+head)
    
    def info(self, done):
        eta = datetime.timedelta(seconds=int(time.time()-self.start))
        cent = (done/self.size)
        tex = self.char*int(self.lon*cent) + ' '*(self.lon-int(self.lon*cent))
        try:spd = int((done - self.done) / (time.time() - self.time))
        except:return
        ftd = datetime.timedelta(seconds=int((self.size - done) / spd))
        spd = Sizeset(spd)
        self.done = done
        self.time = time.time()
        size = Sizeset(self.size)
        done = Sizeset(done)
        done = ' '*(len(size)-len(done)) + done
        spd = ' '*(8-len(spd)) + spd

        print(self.text.format(b=tex,done=done, size=size, ft=ftd, sp=spd+'/s', dt=eta), end='')
    
    def done(self, text):
        print('')
        print(text)

def Recv(clint, head, bar=None):
    size = 0
    mode = 'wb'
    sizeValue = int(head['size'])
    if os.path.exists(head['path']+'.ftmp') == True:
        size = os.path.getsize(head['path']+'.ftmp')
        mode = 'ab'
    clint.send(str(size).encode('utf-8'))
    tim = time.time()
    with open(head['path']+'.ftmp', mode) as file:
        while size < sizeValue:
            value = sizeValue - size
            # Prevent the exception caused by connection interruption
            try:
                if value > 1024:
                    getdate = clint.recv(1024)
                else :
                    getdate = clint.recv(value)
            except:
                print('')
                time.sleep(0.01)
                return False
            file.write(getdate)
            size += 1024
            if bar:
                if time.time() - tim >=0.5:
                    tim = time.time()
                    bar.info(size)
    if bar:
        bar.info(size)
        print('')
        time.sleep(0.01)
    os.rename(head['path']+'.ftmp', head['path'])
    return True

def Send(clint, path, bar=None):
    daze = os.path.getsize(path)
    size = int(clint.recv(1024).decode('utf-8'))
    tim = time.time()
    with open(path, 'rb') as file:
        file.seek(size)
        while size < daze:
            fileDate = file.read(1024)
            # Prevent the exception caused by connection interruption
            try:
                clint.send(fileDate)
            except:return False
            size += 1024
            if bar:
                if time.time() - tim >=0.5:
                    tim = time.time()
                    bar.info(size)
    if bar:
        bar.info(size)
        print('')
        time.sleep(0.01)
    return True

def listdir(path):
    if os.path.exists(path) == True:
        dat = {"files":[],"folders":[],"unknows":[]}
        for i in os.listdir(path):
            if os.path.isdir(path + i) == True:
                dat["folders"].append(i)
            elif os.path.isfile(path + i) == True:
                dat["files"].append(i)
            else:
                dat["unknows"].append(i)
        return dat

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
            if data == '<Get_Flie>':
                path = self.cli.recv(1024).decode("utf-8")
                if os.path.exists(path) == False or os.path.split(path)[1] == '':
                    self.cli.send('<Error>'.encode('utf-8'))
                    continue
                size = os.path.getsize(path)
                self.cli.send(str(size).encode('utf-8'))
                Send(self.cli, path)
                continue
            if data == '<Send_File>':
                path = self.cli.recv(1024).decode("utf-8")
                if os.path.split(path)[1] == '':
                    self.cli.send('<Error>'.encode('utf-8'))
                    continue
                if os.path.exists(os.path.split(path)[0]) == False:
                    os.makedirs(os.path.split(path)[0])
                self.cli.send('<True>'.encode('utf-8'))
                size = self.cli.recv(1024).decode("utf-8")
                if os.path.exists(path) == True:
                    tic = 1
                    while True:
                        filen = os.path.splitext(os.path.split(path)[1])
                        path = os.path.split(path)[0] + filen[0] + '({tic})'.format(tic=tic) + filen[1]
                        if os.path.exists(path) == False:
                            break
                        tic += 1
                head = {}
                head['path'] = path
                head['size'] = int(size)
                Recv(self.cli, head)
                continue
            if data == '<List_File>':
                path = self.cli.recv(1024).decode("utf-8")
                if os.path.isdir(path) == False:
                    self.cli.send('<Error>'.encode('utf-8'))
                    continue
                data = listdir(path)
                self.cli.send(json.dumps(data).encode('utf-8'))
                continue
            if data == '<Stat>':
                path = self.cli.recv(1024).decode("utf-8")
                if os.path.isfile(path) == False:
                    self.cli.send('<Error>'.encode('utf-8'))
                    continue
                head = ['mode','ino','dev','nlink','uid','gid','size','atime','mtime','ctime']
                data = os.stat(path)
                data = zip(head, data)
                self.cli.send(json.dumps(dict(data)).encode('utf-8'))
                continue
            if data == '<Rename>':
                data = self.cli.recv(2048).decode('utf-8')
                data = json.loads(data)
                try:
                    os.rename(data['before'], data['after'])
                    self.cli.send('<True>'.encode('utf-8'))
                except:
                    self.cli.send('<Error>'.encode('utf-8'))
                continue
            if data == '<Remove>':
                path = self.cli.recv(1024).decode("utf-8")
                if os.path.exists(path) == False:
                    self.cli.send('<Error>'.encode('utf-8'))
                try:os.remove(path)
                except:
                    try:
                        Rmtree(path)
                        os.rmdir(path)
                    except:pass
                self.cli.send('<True>'.encode('utf-8'))
                continue
            if data == '<Copy>':
                data = self.cli.recv(2048).decode('utf-8')
                data = json.loads(data)
                if os.path.exists(data['before']) == False:
                    self.cli.send('<Error>'.encode('utf-8'))
                try:
                    if os.path.isdir(data['before']):
                        if os.path.abspath(data['before']) == os.path.abspath(data['after']):
                            self.cli.send('<Error>'.encode('utf-8'))
                            continue
                        if os.path.exists(data['after']):
                            shutil.rmtree(data['after'])
                        shutil.copytree(data['before'],data['after']) 
                    elif os.path.isfile(data['before']):
                        af = os.path.join(os.path.split(data['after'])[0],os.path.split(data['before'])[1])
                        shutil.copyfile(data['before'],af) 
                    self.cli.send('<True>'.encode('utf-8'))
                except:
                    self.cli.send('<Error>'.encode('utf-8'))
                continue
            if data == '<Move>':
                data = self.cli.recv(2048).decode('utf-8')
                data = json.loads(data)
                if os.path.exists(data['before']) == False:
                    self.cli.send('<Error>'.encode('utf-8'))
                try:
                    if os.path.isdir(data['before']):
                        shutil.move(data['before'],data['after']) 
                    elif os.path.isfile(data['before']):
                        af = os.path.join(os.path.split(data['after'])[0],os.path.split(data['before'])[1])
                        shutil.move(data['before'],af)
                    self.cli.send('<True>'.encode('utf-8'))
                except:
                    self.cli.send('<Error>'.encode('utf-8'))
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
    
    def GetTerminal(self):
        Terminal = {'con':[],'net':[]}
        Terminal['con'] = list(self.__Terminal['con'].keys())
        Terminal['net'] = list(self.__Terminal['net'].keys())
        return Terminal
    
    def OPED(self, code, state):
        if not code in self.__Terminal['con']:
            return False
        self.__Terminal['con'][code]['use'] = state
        return True
    
    def Alive(self, code):
        ''' Used to check connection survivability '''
        if not code in self.GetTerminal()['con']:
            return False
        
        if self.__Terminal['con'][code]['use'] == True:
            return True

        self.OPED(code, True)
        try:
            self.__Terminal['con'][code]['exa'].send('<alive>'.encode('utf-8'))
            self.__Terminal['con'][code]['exa'].recv(16).decode("utf-8")
            self.OPED(code, False)
            return True
        except:
            self.__Terminal['con'][code]['exa'].close()
            del self.__Terminal['con'][code]
            return False 
        
    def __Abnormal(self):
        # The server exited unexpectedly
        for code in list(self.__Terminal['con'].keys()):
            self.Alive(code)
        time.sleep(self.InspectionFreq)
        self.__ats = td.Timer(0, self.__Abnormal)
        self.__ats.start()
    
    def __Detection(self, code):
        ''' Used to receive feedback from threads '''
        exe = Execute(self.__Terminal['net'][code])
        exe.run()
        while True:
            if exe.alive == False:
                break
        del self.__Terminal['net'][code]

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
            ran = Ranstr(6)
            self.__Terminal['net'][addr[0]+'-'+ran] = cli

            td.Thread(target=self.__Detection, args=(addr[0]+'-'+ran,)).start()
    
    def Connect(self, addr, token=None):
        ''' Used to connect to the target node '''
        if type(addr) == dict:
            addr = (addr['ip'],addr['port'])
        cli = line.socket(line.AF_INET, line.SOCK_STREAM)
        try:
            cli.connect(addr)
        except:
            return '<IPError>'
        if token == None or token.strip(' ') == '':
            token = '<Astst>'
        cli.send(token.encode("utf-8"))
        rezult = cli.recv(64).decode('utf-8')
        if 'Error' in rezult:
            cli.close()
            return rezult
        ran = Ranstr(6)
        self.__Terminal['con'][addr[0]+'-'+ran] = {'exa':cli,'use':False}
        return addr[0]+'-'+ran
    
    def Dis(self, code):
        ''' Used to disconnect from the target node '''
        if not self.Alive(code):
            return False
        if self.__Terminal['con'][code]['use'] == True:
            return False
        
        self.OPED(code, True)
        exa = self.__Terminal['con'][code]['exa']
        exa.send('<disconnect>'.encode('utf-8'))
        exa.close()

        del self.__Terminal['con'][code]
        return True
    
    def Disall(self):
        code = self.GetTerminal()['con']
        for i in code:self.Dis(i)
        return True
    
    def Command(self, code):
        if not self.Alive(code):
            return False
        self.OPED(code, True)
        exa = self.__Terminal['con'][code]['exa']
        self.OPED(code, False)
    
    def File(self, code, cmd, local='', cloud=''):
        if not self.Alive(code):
            return False
        
        self.OPED(code, True)
        exa = self.__Terminal['con'][code]['exa']
        if cmd == 'get':
            if local == '' or cloud == '':
                return '<PathError>'
            exa.send('<Get_Flie>'.encode('utf-8'))
            exa.send(cloud.encode('utf-8'))
            size = exa.recv(1024).decode('utf-8')
            if 'Error' in size:
                return size
            head = {}
            head['size'] = int(size)
            head['path'] = os.path.split(local)[0] + os.path.split(cloud)[1]
            if os.path.exists(head['path']) == True:
                tic = 0
                while True:
                    tic += 1
                    filen = os.path.splitext(os.path.split(cloud)[1])
                    head['path'] = os.path.split(local)[0] + filen[0] + '({tic})'.format(tic=tic) + filen[1]
                    if os.path.exists(head['path']) == False:
                        break
            if os.path.exists(os.path.split(local)[0]) == False:
                os.makedirs(os.path.split(local)[0], 755)
            bar = Cbar(int(head['size']), os.path.split(head['path'])[1])
            rz = Recv(exa, head, bar)
            self.OPED(code, False)
            return rz
        if cmd == 'send':
            if local == '' or cloud == '' or os.path.exists(local) != True:
                return '<PathError>'
            try:
                size = os.path.getsize(local)
            except:
                return '<PathError>'
            cloud = os.path.split(cloud)[0] + os.path.split(local)[1]
            exa.send('<Send_File>'.encode('utf-8'))
            exa.send(cloud.encode('utf-8'))
            answer = exa.recv(128).decode('utf-8')
            if answer != '<True>':
                return answer
            exa.send(str(size).encode('utf-8'))
            bar = Cbar(size, os.path.split(local)[1])
            rz = Send(exa, local, bar)
            self.OPED(code, False)
            return rz
        if cmd == 'list' or cmd == 'stat':
            if cloud == '':
                return '<PathError>'
            if cmd == 'list':
                mode = '<List_File>'
            elif cmd == 'stat':
                mode = '<Stat>'
            
            exa.send(mode.encode('utf-8'))
            exa.send(cloud.encode('utf-8'))
            data = exa.recv(2048).decode('utf-8')
            if data == '<Error>':
                return False
            data = json.loads(data)
            self.OPED(code, False)
            return data
        if cmd == 'copy':
            pass

        self.OPED(code, False)
    
    def Cloud(self, code, cmd, local='', cloud=''):
        if not self.Alive(code):
            return False
        self.OPED(code, True)
        exa = self.__Terminal['con'][code]['exa']
        if cmd == 'rename' or cmd == 'copy' or cmd == 'move':
            if local == '' or cloud == '':
                return '<PathError>'
            if cmd == 'copy':
                cmd = '<Copy>'
            elif cmd == 'rename':
                cmd = '<Rename>'
            elif cmd == 'move':
                cmd = '<Move>'
            exa.send(cmd.encode('utf-8'))
            data = {'before':local,'after':cloud}
            exa.send(json.dumps(data).encode('utf-8'))
            rz = exa.recv(128).decode('utf-8')
            self.OPED(code, False)
            if rz == '<True>':
                return True
            else:return False
        if cmd == 'remove':
            if cloud == '':
                return '<PathError>'
            exa.send('<Remove>'.encode('utf-8'))
            exa.send(cloud.encode('utf-8'))
            rz = exa.recv(128).decode('utf-8')
            self.OPED(code, False)
            if rz == '<True>':
                return True
            else:return False

        self.OPED(code, False)
    



a = Network(1010, 'F6987ij42')

rz = a.Connect({'ip':HostIP(),'port':1010,'name':'A03HCY'}, 'F6987ij42')
# rz = a.Connect((HostIP(),1010), 'F6987ij42')

print(rz)
print(a.GetTerminal())
print(a.Alive(rz))

while True:
    try:exec(input('>>> '))
    except:pass

if False:
    a.File(rz, 'get', 'L:\\', 'I:\\BilibiliOS.7z')
    a.File(rz, 'send', 'I:\\BilibiliOS.7z', 'L:\\')
    a.File(rz, 'list', '', 'K:\\')
    a.File(rz, 'stat', '', 'K:\\main.cpp')
    a.Cloud(rz, 'rename', 'K:\\b', 'K:\\c')
    a.Cloud(rz, 'remove', '', 'K:\\c')
    a.Cloud(rz, 'move', 'K:\\tkinter-designer-master\\', 'K:\\tkinter-designer-master\\')
    a.Cloud(rz, 'copy', 'K:\\J\\', 'K:\\J')
