
<center style= "font-size:36px; font-family:  '宋体';font-weight: bold;">在线代码提交系统</center>
<center style= "font-size:30px; font-family:  '宋体';font-weight: bold;">——数据库系统大作业</center>

## 实验人
姓名|学号|负责内容|联系方式
-|-|-|-
王子睿|21311590|前端设计和实现|18988999019
谢文龙|21311475|后端设计和实现|13016099039
## 模型概述
### 简述
- 作为本校ACM校队的学生，我们两位作者经常会需要在在线测评网站上完成一些算法竞赛题目，我们便想自己实现一个类似的但更为简化的模型，作为本次作业的主要内容。
- 本数据库系统主要实现了一个代码提交系统，其实现了作为在线代码提交系统的主要功能，即代码提交，提交记录查看等。
### 主要功能
#### 用户需求
我们按照实际需求，将用户分为普通用户和管理员用户两类，并分别实现不同需求，如下表：
-|提交代码|查看提交记录|查看代码|删除代码|修改代码状态
-|-|-|-|-|-
用户|✔|✔|仅自己|X|X
管理员用户|✔|✔|所有人|✔|✔
#### 登录页面
用户需要在登录页面输入用户名和密码，系统会自动判断用户是否被允许登录。

#### 代码提交页面
用户可以选择对应的题目和语言提交代码，提交成功后自动跳转到提交记录页面。

#### 提交记录页面
在提交记录页面，用户可以看到所有人的提交记录，也可以通过查询模式筛选指定用户名或者题目的提交记录，点击自己的提交记录会跳转到代码展示模式。

#### 代码展示
在该页面下，用户可以看到自己的代码。管理员可以查看所有代码并删除或者修改对应的提交记录。

### 主要结构设计
- 本系统主要通过html+python+mysql实现，我们通过利用python的`http.server`库来创建一个简易的服务器，串联前端和后端。
- 前端利用html+CSS+Javascript来建立一个浏览器页面（客户页面）利用HTTP GET 和HTTP POST 来传递和获得信息。
- 后端利用python的Mysqlclient库和mysql数据库来完成数据库的建构以及数据的存储和查询。

## 前端部分
- 由于完整代码过长（每个html文件 300行以上），这里就不放代码了。所有代码会放在附件中，也可以到我们的github仓库查看。
- [在线代码提交系统](https://github.com/VMalzahar/database-homework-T8)

### 登录页面
#### 流程图
![](graph/login.png)
#### 页面展示
![](graph/login_page.png)

### 代码提交页面
#### 流程图
![](graph/submit.png)
#### 页面展示
![](graph/submit_page.png)

### 提交记录页面
#### 流程图
![](graph/status.png)
#### 页面展示
![](graph/status_page_1.png)
![](graph/status_page_2.png)

### 代码展示页面
#### 流程图
![](graph/code.png)
#### 页面展示
![](graph/code_page.png)

### python部分
#### 流程图
![](graph/main.png)
- 通过上面的展示我们可以知道，我们主要依靠HTTP GET和HTTP POST中的不同路径来处理不同的请求，python部分就是负责这将不同路径调用相应封装好的功能函数，起到控制的作用。
  
```python
    def do_GET(self): #处理HTTP GET请求，不同路径对应不同的处理
        
        global username,state,dbconn
        path = self.path
        if(path=='/'):
            if(username!=''):
                self.path='/status.html'
        if(path=="/login.html"):
            username=""
        if(path=="/user"):
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.send_header("username",username)
            self.end_headers()
            return
        if(path=="/submissions"):
            self.send_response(200)
            self.send_header("Content-type","text/json")
            self.end_headers()
            data=get_status(dbconn)
            data=json.dumps(data)
            self.wfile.write(bytes(data, 'utf-8'))
            return

        print(path)
        self.writef()
```
- HTTP POST 的处理是类似的，不过值得主意的是他通过这样的方式解压javascript的字符串：
```python
    datas = self.rfile.read(int(self.headers['content-length']))    #固定格式，获取表单提交的数据
    datas= json.loads(datas)
```
