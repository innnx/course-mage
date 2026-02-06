import yaml

def load_config(env="test"):
    """
    读取环境配置文件
    作用：支持多环境切换(DEV/SIT/Prod/)
    """
    with open(f"config/{env}.yaml",encoding="utf-8") as f:
        return yaml.safe_load(f)