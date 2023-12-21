import pymysql
class USER:
    pass


# self.lang 为 {id:name} 如 {1:'C++',2:'Rust',3:'Python'}
# self.status 为 {id:name} 如 {1:'Pending',2:'Wrong Answer',3:'RunningTimeError'}
class DataBase:
    pass

# 数据库登录至管理员账号，登陆失败则返回None
def DB_login(dbuser:str,password:str)->DataBase:
    return None

# 用户登录，登陆失败则返回None
def USER_login(self,db:DataBase,user:str,password:str)->USER:
    pass

class USER:
    # 提交，返回提交成功与否
    def submit(self,lang_id:int,code:str)->bool:
        pass

    # 返回的记录类型
    class record:
        submit_id=0
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
    # 获取一条提交记录，若取完则返回None
    def fetchone(self)->record:
        pass
    # 获取多条提交记录
    def fetchall(self)->list[record]:
        pass
    def fetchmany(self,x:int = 1)->list[record]:
        pass

    # 获取提交记录的代码
    def fetch_code(self,submit_id:int)->str:
        pass

    # 获取题面
    def fetch_problem(self,problem_id:int)->bytes:
        pass

