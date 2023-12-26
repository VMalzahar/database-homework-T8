import dbconnect
from typing import Dict

class Login_check():
    def __init__(self) -> None:
        pass
    def check(self,username,password) -> bool:
        return dbconnect.USER_login(username,password) is not None
