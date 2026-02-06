import pytest
from common.config_util import load_config

def pytest_addoption(parser):
    # 支持命令行参数 pytest --env=test
    parser.addoption("--env",action="store",default="test")

@pytest.fixture(scope="session")
def env_config(request):
    # 全局环境配置
    env = request.config.getoption("--env")
    return load_config(env)