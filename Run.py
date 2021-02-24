from Core import *
import sys

__verson__ = '0.1.2'

class Runner(Network):
    Contin = True
    t_id = None
    t_pt = None

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
    
    def simplifyPath(self, path):
        path.replace('//', '/')
        path.replace('\\', '/')
        list = path.split('/')
        res =[]
        for i in range(len(list)):
            if list[i] == '..' and len(res) > 0:
                res = res[:-1]
            elif list[i] != '' and list[i] != '.' and list[i] != '..':
                res.append(list[i])
        return '/'+'/'.join(res)

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
                self.t_pt = input('Folder > ')
                self.t_id = rs
                continue
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
                continue
            if cmd[0] in ['ls']:
                rz = self.File(self.t_id, 'list', '', self.t_pt)
                if 'Error' in rz:
                    print(rz)
                    continue
                for part in rz:
                    if rz[part] == []:
                        continue
                    print(part+':')
                    for files in rz[part]:print('  '+files)
                continue

            if cmd[0] in ['cd']:
                rz = self.File(self.t_id, 'list', '', self.t_pt)
                if 'Error' in rz:
                    self.t_pt = input('Reset Path > ')
                    continue
                if rz['folders'] == []:
                    print('No folder can change.')
                    stay = input('Up folder? > ')
                    if stay in ['yes', 'y']:
                        self.t_pt = os.path.join(self.t_pt, '/..')
                        self.t_pt = self.simplifyPath(self.t_pt)[1:]
                        print(self.t_pt)
                    continue
                print('folders:')
                i = 1
                for part in rz['folders']:
                    print(' '+str(i)+' '+part)
                    i += 1
                cmd = int(input('Number > '))
                if cmd == 0:
                    self.t_pt = os.path.join(self.t_pt, '/..')
                    self.t_pt = self.simplifyPath(self.t_pt)[1:]
                    continue
                if rz['folders'][cmd-1]:
                    self.t_pt = os.path.join(self.t_pt, rz['folders'][cmd-1])
                    self.t_pt = self.simplifyPath(self.t_pt)[1:]
                print(self.t_pt)
                continue
            if cmd[0] in ['get']:
                rz = self.File(self.t_id, 'list', '', self.t_pt)
                if 'Error' in rz:
                    self.t_pt = input('Reset Path > ')
                    continue
                if rz['files'] == [] and rz['unknows'] == []:
                    print('No Files.')
                    continue
                fun = rz['files'] + rz['unknows']
                print('Files and unknows:')
                i = 1
                for part in fun:
                    print(' '+str(i)+' '+part)
                    i += 1
                cmd = int(input('Number > '))
                if fun[cmd-1]:
                    download = os.path.join(self.t_pt, fun[cmd-1]).replace('\\', '/')
                    download = download.replace('/', '\\')
                    print(download)
                    rz = self.File(self.t_id, 'get', './', download)
                    print(rz)


                
                    

a = Runner(1010, 'F6987ij42')
a.t_id = a.Connect(('192.168.1.8', 1010), 'F6987ij42')
a.t_pt = 'x:/'
a.run()