import pymysql
class DB:
    pass



# 登录，返回数据库类型，登陆失败则返回返回None
def login(user:str,password:str)->DB:
    global langs,status
    return None


# 静态变量部分
# DB.lang 为 {id:name} 如 {1:'C++',2:'Rust',3:'Python'}
# DB.status 为 {id:name} 如 {1:'Pending',2:'Wrong Answer',3:'RunningTimeError'}
# DB.fetch_code_limit 为是否限制读取其他用户的代码

class DB:
    fetch_code_limit=True

    # 提交，返回提交成功与否
    def submit(lang_id:int,code:str)->bool:
        pass

    # 返回的记录类型
    class record:
        # 提交用户
        user_id=0
        user_name=''
        # 提交结果
        status_id=0
        status_name=''
        # 提交语言
        language_id=0
        language_name=''
        # 题目编号
        problem_id=0

    # 按要求选择提交记录，返回成功与否
    # 传入参数为空，则表示不做限制
    def select_record(
            submit_ids:list[int] = [],
            user_ids:list[int] = [],
            status_ids:list[int] = [],
            problem_ids:list[int] = [],
            language_ids:list[int] = []
            )->bool:
        pass
    # 获取一条提交记录，若取完则返回None
    def fetchone()->record:
        pass
    # 获取多条提交记录
    def fetchall()->list[record]:
        pass
    def fetchmany(x:int = 1)->list[record]:
        pass

    # 获取提交记录的代码
    def fetch_code(submit_id:int)->str:
        pass

    # 获取题面
    def fetch_problem(problem_id:int)->bytes:
        pass
