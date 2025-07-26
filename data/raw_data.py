import pandas as pd
import os

def read_csv(filename='Dados.csv'):
    try:
        base_path = os.path.dirname(__file__) 
        file_path = os.path.join(base_path, filename)

        return pd.read_csv(file_path, sep=';', encoding='latin1')
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return None
    
