import os

def app_config():
    ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    os.environ["ROOT_DIR"] = ROOT_DIR
