import pandas as pd

def save_to(file_data, file_path):
    with open(file_path, 'w') as f:
        f.write(file_data)

def load_json_into_df(file_path):
    with open(file_path, 'r') as f:
        data_stream = f.read()
    return pd.read_json(data_stream)

