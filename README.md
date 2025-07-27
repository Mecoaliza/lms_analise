# Análise de LMS (Learning Management System)

Este projeto utiliza dados de interação com um LMS para explorar padrões de uso, engajamento dos alunos e desempenho.
Criando uma pipeline simples para transformação e segmentação das informações.

## 📊 Objetivos

- Tratar dados e criar campos a partir dos existentes para uma melhor análise
- Segmentar alunos por desempenho e tipo de conteúdo
- Criar campos calculados do comportamento dos alunos
- Implementação de cluster e previsão de churn para identificar padrões e treinar dados


## 🛠️ Tecnologias

- Python
- Power BI
- Linguagem DAX

## 🛠️ Funcões

### `normaliza_data(df)`

- Combina as colunas de **Data** e **Hora** em uma única coluna `data_hora` do tipo datetime.
- Cria a coluna `dia_semana` com o nome do dia da semana (ex: Segunda-feira, Terça-feira, etc.).
- Cria a coluna `periodo`, categorizando o horário do acesso em:
  - `Manhã`: 06h às 11h59  
  - `Tarde`: 12h às 17h59  
  - `Noite`: 18h às 23h59  
  - `Madrugada`: 00h às 05h59

### `normaliza_notas(df)`

- Trata os valores da coluna `Nota` (em string com vírgula) para número decimal.
- Cria a coluna `nota_valida` para identificar se a nota é numérica ou nula.
- Classifica as notas em três categorias na coluna `nivel_nota`:
  - `Baixa`: nota < 4  
  - `Média`: nota ≥ 4 e < 7  
  - `Alta`: nota ≥ 7  

- Categorização da coluna `Feature` em tipos:
  - `Avaliativo`: simulados  
  - `Teórico`: eBooks, aulas online  
  - `Prático`: exercícios  
  - `Outro`: demais categorias

### `comportamento_aluno(df)`

- Calcula a quantidade de interações por:
  - Estudante (`interacoes_estudante`)
  - Curso (`interacoes_curso`)
  - Região (`interacoes_regiao`)

- Adiciona colunas com:
  - `primeiro_acesso` e `ultimo_acesso` por estudante
  - `tempo_desde_ultimo` acesso (em dias)
  - `dias_ativos` (número de dias únicos com acesso)
  - `media_nota_estudante` (média das notas numéricas)


