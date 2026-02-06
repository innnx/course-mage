from api.base_api import BaseApi

class CourseApi(BaseApi):
    def create_course(self,base_url,token,course_title,categoryId,description,price):
        # 创建课程 返回课程id
        url = f"{base_url}/api/course"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return self.request(
            "POST",
            url,
            headers = headers,
            json = {
                "title": course_title,
                "categoryId": categoryId,
                "description": description,
                "price": price
            }
        )
    
    def page_query(self,base_url,token,query_keyword):
        # 分页查询课程（关键字）
        url = f"{base_url}/api/course/page"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        # 将 json 改为 params ---
        payload = {
            "keyword": query_keyword,
            "pageNum": 1,
            "pageSize": 10
        }
        return self.request(
            "GET",
            url,
            headers = headers,
            params = payload
        )