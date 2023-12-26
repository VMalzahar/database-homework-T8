# 需要 pip install mysqlclient

import MySQLdb
import MySQLdb.cursors as cors
from operator import itemgetter as iget

# 返回的记录类型
class reccls:
    def __init__(self,rec:dict):
        self.submit_id=0
        # time_slot 返回整数
        # 可用 datetime.datetime.fromtimestamp(time_slot) 获得时间戳
        # 可用 dt.timestamp() 获得整数格式
        self.time_slot=0
        # 题目编号
        self.problem_id=0
        # 提交用户
        self.user_id=0
        self.user_name=''
        # 提交语言
        self.language_id=0
        self.language_name=''
        # 提交结果
        self.status_id=0
        self.status_name=''
        self.code_len=0
        self.time=0
        # 提交代码，若权限不足则为 None
        self.code=None

        (self.submit_id,self.time_slot,
         self.problem_id,
         self.user_id,self.user_name,
         self.language_id,
         self.status_id,
         self.code_len,self.time,
         self.code)=iget(
             "submit_id","time_slot",
             "problem_id",
             "user_id","user_name",
             "language_id",
             "status_id",
             "code_len","time",
             "code"
             )(rec)
        self.time_slot=self.time_slot.timestamp()

# 进行数据库连接内容设置，返回测试连接成功与否
def DB_set(dbuser:str,password:str,database:str,connection:str = "localhost")->bool:
    try:
        conn = MySQLdb.connect(
                connection,
                dbuser,
                password,
                database,
                charset='utf8',
                cursorclass=cors.DictCursor)
        conn.close()
        DB._connection=connection
        DB._dbuser=dbuser
        DB._password=password
        DB._database=database
        return True
    except:
        return False

# self.lang 为 {id:name} 如 {1:'C++',2:'Rust',3:'Python'}
# self.status 为 {id:name} 如 {1:'Pending',2:'Wrong Answer',3:'RunningTimeError'}
# self.user_name 为用户昵称
class DB:
    _connection=""
    _dbuser=""
    _password=""
    _database=""

    def __init__(self,user:str,password:str):
        self.conn = MySQLdb.connect(
                DB._connection,
                DB._dbuser,
                DB._password,
                DB._database,
                charset='utf8',
                cursorclass=cors.DictCursor)
        try:
            tmpc=self.conn.cursor()
            sql="""SELECT user_id,password,user_name,`grant` FROM `user` WHERE user_code=%s"""
            tmpc.execute(sql,[user])
            results=tmpc.fetchall()
            if len(results)!=1 or results[0]['password']!=password:
                raise Exception("password error")
            result=results[0]
            (self.user_id, self.password,
             self.user_name, self.grant)=iget(
                     "user_id","password",
                     "user_name","grant")(result)

            try:
                sql="""select {0}_id,{0}_name from `{0}`"""
                dim="language"
                tmpc.execute(sql.format(dim))
                self.lang={
                        i_n[dim+'_id']:i_n[dim+'_name']
                        for i_n in tmpc.fetchall()}

                dim="status"
                tmpc.execute(sql.format(dim))
                self.status={
                        i_n[dim+'_id']:i_n[dim+'_name']
                        for i_n in tmpc.fetchall()}
            except:
                pass
            tmpc.close()

        except:
            tmpc.close()
            raise Exception("user or password error")

    def __del__(self):
        self.conn.close()

    # 修改，只有管理员账户能够成功
    # update_column 为修改项目，参考class record中非`*_name`项
    # update_record 为具体修改，支持多个记录同时修改，格式为 [(update_thing,submit_id), (update_thing,submit_id), ...]
    # 不支持改 code
    def update(self,
              update_column:str,
              update_record:list[(any,int)])->bool:
        if self.grant==0:
            return False
        tmpc=self.conn.cursor()
        try:
            sql="UPDATE record SET `{}`=%s WHERE submit_id=%s".format(update_column)
            c=update_record[0]
            tmpc.executemany(sql,update_record)
            self.conn.commit()
            succ=True
        except:
            self.conn.rollback()
            succ=False
        tmpc.close()
        return succ
    # 提交，返回提交成功的 submit_id ，若提交失败则返回 None
    def submit(self,problem_id:int,lang_id:int,code:str)->int:
        tmpc=self.conn.cursor()
        try:
            sql="INSERT INTO record(user_id,problem_id,language_id,`code`) VALUES (%s,%s,%s,%s)"
            tmpc.execute(sql%
                         (self.user_id,problem_id,lang_id,
                          "0x"+code.encode("utf-8").hex()))
            sql="SELECT LAST_INSERT_ID()"
            tmpc.execute(sql)
            self.conn.commit()
            succ=tmpc.fetchone()["LAST_INSERT_ID()"]
        except:
            self.conn.rollback()
            succ=None
        tmpc.close()
        return succ



    def get_record(self,rec:dict)->reccls:
        r=reccls(rec)
        (r.language_name,
         r.status_name)=(
                self.lang[r.language_id],
                self.status[r.status_id])
        r.code = None if self.grant==0 and self.user_id!=r.user_id else r.code.decode("utf-8")
        return r

    def getview(self):
        return "s_{}_{}_record".format(self.user_id,self.user_name)
    # 按要求选择提交记录，返回成功与否
    # 传入参数为空，则表示不做限制
    def select_record(self,
            submit_ids:list[int] = [],
            user_ids:list[int] = [],
            status_ids:list[int] = [],
            problem_ids:list[int] = [],
            language_ids:list[int] = []
            )->bool:
        tmpc=self.conn.cursor()
        try:
            view_condition = lambda st,ls: st+" IN ("+",".join(map(str,ls))+")" if ls else "TRUE"
            condition = " AND ".join(
                    [view_condition("submit_id",submit_ids),
                     view_condition("user_id",user_ids),
                     view_condition("status_id",status_ids),
                     view_condition("problem_id",problem_ids),
                     view_condition("language_id",language_ids),
                     ])
            sql="""CREATE OR REPLACE VIEW {} AS
SELECT * FROM record NATURAL JOIN `user`
WHERE {}
ORDER BY time_slot DESC, submit_id DESC""".format(
        self.getview(),condition)
            tmpc.execute(sql)
            succ=True
        except:
            succ=False
        tmpc.close()
        return succ
    # 获取多条提交记录
    def fetchall(self)->list[reccls]:
        tmpc=self.conn.cursor()
        try:
            sql="SELECT * FROM {}".format(self.getview())
            tmpc.execute(sql)
            lst=list(map(self.get_record,tmpc.fetchall()))
        except:
            lst=[]
        tmpc.close()
        return lst

    # 获取从 x 开始 num 条提交记录
    def fetchmany(self,x:int = 1,num:int = 100)->list[reccls]:
        # select * from table limit L,num
        tmpc=self.conn.cursor()
        try:
            sql="SELECT * FROM {} LIMIT {},{}".format(self.getview(),x,num)
            tmpc.execute(sql)
            lst=list(map(self.get_record,tmpc.fetchall()))
        except:
            lst=[]
        tmpc.close()
        return lst

    # 获取提交记录的代码
    def fetch_code(self,submit_id:int)->str:
        pass

    # 获取题面
    def fetch_problem(self,problem_id:int)->bytes:
        pass

# 用户登录，登陆失败则返回None
# 也推荐使用DB(user,password)建立连接，登陆失败会报异常
def USER_login(user:str,password:str)->DB:
    try:
        db=DB(user,password)
        return db
    except:
        return None


if __name__=="__main__":
    dbuser="root"
    password=""
    database="final"
    if DB_set(dbuser,password,database): # 设置数据库管理员
        user="coder_2"
        password="654321"
        user=USER_login(user,password) # 登录用户
        print("user_id=",user.user_id," user_name=",user.user_name)
    else:
        print("set error")
        exit()
    
    print("grant",user.grant)

    # 提交代码
    problem_id=1
    language_id=2
    code="""haawh
awdn'"_+`123awdoof"""
    sid=user.submit(problem_id,language_id,code)
    language_id=3
    sid=user.submit(problem_id,language_id,code)
    # 如果有权限则可以更新
    user.grant=1 
    flag=user.update("language_id",[(4,sid),(1,sid-1)]) # 批量更新
    print("update sid(",sid,")",flag)
 
    # 选择满足特定条件的数据
    flag=user.select_record(
            submit_ids=range(2,sid+2),
            language_ids=[2,4])
    print("select",flag)
    s=user.fetchmany(0,3) # 取数据，取从0开始3个
    for rec in s:
        print("\n>>> submit_id=",rec.submit_id,"user_name=",rec.user_name)
        print("---------------",rec.language_name)
        print(rec.code)
        print("+++++++++++++++")


