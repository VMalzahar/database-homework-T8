import dbconnect
from typing import Dict

class Login_check():
    def __init__(self) -> None:
        pass
    def check(self,username,password) -> int:
        print("check",username,password)
        if dbconnect.USER_login(username,password) is not None:
            return 1
        else:
            return 0
