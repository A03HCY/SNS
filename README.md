# Miniature Network System
简单的文件数据传输 - Simple file data transfer  ( ? )

> 整个代码中会有许多不规范/不简洁/不合理的写法，以后会慢慢修改的（咕咕咕）
>
> Backup 仅仅是为了避免不可抗因素带来的灾难而做的备份，请小心参考（雾）



## Network

```python
class Network:
    def __init__(self, port, token):
        pass
    
    def GetTerminal(self):
        return
    
    def OPED(self, code, state):
        return
    
    def Alive(self, code):
        return
    
    def Connect(self, addr, token=None):
        return
    
    def Dis(self, code):
        return
    
    def Disall(self):
        return
    
    def File(self, code, cmd, local='', cloud=''):
        return
    
    def Cloud(self, code, cmd, local='', cloud=''):
        return
```

------

### init (self, port, token)

| 参数  |               解释                |   类型   |
| :---: | :-------------------------------: | :------: |
| port  |       供其他节点连接的端口        | int 必填 |
| token | 节点连接时需要提供的token（密码） | str 必填 |

```python
exam = Network(1010, 'ABCd-e254#6')
```

------

### Connect (self, addr, token=None)

| 参数  |               解释                |      类型       |
| :---: | :-------------------------------: | :-------------: |
| addr  |            连接的地址             | dict/tuple 必填 |
| token | 节点连接时需要提供的token（密码） |    str 选填     |

```python
addr = ('127.0.0.1', 1010)
addr = {'ip':'127.0.0.1','port':1010}
token = 'ABCd-e254#6'

rz = exam.Connect(addr,token)
# 返回 {ip}-{6位随机字符串}
print(rz) # 127.0.0.1-F9mo6V
```

