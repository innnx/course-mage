import yaml

def load_yaml(file_path):
    # 读取yaml文件并返回数据
    with open(file_path,encoding="utf-8")as f:
        return yaml.safe_load(f)