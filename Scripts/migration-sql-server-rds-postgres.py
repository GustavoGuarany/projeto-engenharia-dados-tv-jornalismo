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
