import time
from api.course_api import CourseApi
from api.order_api import OrderApi
from api.user_api import UserApi
from common.logger import logger

class BusinessFlow:
    """
    业务流程层（核心）
    作用：
        把多个接口组合成一个业务动作
    好处：
        - 用例更简洁
        - 逻辑复用
        - 易维护
    """
    def __init__(self,base_url):
        self.base_url = base_url
        # 初始化所有api
        self.user_api = UserApi()
        self.order_api = OrderApi()
        self.course_api = CourseApi()

        self.token = None

    # 注册+登录
    def register_and_login(self,username,password,nickname):
        username = f"{username}_{int(time.time())}"
        logger.info(f"注册用户:{username}")
        self.user_api.register(self.base_url,username,password,nickname)
        res = self.user_api.login(self.base_url,username,password)
        self.token = res.json()["data"]["token"]
        logger.info(f"登录成功:{self.token}")
        return self.token
    
    # 创建课程并获取id
    def create_course_and_get_id(self,query_keyword,course_title,categoryId,description,price):
        logger.info(f"创建课程:{course_title}")
        self.course_api.create_course(self.base_url,self.token,course_title,categoryId,description,price)
        res = self.course_api.page_query(
            self.base_url,
            self.token,
            query_keyword
        )
        course_list = res.json()["data"]["records"]
        for c in course_list:
            if c["title"] == course_title:
                logger.info(f"获取课程成功:{c['id']}")
                return c["id"]
        raise Exception("未找到课程ID")
    
    # 创建并支付订单
    def create_paid_order(self,course_id):
        logger.info(f"创建订单:course_id={course_id}")
        res = self.order_api.create_order(
            self.base_url,
            self.token,
            course_id
        )
        order_id = res.json()["data"]
        logger.info(f"支付订单:order_id={order_id}")
        self.order_api.pay_order(
            self.base_url,
            self.token,
            order_id
        )
        return order_id

