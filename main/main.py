from http.server import HTTPServer, BaseHTTPRequestHandler
import login_check
import json
from getdata import *
import dbconnect

if not dbconnect.DB_set("root","","final"):
    raise Exception("cannot connect to database.")
host = ('localhost', 8888)

username=""
password=""
login=login_check.Login_check()    
dbconn=None
state=0
class Resquest(BaseHTTPRequestHandler):
    timeout = 5
    server_version = "Apache"   #设置服务器返回的的响应头 
    def writef(self,login_flag=2): #根据路径向客户端发送对应的html
        global username,password,state,dbconn
        if(login_flag==1):
            dbconn=dbconnect.USER_login(username,password)
            self.path="/submit.html"
        if(login_flag==0):
            self.path="/login.html"
            username=""
        if(username==""):
            self.path='/login.html'
            self.state=0
        self.send_response(200)
        self.send_header("Content-type","text/html")  #设置服务器响应头
        if login_flag==0:
            self.send_header("login_fail","")
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()
        with open('html'+self.path, 'r', encoding='utf-8') as html1:
            buf=html1.read()
        self.wfile.write(bytes(buf, 'utf-8'))


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
 
    def do_POST(self):#处理HTTP POST请求，不同路径对应不同的处理
        
        global username,password,state,dbconn
        path = self.path
        print(path)
        #获取post提交的数据
        datas = self.rfile.read(int(self.headers['content-length']))    #固定格式，获取表单提交的数据
        datas= json.loads(datas)
        print(datas)
        if(path== "/login"):
            if username=="":
                username=datas["user_name"]
                password=datas["password"]
            self.writef(login_flag=login.check(username,password))
        if(path== "/search"):
            self.send_response(200)
            self.send_header("Content-type","text/json")
            self.end_headers()
            data=get_status(dbconn,id=datas["id"],problem_id=datas["problem_id"],user_name=datas['username']) 
            data=json.dumps(data)
            self.wfile.write(bytes(data, 'utf-8'))
            return
            pass
        if(path== "/find"):
            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            if username=="admin":
                self.path="/code_admin.html"
            else:
                self.path="/code_normal.html"
            with open('html'+self.path, 'r', encoding='utf-8') as html1:
                buf=html1.read()
            ### 插入code
            buf=buf.replace("'id': 0,","'id': "+str(datas["id"])+",")
            buf=buf.replace("deletesubmition(id)","deletesubmition("+str(datas["id"])+")")
            buf=buf.replace("Changesubmition(id)","Changesubmition("+str(datas["id"])+")")
            buf=buf.replace("<code></code>","<code>\n"+findcode(dbconn,datas["id"])+"\n</code>")

            ###
            self.wfile.write(bytes(buf, 'utf-8'))
            print(buf)
        if(path=='/change'):
            Changesubmition(dbconn,datas["id"],datas["new_status"])
            self.path='/status.html'
            self.writef()
            pass
        if(path=='/delete'):

            deletesubmition(dbconn,datas["id"])
            self.path='/status.html'
            self.writef()
            pass
        if(path=='/submitCode'):
            submitCode(dbconn,username,datas["Language"],datas["Code"],datas["question_id"])
            self.path='/status.html'
            self.writef()
            pass

        

if __name__ == '__main__':
    #启动服务器
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
