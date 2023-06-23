# Projeto de Engenharia de Dados: Migração, Processamento e Visualização de um Banco de Dados SQL Server para um Ambiente AWS com Datalake e Power BI

Este projeto envolve a transferência de dados de um banco de dados SQL Server para a AWS, sua transformação e posterior visualização no Power BI. Ao longo deste processo, são utilizadas várias tecnologias e serviços da AWS, como RDS, DMS, Glue e Athena, para garantir uma manipulação de dados eficiente e eficaz.




## 💻 Sumário
* [Overview da solução](#overview-da-solução)
* [Desafios e potenciais impactos ](#desafios-e-potenciais-impactos)
* [Backup do SQL Server](#backup-do-sql-server)
    + Instalação Docker 
    + Criação de um container sql server.
    + Importação do backup para o container
* [Criação de uma instância do RDS Postgres](#criação-de-uma-instância-do-rds-postgres)
* [Migração dos dados do banco Sql Server no Docker para RDS Postgres](#migração-dos-dados-do-banco-sql-server-no-docker-para-rds-postgres)
* [Migração dos dados do RDS para S3 com DMS](#migração-dos-dados-do-RDS-para-S3-com-DMS)
* [Transformação dos dados com AWS Glue](#transformação-dos-dados-com-aws-glue)
* [Armazenamento dos dados processados no S3](#armazenamento-dos-dados-processados-no-s3)
* [Consulta dos dados com o AWS Athena](#consulta-dos-dados-com-o-AWS-Athena)
* [Visualização dos dados com Power BI](#visualização-dos-dados-com-Power-BI)
<br>

## Overview da solução
![AWS Glue Job (1)](https://github.com/GustavoGuarany/projeto-ed-tv-jornalismo/assets/126171692/12b86413-927b-4791-9376-6db847c8a65e)
<br>

## Desafios e potenciais impactos 
1. Garantia da integridade e consistência dos dados
2. Otimização do desempenho dos recursos
3. Segurança dos dados durante todo o fluxo
4. Identificação dos repórteres mais ativos
5. Analise dos locais das matérias e as cidades com maior cobertura
6. Distribuição de tipos de matérias
7. Identificação de cinegrafistas e produtores mais ativos
8. Análise temporal: identificação de padrões sazonais, quantidade e tipos de matérias por período 
9. Identificação da subutilização do sistema
<br>

 
## Backup do SQL Server 
![MicrosoftSQLServer](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft%20sql%20server&logoColor=white)	![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

![sql-server-jupyter-postgres](https://github.com/GustavoGuarany/projeto-engenharia-dados-tv-jornalismo/assets/126171692/6c58c6b7-4e4d-4cd4-80a8-248900800aac)

1. Docker
[Instalação do docker em ambiente windows](https://docs.docker.com/desktop/install/windows-install/)

2. Criação de um container docker para instalar o sql server e restaurar o backup do banco de dados.

Pull da imagem de contêiner do SQL Server mais recente.
```console
docker pull mcr.microsoft.com/mssql/server:2022-latest
```
3. Criação do contêiner docker SQL Server usando a imagem
```console
docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=sua_senha_aqui' \
   -p 1433:1433 --name meu-sql-server \
   -v sql1data:/var/opt/mssql\
   -d mcr.microsoft.com/mssql/server:2022-latest
```
4. Movendo o arquivo de backup para o contêiner
```console
docker cp /path/to/database.bak  sql_server_conteiner_id:/var/opt/mssql/data/database.bak
```
5. Interagindo com o conteiner em execução.
```console
docker exec -it conteiner_id /bin/bash
```
6. Restaurando o banco de dados utilizando a ferramenta de linha de comando 'sqlcmd'.
```console
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "sua_senha"

RESTORE DATABASE database FROM DISK = 'database.bak'
GO
```
<br>

## Criação de uma instância do RDS Postgres 
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)

Utilização do terraform para provisionamento de recursos e gerenciamento da infraestrutura.
* [Tutorial instalção do Terraform no Windows](https://github.com/GustavoGuarany/terraform/blob/main/README.md)

> ➡️ **[Códigos Terraform](https://github.com/GustavoGuarany/projeto-engenharia-dados-tv-jornalismo/tree/master/Terraform)**
<br>
  
## Migração dos dados do banco Sql Server no Docker para RDS Postgres 
[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)](https://jupyter.org/try)![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white)

Migração de dados de um banco SQL Server rodando no contêiner Docker para um banco PostgreSQL na AWS RDS.<br><br>
`Python`<br>
`Bibliotecas pyodbc, pandas e sqlalchemy.`<br><br>

**Código Migração SQL Server para o RDS** ⬇️
<details>

<summary>migration-sql-server-rds-postgres.py</summary>

```python
import pyodbc
import pandas as pd
import pymysql
from sqlalchemy import create_engine

#Estabelecendo conexão com o banco de dados no docker
server = 'server' 
database = 'db' 
username = 'username' 
password = '*****'  
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

#Extraindo somente as tabelas que serão utilizadas
query_materia = "SELECT * FROM materia;"
df_materia = pd.read_sql(query_materia, cnxn)

query_usuario = "SELECT * FROM usuario;"
df_usuario = pd.read_sql(query_usuario, cnxn)

query_muni = "SELECT * FROM municipio;"
df_muni = pd.read_sql(query_muni, cnxn)

query_tm = "SELECT * FROM tipomateria;"
df_tm = pd.read_sql(query_tm, cnxn)

query_edi = "SELECT * FROM editoria;"
df_edi = pd.read_sql(query_edi, cnxn)

#Fazendo a ingestão no banco postgre do RDS da AWS
engine = create_engine('postgresql://postgres:*****@db.url:porta/banco')
#Dataframes que serão inseridos
dataframes = [df_materia, df_usuario, df_muni, df_tm, df_edi]
#Nomeando as tabelas
nomes_tabelas = ['dbo_materia', 'dbo_usuario','dbo_municipio','dbo_tipomateria','dbo_editoria']
#Inteirando nos dataframes e inserindo os dados no rds
for df, tabela in zip(dataframes, nomes_tabelas):
    df.to_sql(tabela, engine, if_exists='replace')

```

</details>
<br>

 
## Migração dos dados do RDS para S3 com DMS 
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white) 

Cada etapa será realizada via códigos Terraform

Para realizar a migração dos dados da instância RDS para o S3 usando o AWS DMS (Data Migration Service), seguiremos algumas etapas.
1. Configuração do IAM: Criação de uma função de IAM que o AWS DMS utilize para acessar o bucket do S3
2. Criação da instância de replicação do DMS: Será responsável por gerenciar a migração do dados
3. Criação do endpoint de origem no DMS: Será a conexão com a instância do RDS
4. Criação do endpoint de destino no DMS: Será a conexão com o bucket S3
5. Criação de uma tarefa de migração no DMS: A tarefa usará a instância de replicação, o endpoint de origem e o endpoint de destino para migrar os dados

Após a criação e iniciação da tarefa de migração, o AWS DMS começará a migrar os dados do seu banco de dados RDS para o bucket S3


> ➡️ **[Códigos Terraform](https://github.com/GustavoGuarany/projeto-engenharia-dados-tv-jornalismo/tree/master/Terraform)**
<br>
 
## Transformação dos dados com AWS Glue  
⚙️  Preparação e o carregamento dos dados para análise.

**Etapas**
* job ETL: execução do script python    
    + Extração: obtenção do dados brutos
    + Transformação, limpeza dos dados, remoção de duplicatas, preenchimento de valores ausentes, modelagem, normalização, agregação de dados.
    + Limpeza e validação, verificação de consistência, integridade e validade
    + Carregamento dos dados no destino final
* Crawler
    + Definição de um crawler para rastrear os dados, criar um banco dentro do catalogo de dados.
    + Crawler name : crawler-tvnews
    + Crawler soucer type: Data stores
    + Repeat crawls od s3 data stores: crawl all folders
    + Escolha um datastore: S3
    + conexão: sem conexão
    + Rastrear dados no > Caminho especificado na minha conta: s3a://tvnews-curated-prod/tvnews-full
    + Função do IAM: Crie uma função do IAM: tvnews-role-crawler
    + Frequência: Executar sob demanda
    + Banco de dados: database
    + Prefixo adicionados a tabelas: crawler_tvnews_
    + Opções de configuração: Atualizar a definição da tabela no catálogo de dados
    + Como o AWS Glue deve lidar com a exclusão de objetos no datastore?: Marcar a tabela como suspensa no catálogo de dados
    + Execução do crawler criado
    + Dados disponiveis no Athena
<br>

**Código Glue job** ⬇️
<details>

<summary>glue-job-tvnews.py</summary>

```python
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

-- setup da aplicação Spark
spark = SparkSession \
    .builder \
    .appName("job-glue-spark-tvnews") \
    .getOrCreate()

-- definindo o método de logging da aplicação use INFO somente para DEV [INFO,ERROR]
spark.sparkContext.setLogLevel("ERROR")

df_mat = spark.read.format("csv")\
    .option("header", "True")\
    .option("inferSchema","True")\
    .csv("s3a://tvnews-landing-prod/materia.csv")
df_usu = spark.read.format("csv")\
    .option("header", "True")\
    .option("inferSchema","True")\
    .csv("s3a://tvnews-landing-prod/usuarios.csv")
df_edi = spark.read.format("csv")\
    .option("header", "True")\
    .option("inferSchema","True")\
    .csv("s3a://tvnews-landing-prod/editoria.csv")
df_muni = spark.read.format("csv")\
    .option("header", "True")\
    .option("inferSchema","True")\
    .csv("s3a://tvnews-landing-prod/municipio.csv")
df_tpmat = spark.read.format("csv")\
    .option("header", "True")\
    .option("inferSchema","True")\
    .csv("s3a://tvnews-landing-prod/tipomateria.csv") 


-- converte para formato parquet
print ("\nEscrevendo os dados lidos da raw para parquet na processing zone...")
df_mat.write.format("parquet")\
        .mode("overwrite")\
        .save("s3a://tvnews-processed-prod/dbo_materia.parquet")
df_usu.write.format("parquet")\
        .mode("overwrite")\
        .save("s3a://tvnews-processed-prod/dbo_usuario.parquet")
df_edi.write.format("parquet")\
        .mode("overwrite")\
        .save("s3a://tvnews-processed-prod/dbo_editoria.parquet")
df_muni.write.format("parquet")\
        .mode("overwrite")\
        .save("s3a://tvnews-processed-prod/dbo_municipio.parquet")
df_tpmat.write.format("parquet")\
        .mode("overwrite")\
        .save("s3a://tvnews-processed-prod/dob_tipomateria.parquet")

-- lendo arquivos parquet
df_mat_parquet = spark.read.format("parquet")\
 .load("s3a://tvnews-processed-prod/dbo_materia.parquet/*.parquet")
df_usu_parquet = spark.read.format("parquet")\
 .load("s3a://tvnews-processed-prod/dbo_usuario.parquet/*.parquet")
df_edi_parquet = spark.read.format("parquet")\
 .load("s3a://tvnews-processed-prod/dbo_editoria.parquet/*.parquet")
df_muni_parquet = spark.read.format("parquet")\
 .load("s3a://tvnews-processed-prod/dbo_municipio.parquet/*.parquet")
df_tpmat_parquet = spark.read.format("parquet")\
 .load("s3a://tvnews-processed-prod/dob_tipomateria.parquet/*.parquet")

-- Selecionando apenas as colunas necessarias dos dataframes
df_usu_parquet = df_usu_parquet.select('CODUSUARIO', 'US_NOME')
df_muni_parquet = df_muni_parquet.select('CODMUNICIPIO', 'MU_NOME')
df_edi_parquet = df_edi_parquet.select('CODEDITORIA', 'ED_DESCRICAO')
df_tpmat_parquet = df_tpmat_parquet.select('CODTIPOMATERIA', 'TM_DESCRICAO')

-- Substituindo o codigo dos reportes, produtores, cinegrafistas pelo nome
df_joined = df_mat_parquet.join(df_usu_parquet, df_mat_parquet.CODREPORTER == df_usu_parquet.CODUSUARIO, 'left').withColumnRenamed('US_NOME', 'REPORTER').withColumnRenamed('CODUSUARIO', 'CODREPORTER_')
df_joined = df_joined.join(df_usu_parquet, df_mat_parquet.CODPRODUTOR == df_usu_parquet.CODUSUARIO, 'left').withColumnRenamed('US_NOME', 'PRODUTOR').withColumnRenamed('CODUSUARIO', 'CODPRODUTOR_')
df_joined = df_joined.join(df_usu_parquet, df_mat_parquet.CODCINEGRAFISTA == df_usu_parquet.CODUSUARIO, 'left').withColumnRenamed('US_NOME', 'CINEGRAFISTA').withColumnRenamed('CODUSUARIO', 'CODPRODUTOR_')

-- Substituindo o codigo dos municipios, editoria, tipo da materia por seus respectivos nomes
df_joined = df_joined.join(df_muni_parquet, df_mat_parquet.CODMUNICIPIO == df_muni_parquet.CODMUNICIPIO, 'left').withColumnRenamed('MU_NOME', 'MUNICIPIO').withColumnRenamed('CODMUNICIPIO', 'CODREPORTER_')\
                     .join(df_edi_parquet, df_mat_parquet.CODEDITORIA == df_edi_parquet.CODEDITORIA, 'left').withColumnRenamed('ED_DESCRICAO', 'EDITORIA').withColumnRenamed('CODEDITORIA', 'CODEDITORIA_')\
                     .join(df_tpmat_parquet, df_mat_parquet.CODTIPOMATERIA == df_tpmat_parquet.CODTIPOMATERIA, 'left').withColumnRenamed('TM_DESCRICAO', 'TIPO_MATERIA').withColumnRenamed('CODTIPOMATERIA', 'CODTIPOMATERIA_')

df_soft = df_joined.select('CODMATERIA', 'PRODUTOR','REPORTER','CINEGRAFISTA','MUNICIPIO','TIPO_MATERIA','EDITORIA','MA_DATA','MA_LOCAL','MA_RETRANCA')

df_soft = df_soft.withColumn("MA_LOCAL", when(col("MA_LOCAL") == 'POLÍCIA', 'DELEGACIA').otherwise(col("MA_LOCAL")))\
                   .withColumn("MA_LOCAL", when(col("MA_LOCAL") == 'POLICIA', 'DELEGACIA').otherwise(col("MA_LOCAL")))\
                   .withColumn("MA_LOCAL", when(col("MA_LOCAL") == 'ESTÁDIO BARBALHÃO', 'ESTÁDIO ').otherwise(col("MA_LOCAL")))\
                   .withColumn("MA_LOCAL", when(col("MA_LOCAL") == 'COLOSSO DO TAPAJÓS', 'ESTÁDIO ').otherwise(col("MA_LOCAL")))\
                   .withColumn("MA_LOCAL", when(col("MA_LOCAL") == 'CÂMARA', 'CÂMARA DE VEREADORES').otherwise(col("MA_LOCAL")))

-- Limpeza na coluna MA_LOCAL 
df_final = df_soft.withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('X{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('\.{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('\,{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('\\*,{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('Z{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('\;{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('-{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))


-- Crie uma lista das palavras que você deseja substituir
palavras_para_substituir = [ 'NA PAURTA',r'\bS\b',r'\bN PAUTA\b',r'\b-\b','NA PAUTA', r'\b//\b','NA PAUTA//','SANTARÉM','SANTAREM','TV','STM','VÁRIOS','///','/','VER PAUTA','VER PAUTA','INDEFINIDO',r'\bRUA\b','VER NA PAUTA','RUAS','A DEFINIR','\\.', r'\b;\b', r'\bVÍDEO\b','\\*+',r'\bR\b',r'\bRR\b','RRR','SSSS',r'\bD\b','AAA',r'\bAA\b','////','SSS',r'\bSS\b',r'\bQ\b',r'\bVARIOS\b','LLLL','NA ´PAUTA','N APAUTA','NA OPAUTA','GGG','NA PAUTAS']  # note que estamos escapando o ponto

-- Crie a expressão regular
regex = '|'.join(palavras_para_substituir)

-- Substitua a coluna se ela contiver qualquer uma das palavras na lista
df_final = df_final.withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike(regex), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))

df_final.show(truncate=False)

df_final.repartition(1)\
          .write\
          .format("parquet")\
          .mode("overwrite")\
          .save("s3a://tvnews-curated-prod/tvnews-full.parquet/*.parquet")
```
</details>
<br>
   
O processo de ETL pode ser contínuo, permitindo que os dados sejam atualizados e refinados ao longo do tempo.

<br><br>

![crawler](https://github.com/GustavoGuarany/projeto-ed-tv-jornalismo/assets/126171692/76835da7-01bb-45fb-9763-9b7fb20ca9ec)

<br><br>

## Armazenamento dos dados processados no S3 

🌐 Os dados serão organizados e armazenados em três buckets distintos: Landing, Processing e Curated, todos integrantes de um sistema de Data Lake.

> 🪣 **Bucket Landing**: O armazenamento dos dados em seu estado bruto, em formato csv, sem nenhum tipo de manipulação ou processamento.

> 🪣 **Bucket Processing**: Armazena os dados convertidos para o formato Parquet.

> 🪣 **Bucket Curated**: Armazena o resultado final do processo de ETL, nessa etapa, os dados já foram limpos, transformados, validados, modelados e estão prontos para serem consumidos e usados para gerar valor para a organização.

Em conjunto, esses três buckets formam a estrutura do Data Lake, permitindo um fluxo de dados eficiente e bem organizado, que facilita a manipulação, análise e utilização desses dados

**Buckets Provisionados via Terraform**
> ➡️ **[Códigos Terraform](https://github.com/GustavoGuarany/projeto-engenharia-dados-tv-jornalismo/tree/master/Terraform)**
<br>

## Consulta dos dados com o AWS Athena 

⚡ Serviço interativo de consultas que facilita a análise de dados diretamente no Amazon S3 usando SQL padrão

Após a execução do crawler o aws glue cria uma tabela no AwsDataCatalog e essa tabela fica disponível no editor do Athena.

Configurações > Manage Settings > Direcione o resultado das consultas para o backet athena-query-tvnews

<br><br>

**Código para consultar as tabelas diretamente no Athena** ⬇️
<details>
<summary>querys-athena-tvnews.sql</summary>
    
```sql
-- Consultando as editorias com mais ocorrencias em 2022
SELECT extract(year from MA_DATA) AS ANO, EDITORIA, COUNT(*) AS TOTAL
FROM crawler_bucket_tvnews_prod
WHERE extract(year from MA_DATA) = 2022
GROUP BY extract(year from MA_DATA), EDITORIA
ORDER BY TOTAL DESC

-- Reporter que mais colaborarão no ano de 2023
WITH data AS (
  SELECT extract(year from MA_DATA) AS ANO, REPORTER
  FROM crawler_bucket_tvnews_prod
)
SELECT ANO, REPORTER, COUNT(*) AS TOTAL
FROM data
WHERE ANO = 2023
GROUP BY ANO, REPORTER
ORDER BY TOTAL DESC

-- Reporter e cinegrafista que mais trabalharam juntos no ano de 2023
WITH data AS (
  SELECT extract(year from MA_DATA) AS ANO, REPORTER, CINEGRAFISTA
  FROM dados
)
SELECT REPORTER, CINEGRAFISTA, COUNT(*) AS TOTAL
FROM data
WHERE ANO = 2023
GROUP BY REPORTER, CINEGRAFISTA
ORDER BY TOTAL DESC
LIMIT 10

-- Repórter e editoria e ordenados em ordem decrescente pelo número total de matérias
WITH data AS (
  SELECT extract(year from MA_DATA) AS ANO, REPORTER, EDITORIA
  FROM dados
)
SELECT REPORTER, EDITORIA, COUNT(*) AS TOTAL_MAT
FROM data
WHERE ANO = 2023
GROUP BY REPORTER, EDITORIA
ORDER BY TOTAL_MAT DESC
```

</details>

<br>

![tela-athena_borra](https://github.com/GustavoGuarany/projeto-ed-tv-jornalismo/assets/126171692/f3f7302d-be59-443a-9a75-1fa0333c8d5c)

<br>
 
## Visualização dos dados com Power BI

![Power Bi](https://img.shields.io/badge/power_bi-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

 📊 📈 Setup Athena + Power BI
 <br>
* Conexão ao Amazon Athena com ODBC
    + Baixar Simba Athena ODBC Driver
        + Fonte de dados ODBC >> DSN de Sistema >> Simba Athena ODBC drive >> Configurar o Simba com os dados corretos >> configurar as opções de autenticação >> No Power BI >> Obter dados >> ODBC >> DNS 
<br>

**Visualizações**

![tela-01-powerbi_borra](https://github.com/GustavoGuarany/projeto-ed-tv-jornalismo/assets/126171692/b4687189-01be-4219-86a5-d61659bd4402)

<br><br>

![tela-02-powerbi_borra](https://github.com/GustavoGuarany/projeto-ed-tv-jornalismo/assets/126171692/8efad900-5b42-4085-907a-0692b5afafb5)

<br><br>

![tela-03-powerb_borra](https://github.com/GustavoGuarany/projeto-ed-tv-jornalismo/assets/126171692/6a90a8be-d3de-4412-b2f8-1aab66dedf80)

<br><br>








