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


## Overview da solução
![AWS Glue Job (1)](https://github.com/GustavoGuarany/projeto-ed-tv-jornalismo/assets/126171692/12b86413-927b-4791-9376-6db847c8a65e)


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


 
## Backup do SQL Server 
![MicrosoftSQLServer](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft%20sql%20server&logoColor=white)	![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

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


## Criação de uma instância do RDS Postgres 
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)

Utilização do terraform para provisionamento de recursos e gerenciamento da infraestrutura.
* [Tutorial instalção do Terraform no Windows](https://github.com/GustavoGuarany/terraform/blob/main/README.md)
* Código para provisionamento do RDS Postgres via Terraform link:

  
## Migração dos dados do banco Sql Server no Docker para RDS Postgres 
[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)](https://jupyter.org/try)![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white)

Migração de dados de um banco SQL Server rodando no contêiner Docker para um banco PostgreSQL na AWS RDS.<br><br>
`Python`<br>
`Bibliotecas pyodbc, pandas e sqlalchemy.`<br><br>
código python link:

 
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


Códigos terraform link:

 
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


código glue-job-tvnews
   
O processo de ETL pode ser contínuo, permitindo que os dados sejam atualizados e refinados ao longo do tempo.


## Armazenamento dos dados processados no S3 

🌐 Os dados serão organizados e armazenados em três buckets distintos: Landing, Processing e Curated, todos integrantes de um sistema de Data Lake.

> 🪣 **Bucket Landing**: O armazenamento dos dados em seu estado bruto, em formato csv, sem nenhum tipo de manipulação ou processamento.

> 🪣 **Bucket Processing**: Armazena os dados convertidos para o formato Parquet.

> 🪣 **Bucket Curated**: Armazena o resultado final do processo de ETL, nessa etapa, os dados já foram limpos, transformados, validados, modelados e estão prontos para serem consumidos e usados para gerar valor para a organização.

Em conjunto, esses três buckets formam a estrutura do Data Lake, permitindo um fluxo de dados eficiente e bem organizado, que facilita a manipulação, análise e utilização desses dados


## Consulta dos dados com o AWS Athena 

⚡ Serviço interativo de consultas que facilita a análise de dados diretamente no Amazon S3 usando SQL padrão

Após a execução do crawler o aws glue cria uma tabela no AwsDataCatalog e essa tabela fica disponível no editor do Athena.

Configurações > Manage Settings > Direcione o resultado das consultas para o backet athena-query-tvnews

* Código para consultar as tabelas diretamente no Athena.

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

 
## Visualização dos dados com Power BI

 📊 📈 Setup Athena + Power BI
* Conexão ao Amazon Athena com ODBC
    + Baixar Simba Athena ODBC Driver
        + Fonte de dados ODBC >> DSN de Sistema >> Simba Athena ODBC drive >> Configurar o Simba com os dados corretos >> configurar as opções de autenticação >> No Power BI >> Obter dados >> ODBC >> DNS 
               







