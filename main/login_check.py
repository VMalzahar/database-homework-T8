from typing import Dict

class Login_check():
    def __init__(self) -> None:
        pass
    def check(self,username,password) -> bool:
        if username=="admin" and password=="123456":
            return 1
        else:
            return 0