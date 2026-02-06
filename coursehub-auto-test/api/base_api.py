import requests

class BaseApi:
    """
    所有接口的基类
    统一封装request
    后期可以在这里：
        -打日志
        -加重试
        -加统一headers
    """

    def request(self,method,url,**kwargs):
        return requests.request(method,url,**kwargs)