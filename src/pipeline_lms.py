import pandas as pd
import os
from data.raw_data import read_csv
from datetime import datetime
from src.segmentation import segmentar_alunos_por_perfil, prever_churn_alunos
from src.transform import normaliza_data, normaliza_notas, comportamento_aluno

df = read_csv()

df = normaliza_data(df)
print("Tratando data e hora...")
df = normaliza_notas(df)
print("Classificando notas...")
df = comportamento_aluno(df)
print("Classificando comportamento dos alunos...")
df = segmentar_alunos_por_perfil(df)
print("Segmentando alunos por perfil...")
#df = prever_churn_alunos(df)
#print("Classificando aluno por risco...")

output_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
data_export = datetime.today().strftime('%Y-%m-%d')
output_path = os.path.join(output_folder, f'powerbi_base_lms_{data_export}.csv')
df.to_csv(output_path, index=False)


print(f"Arquivo exportado com sucesso para: {output_path}")