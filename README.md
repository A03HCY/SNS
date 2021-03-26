# Miniature Network System
简单的文件数据传输 - Simple file data transfer

> 整个代码中会有许多不规范/不简洁/不合理的写法，以后会慢慢修改的（咕咕咕）
>
> Backup 仅仅是为了避免不可抗因素带来的灾难而做的备份，请小心参考（雾）

## Network

可以使用的函数

```python
class Network:
    def __init__(self, port, token):
        pass
    
    def GetTerminal(self):
        # 获取连接与被连接的设备的code
        return
    
    def Alive(self, code):
        # 检查连接是否存活
        return
    
    def Connect(self, addr, token=None):
        # 连接到设备
        return
    
    def Dis(self, code):
        # 断开主动的连接
        return
    
    def Disall(self):
        # 断开所有主动的连接
        return
    
    def File(self, code, cmd, local='', cloud=''):
        # 对本地与云端文件及目录的操作
        return
    
    def Cloud(self, code, cmd, local='', cloud=''):
        # 对云端文件与目录的操作
        return
```
  
### 创建一个实例

| 参数  |               解释                |   类型   |
| :---: | :-------------------------------: | :------: |
| port  |       供其他节点连接的端口        | int 必填 |
| token | 节点连接时需要提供的token（密码） | str 必填 |
  
```python
exam = Network(1010, 'ABCd-e254#6')
```
  
### 连接到设备

| 参数  |               解释                |      类型       |
| :---: | :-------------------------------: | :-------------: |
| addr  |          连接的IPv4地址           | dict/tuple 必填 |
| token | 节点连接时需要提供的token（密码） |    str 选填     |
  

```python
addr = ('127.0.0.1', 1010)
addr = {'ip':'127.0.0.1','port':1010}
token = 'ABCd-e254#6'

code = exam.Connect(addr,token)
# 返回 {ip}-{6位随机字符串}
print(code) # 127.0.0.1-F9mo6V
```
  
| 返回 |          解释          | 类型 |
| :--: | :--------------------: | :--: |
| code | 在进行其他操作时需提供 | str  |
  

### 检查连接存活

| 参数 |     解释     |  类型   |
| :--: | :----------: | :-----: |
| code | 被检查的连接 | str必填 |
  
```python
rz = a.Alive(code)
print(code) # True / False
```
  
| 返回 |   解释   | 类型 |
| :--: | :------: | :--: |
| stat | 存活状态 | bool |
  
当被检查的连接并不存活时，会自动断开并删除这个连接，要继续下面的操作必修重新进行连接
  
### 本地与云端的操作
  
| 命令 |            解释            | code |   local目录    |   cloud目录    | 返回 |
| :--: | :------------------------: | :--: | :------------: | :------------: | :--: |
| get  |       获取文件到本地       | 需要 | 保存文件的目录 |  目标文件目录  | bool |
| send |       发送文件到云端       | 需要 |  目标文件目录  | 保存文件的目录 | bool |
| list | 查询某目录下的文件与文件夹 | 需要 |     不需要     |    目标目录    | dict |

