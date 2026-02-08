FROM python:3.10-slim

WORKDIR /app

# 预安装依赖（利用缓存）
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 拷贝测试代码
COPY . .

#运行指令
CMD ["pytest", "--env=prod", "--alluredir=./allure-results"]