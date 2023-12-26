# 需要 pip install mysqlclient
# 在 dbconnect.py 的末尾有测试及演示

import MySQLdb
import MySQLdb.cursors as cors

# 进行数据库连接内容设置，返回测试连接成功与否
def DB_set(dbuser:str,password:str,database:str,connection:str = "localhost")->bool:
    pass
# 用户登录，登陆失败则返回None
# 也推荐使用DB(user,password)建立连接，登陆失败会报异常
def USER_login(user:str,password:str)->DB:
    pass

# 返回的记录类型
class reccls:
    submit_id=0
    # time_slot 返回小数
    # 可用 datetime.datetime.fromtimestamp(time_slot) 获得时间戳
    # 可用 dt.timestamp() 获得小数格式
    time_slot=0
    # 题目编号
    problem_id=0
    # 提交用户
    user_id=0
    user_name=''
    # 提交语言
    language_id=0
    language_name=''
    # 提交结果
    status_id=0
    status_name=''
    code_len=0
    time=0
    # 提交代码，若权限不足则为 None
    code=None


# self.lang 为 {id:name} 如 {1:'C++',2:'Rust',3:'Python'}
# self.status 为 {id:name} 如 {1:'Pending',2:'Wrong Answer',3:'RunningTimeError'}
# self.user_name 为用户昵称
class DB:
    # 修改，只有管理员账户能够成功
    # update_column 为修改项目，参考class record中非`*_name`项
    # update_record 为具体修改，支持多个记录同时修改，格式为 [(update_thing,submit_id), (update_thing,submit_id), ...]
    # 不支持改 code
    def update(self,
              update_column:str,
              update_record:list[(any,int)])->bool:
        pass
    # 提交，返回提交成功的 submit_id ，若提交失败则返回 None
    def submit(self,problem_id:int,lang_id:int,code:str)->int:
        pass

    # 按要求选择提交记录，返回成功与否
    # 传入参数为空，则表示不做限制
    def select_record(self,
            submit_ids:list[int] = [],
            user_ids:list[int] = [],
            status_ids:list[int] = [],
            problem_ids:list[int] = [],
            language_ids:list[int] = []
            )->bool:
        pass
    # 获取所有提交记录
    def fetchall(self)->list[record]:
        pass
    # 获取从满足条件的第 x 开始 num 条提交记录（x从0开始算）
    def fetchmany(self,x:int = 0,num:int = 100)->list[record]:
        pass

    # 获取提交记录的代码
    def fetch_code(self,submit_id:int)->str:
        pass

    # 获取题面
    def fetch_problem(self,problem_id:int)->bytes:
        pass

