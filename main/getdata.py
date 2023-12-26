from datetime import datetime

def get_status(dbconn,id=[],problem_id=[] ,user_name=[]):
    # res=[{"problem":"problem1","language":"C++","verdict":"accept","time":"300ms","time_slot":"2023/12/25","user":"Frieren","id":"1"}]
    r2d = lambda r: {"problem":str(r.problem_id),
                     "language":r.language_name,
                     "verdict":r.status_name,
                     "time":str(r.time)+"ms",
                     "time_slot":datetime.fromtimestamp(r.time_slot).strframe("%Y-%m-%d %H:%M:%S"),
                     "user":r.user_name,
                     "id":r.submit_id}
    dbconn.select_record(submit_ids=id,problem_id=problem_ids,user_ids=user_name)
    return list(map(r2d,dbconn.fetchall()))

def deletesubmition(dbconn,id:int):
    dbconn.delete([id])

def Changesubmition(dbconn,id:int,status:str):
    if status=="AC":
        status_id=2
    elif status=="WA":
        status_id=3
    elif status=="TLE":
        status_id=4
    elif status=="MLE":
        status_id=5
    elif status=="RE":
        status_id=6
    dbconn.update("status_id",[(status_id,id)])

def findcode(dbconn,id:int) -> str:
    return dbconn.fetchcode(id)

def submitCode(dbconn,user:str,lang:str,code:str,question_id:int):
    dbconn.submit(question_id,lang,code)
