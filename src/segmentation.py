from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def segmentar_alunos_por_perfil(df, n_clusters=3):

    """
    Realiza clustering dos alunos com base em engajamento e desempenho.

    Parâmetros:
    - df: DataFrame com colunas ['Estudante', 'media_nota_estudante', 'interacoes_estudante', 'dias_ativos']
    - n_clusters: número de clusters para o KMeans

    1. Seleciona colunas relevantes e remove duplicatas por aluno
    2. Padroniza os dados
    3. KMeans clustering
    4. Mapeia clusters para perfis com base em médias
    5. Junta os perfis de volta ao DataFrame original com a coluna 'perfil_aluno'
    """


    alunos = df[['Estudante', 'media_nota_estudante', 'interacoes_estudante', 'dias_ativos']].drop_duplicates()
    alunos = alunos.dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(alunos[['media_nota_estudante', 'interacoes_estudante', 'dias_ativos']])

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    alunos['cluster'] = kmeans.fit_predict(X_scaled)

    cluster_mean = alunos.groupby('cluster').mean().sort_values(by='interacoes_estudante')
    perfil_map = {idx: perfil for idx, perfil in zip(cluster_mean.index, ['Inativo', 'Regular', 'Engajado'])}
    alunos['perfil_aluno'] = alunos['cluster'].map(perfil_map)

    df = df.merge(alunos[['Estudante', 'perfil_aluno']], on='Estudante', how='left')

    return df


def prever_churn_alunos(df, dias_limite=5):
    """
    Cria um modelo de churn prediction com base em interações e notas.
    Aluno "ativo" (0) → acessou nos últimos 5 dias

    Aluno "churn" (1) → não acessa há 5 dias ou mais

    Parâmetros:
    - df: DataFrame com colunas: Estudante, ultimo_acesso, interacoes_estudante, dias_ativos, media_nota_estudante
    - dias_limite: número de dias sem acesso para considerar churn

    1. Calcula tempo desde o último acesso
    2. Cria target: churn = 1 se inativo por mais de X dias
    3. Remove duplicatas por aluno
    4. Prepara dados para ML
    5. Divide treino/teste e treina modelo
    6. Aplica modelo em todos os alunos para prever risco de churn
    7. Junta de volta ao DataFrame principal com a coluna 'churn_risco'

    """

    df['dias_desde_ultimo'] = (pd.to_datetime('now') - df['ultimo_acesso']).dt.days

    df['churn'] = (df['dias_desde_ultimo'] >= dias_limite).astype(int)

    alunos = df[['Estudante', 'interacoes_estudante', 'dias_ativos', 'media_nota_estudante', 'churn']].drop_duplicates()
    alunos = alunos.dropna()

    X = alunos[['interacoes_estudante', 'dias_ativos', 'media_nota_estudante']]
    y = alunos['churn']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    alunos['churn_risco'] = model.predict_proba(X_scaled)[:, 1]

    df = df.merge(alunos[['Estudante', 'churn_risco']], on='Estudante', how='left')

    return df