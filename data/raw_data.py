import pandas as pd

def read_csv(file_path):
    try:
        return pd.read_csv(file_path, sep=';', encoding='latin1')
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return None
    