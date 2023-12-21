from http.server import HTTPServer, BaseHTTPRequestHandler
import login_check
import json

host = ('localhost', 8888)
 
class Resquest(BaseHTTPRequestHandler):
    timeout = 5
    server_version = "Apache"   #设置服务器返回的的响应头 
    state=0
    user_name=""
    password=""
    login_check=login_check.Login_check()
    def writef(self,login_flag=True):
        
        if(self.user_name==""):
            self.path='/login.html'
            self.state=0
        # if(flag==1):
        #     self.path='/submit.html'
        # print(buf)
        self.state=0
        # if(flag==1):
        self.send_response(200)
        self.send_header("Content-type","text/html")  #设置服务器响应头
        if(login_flag==False):self.send_header("login_fail","")
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()
        with open('html'+self.path, 'r', encoding='utf-8') as html1:
            buf=html1.read()
        # print(buf)
            # self.state=1
        # print("TT",buf)
        self.wfile.write(bytes(buf, 'utf-8'))
        # self.wfile.write(buf.encode()) 


    def do_GET(self):
        
        path = self.path
        print(path)
        self.writef(self.state)
        # print(self.state)
         #里面需要传入二进制数据，用encode()函数转换为二进制数据   #设置响应body，即前端页面要展示的数据
 
    def do_POST(self):
        path = self.path
        print(path)
        #获取post提交的数据
        datas = self.rfile.read(int(self.headers['content-length']))    #固定格式，获取表单提交的数据
        datas= json.loads(datas)
        if self.user_name=="":
            self.user_name=datas["user_name"]
            self.password=datas["password"]
        
        #datas = urllib.unquote(datas).decode("utf-8", 'ignore')
        print(datas)
        # self.state=1
        # self.do_GET()
        self.writef(login_flag=self.login_check.check(self.user_name,self.password))


if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()