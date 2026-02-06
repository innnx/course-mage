from api.base_api import BaseApi

class OrderApi(BaseApi):
    def create_order(self,base_url,token,course_id):
        # 创建订单
        url = f"{base_url}/api/order"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return self.request(
            "POST",
            url,
            headers = headers,
            json = {
                "courseId": course_id
            }
        )
    
    def pay_order(self,base_url,token,order_id):
        # 支付订单
        url = f"{base_url}/api/order/{order_id}/pay"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return self.request(
            "PUT",
            url,
            headers = headers,
            json = {}
        )