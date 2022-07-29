import json
import os
import pandas as pd
from app_utils import eng_db

file_path = r'pipe_api\files\all_deals_history'
with open(file_path, 'r') as f:
    data_stream = json.loads(f.read())


