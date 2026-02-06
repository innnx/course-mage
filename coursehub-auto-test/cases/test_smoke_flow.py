import pytest

from common.yaml_util import load_yaml
from service.business_flow import BusinessFlow

@pytest.mark.smoke
@pytest.mark.parametrize(
    "case_data",
    load_yaml("data/smoke_flow.yaml")
)
class TestSmokeFlow:

    # 主流程冒烟测试：注册 -> 登录 -> 创建课程 -> 查询课程 -> 创建订单 -> 支付订单

    def test_full_bussiness_flow(self,env_config,case_data):
        flow = BusinessFlow(env_config["base_url"])

        # 1.注册&登录
        flow.register_and_login(
            case_data["username"],
            case_data["password"],
            case_data["nickname"]
        )

        # 3.创建课程&查询课程ID
        course_id = flow.create_course_and_get_id(
            course_title=case_data["course_title"],
            categoryId=case_data["categoryId"],
            price=case_data["price"],
            description=case_data["description"],
            query_keyword=case_data["query_keyword"]
        )

        # 5.创建订单&支付
        order_id = flow.create_paid_order(course_id)
        assert order_id is not None