from data.raw_data import read_csv
import pandas as pd

def normaliza_data(df):
    df['data_hora'] = pd.to_datetime(df['Data'] + ' ' + df['Hora'], format='%d/%m/%Y %H:%M:%S')
    df['dia_semana'] = df['data_hora'].dt.day_name()
    df['periodo'] = df['data_hora'].dt.hour.apply(periodo_do_dia)

    return df

def periodo_do_dia(h):
    if 6 <= h < 12:
        return 'Manhã'
    elif 12 <= h < 18:
        return 'Tarde'
    elif 18 <= h < 24:
        return 'Noite'
    else:
        return 'Madrugada'
    
def classifica_nota(n):
    if pd.isnull(n): return 'Sem nota'
    elif n < 4: return 'Baixa'
    elif n < 7: return 'Média'
    else: return 'Alta'
    
def normaliza_notas(df):
    df['nota_num'] = pd.to_numeric(df['Nota'].str.replace(',', '.'), errors='coerce')
    df['nota_valida'] = df['nota_num'].notnull()
    df['nivel_nota'] = df['nota_num'].apply(classifica_nota)
    df['tipo_feature'] = df['Feature'].apply(tipo_feature)

    return df

def tipo_feature(feature):
    feature = feature.lower().strip()
    if feature == 'simulados':
        return 'Avaliativo'
    elif feature in ['ebooks', 'aulas online']:
        return 'Teórico'
    elif feature == 'exercicio':
        return 'Prático'
    else:
        return 'Outro'
    
def comportamento_aluno(df):
    df['interacoes_estudante'] = df.groupby('Estudante')['ID'].transform('count')
    df['interacoes_curso'] = df.groupby('Curso')['ID'].transform('count')
    df['interacoes_regiao'] = df.groupby('Região')['ID'].transform('count')
    df['ultimo_acesso'] = df.groupby('Estudante')['data_hora'].transform('max')
    df['primeiro_acesso'] = df.groupby('Estudante')['data_hora'].transform('min')
    df['tempo_desde_ultimo'] = pd.to_datetime('now') - df['ultimo_acesso']
    df['dia'] = df['data_hora'].dt.date
    df['dias_ativos'] = df.groupby('Estudante')['dia'].transform('nunique')


df = read_csv('./data/Dados.csv')
normaliza_data(df)
normaliza_notas(df)
comportamento_aluno(df)
print(df.head(5))