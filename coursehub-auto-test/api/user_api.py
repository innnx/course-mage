from api.base_api import BaseApi

class UserApi(BaseApi):

    def register(self,base_url,username,password,nickname):
        # 注册接口
        url = f"{base_url}/api/user/register"
        return self.request(
            "POST",
            url,
            json = {
                "username": username,
                "password": password,
                "nickname": nickname
            }
        )
    
    def login(self,base_url,username,password):
        # 登录接口--获取token
        url = f"{base_url}/api/user/login"
        return self.request(
            "POST",
            url,
            json = {
                "username": username,
                "password": password
            }
        )