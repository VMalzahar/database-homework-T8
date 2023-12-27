from datetime import datetime

def get_status(dbconn,id=0,problem_id="" ,user_name=""):
    # res=[{"problem":"problem1","language":"C++","verdict":"accept","time":"300ms","time_slot":"2023/12/25","user":"Frieren","id":"1"}]
    r2d = lambda r: {"problem":r.problem_id,
                     "language":r.language_name,
                     "verdict":r.status_name,
                     "time":str(r.time)+"ms" if r.time else "",
                     "time_slot":datetime.fromtimestamp(r.time_slot).strftime("%Y-%m-%d %H:%M:%S"),
                     "user":r.user_name,
                     "id":r.submit_id}
    id = [] if id==0 else [id]
    print("id=",problem_id)
    problem_id = [] if problem_id=="" else [problem_id]
    print("<id=",problem_id)
    user_name = [] if user_name=="" else [user_name]
    dbconn.select_record(submit_ids=id,problem_ids=problem_id,user_ids=user_name)
    return list(map(r2d,dbconn.fetchall()))

def deletesubmition(dbconn,id:int):
    dbconn.delete([id])

def Changesubmition(dbconn,id:int,status:str):
    s2id={"AC":2,"WA":3,"TLE":4,"MLE":5,"RE":6}
    dbconn.update("status_id",[(s2id[status],id)])

def findcode(dbconn,id:int) -> str:
    return dbconn.fetch_code(id)

def submitCode(dbconn,user:str,lang:str,code:str,question_id:int):
    l2id={"cpp":2,"java":4,"python":3}
    dbconn.submit(question_id,l2id[lang],code)
