from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# setup da aplicação Spark
spark = SparkSession \
    .builder \
    .appName("job-glue-spark-tvnews") \
    .getOrCreate()

# definindo o método de logging da aplicação use INFO somente para DEV [INFO,ERROR]
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

# imprime os dados lidos da raw
print ("\nImprime os dados lidos da landing:")

# imprime o schema do dataframe
print ("\nImprime o schema do dataframe lido da landing:")

# converte para formato parquet
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

# lendo arquivos parquet
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

#Selecionando apenas as colunas necessarias dos dataframes
df_usu_parquet = df_usu_parquet.select('CODUSUARIO', 'US_NOME')
df_muni_parquet = df_muni_parquet.select('CODMUNICIPIO', 'MU_NOME')
df_edi_parquet = df_edi_parquet.select('CODEDITORIA', 'ED_DESCRICAO')
df_tpmat_parquet = df_tpmat_parquet.select('CODTIPOMATERIA', 'TM_DESCRICAO')

#Substituindo o codigo dos reportes, produtores, cinegrafistas pelo nome
df_joined = df_mat_parquet.join(df_usu_parquet, df_mat_parquet.CODREPORTER == df_usu_parquet.CODUSUARIO, 'left').withColumnRenamed('US_NOME', 'REPORTER').withColumnRenamed('CODUSUARIO', 'CODREPORTER_')
df_joined = df_joined.join(df_usu_parquet, df_mat_parquet.CODPRODUTOR == df_usu_parquet.CODUSUARIO, 'left').withColumnRenamed('US_NOME', 'PRODUTOR').withColumnRenamed('CODUSUARIO', 'CODPRODUTOR_')
df_joined = df_joined.join(df_usu_parquet, df_mat_parquet.CODCINEGRAFISTA == df_usu_parquet.CODUSUARIO, 'left').withColumnRenamed('US_NOME', 'CINEGRAFISTA').withColumnRenamed('CODUSUARIO', 'CODPRODUTOR_')

#Substituindo o codigo dos municipios, editoria, tipo da materia por seus respectivos nomes
df_joined = df_joined.join(df_muni_parquet, df_mat_parquet.CODMUNICIPIO == df_muni_parquet.CODMUNICIPIO, 'left').withColumnRenamed('MU_NOME', 'MUNICIPIO').withColumnRenamed('CODMUNICIPIO', 'CODREPORTER_')\
                     .join(df_edi_parquet, df_mat_parquet.CODEDITORIA == df_edi_parquet.CODEDITORIA, 'left').withColumnRenamed('ED_DESCRICAO', 'EDITORIA').withColumnRenamed('CODEDITORIA', 'CODEDITORIA_')\
                     .join(df_tpmat_parquet, df_mat_parquet.CODTIPOMATERIA == df_tpmat_parquet.CODTIPOMATERIA, 'left').withColumnRenamed('TM_DESCRICAO', 'TIPO_MATERIA').withColumnRenamed('CODTIPOMATERIA', 'CODTIPOMATERIA_')

df_soft = df_joined.select('CODMATERIA', 'PRODUTOR','REPORTER','CINEGRAFISTA','MUNICIPIO','TIPO_MATERIA','EDITORIA','MA_DATA','MA_LOCAL','MA_RETRANCA')

df_soft = df_soft.withColumn("MA_LOCAL", when(col("MA_LOCAL") == 'POLÍCIA', 'DELEGACIA').otherwise(col("MA_LOCAL")))\
                   .withColumn("MA_LOCAL", when(col("MA_LOCAL") == 'POLICIA', 'DELEGACIA').otherwise(col("MA_LOCAL")))\
                   .withColumn("MA_LOCAL", when(col("MA_LOCAL") == 'ESTÁDIO BARBALHÃO', 'ESTÁDIO COLOSSO DO TAPAJÓS').otherwise(col("MA_LOCAL")))\
                   .withColumn("MA_LOCAL", when(col("MA_LOCAL") == 'COLOSSO DO TAPAJÓS', 'ESTÁDIO COLOSSO DO TAPAJÓS').otherwise(col("MA_LOCAL")))\
                   .withColumn("MA_LOCAL", when(col("MA_LOCAL") == 'CÂMARA', 'CÂMARA DE VEREADORES').otherwise(col("MA_LOCAL")))

#Limpeza na coluna MA_LOCAL 
df_final = df_soft.withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('X{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('\.{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('\,{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('\\*,{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('Z{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('\;{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))\
                               .withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike('-{2,}'), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))

# Crie uma lista das palavras que você deseja substituir
palavras_para_substituir = [ 'NA PAURTA',r'\bS\b',r'\bN PAUTA\b',r'\b-\b','NA PAUTA', r'\b//\b','NA PAUTA//','SANTARÉM','SANTAREM','TV','STM','VÁRIOS','///','/','VER PAUTA','VER PAUTA','INDEFINIDO',r'\bRUA\b','VER NA PAUTA','RUAS','A DEFINIR','\\.', r'\b;\b', r'\bVÍDEO\b','\\*+',r'\bR\b',r'\bRR\b','RRR','SSSS',r'\bD\b','AAA',r'\bAA\b','////','SSS',r'\bSS\b',r'\bQ\b',r'\bVARIOS\b','LLLL','NA ´PAUTA','N APAUTA','NA OPAUTA','GGG','NA PAUTAS']  # note que estamos escapando o ponto

# Crie a expressão regular
regex = '|'.join(palavras_para_substituir)

# Substitua a coluna se ela contiver qualquer uma das palavras na lista
df_final = df_final.withColumn('MA_LOCAL', when(col('MA_LOCAL').rlike(regex), 'NAO ESPECIFICADO').otherwise(col('MA_LOCAL')))

df_final.show(truncate=False)

df_final.repartition(1)\
          .write\
          .format("parquet")\
          .mode("overwrite")\
          .save("s3a://tvnews-curated-prod/tvnews-full.parquet/*.parquet")