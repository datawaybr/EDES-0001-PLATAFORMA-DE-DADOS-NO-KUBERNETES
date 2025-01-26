from pyspark.sql import SparkSession
from delta import *

# Configuração da Sessão do Spark
# Dependencias do Delta + configuracoes de log
spark = (
    SparkSession
    .builder
    .master("local[*]")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.databricks.delta.retentionDurationCheck.enabled", "true")
    .config("spark.databricks.delta.checkpointInterval", "10")
    .config("spark.delta.logLevel", "DEBUG")
    .getOrCreate()
)

# Dados de criacao manual com 10 registros
data = [
    {"id": 1, "name": "Alice Johnson", "email": "alice.johnson@example.com", "address": "123 Maple St, Springfield, IL", "age": 28, "join_date": "2021-03-01"},
    {"id": 2, "name": "Bob Smith", "email": "bob.smith@example.com", "address": "456 Oak St, Metropolis, NY", "age": 35, "join_date": "2020-07-15"},
    {"id": 3, "name": "Charlie Brown", "email": "charlie.brown@example.com", "address": "789 Pine St, Gotham, MA", "age": 42, "join_date": "2019-10-10"},
    {"id": 4, "name": "Diana Prince", "email": "diana.prince@example.com", "address": "101 Elm St, Star City, CA", "age": 30, "join_date": "2022-01-22"},
    {"id": 5, "name": "Eve Adams", "email": "eve.adams@example.com", "address": "202 Birch St, Central City, TX", "age": 26, "join_date": "2023-05-18"},
    {"id": 6, "name": "Frank Castle", "email": "frank.castle@example.com", "address": "303 Cedar St, Coast City, FL", "age": 50, "join_date": "2018-11-11"},
    {"id": 7, "name": "Grace Lee", "email": "grace.lee@example.com", "address": "404 Walnut St, Keystone, PA", "age": 33, "join_date": "2019-09-09"},
    {"id": 8, "name": "Henry Ford", "email": "henry.ford@example.com", "address": "505 Cherry St, Smallville, KS", "age": 45, "join_date": "2021-04-05"},
    {"id": 9, "name": "Ivy Green", "email": "ivy.green@example.com", "address": "606 Ash St, Emerald City, WA", "age": 29, "join_date": "2020-02-20"},
    {"id": 10, "name": "Jack White", "email": "jack.white@example.com", "address": "707 Willow St, Hill Valley, CO", "age": 38, "join_date": "2023-06-30"}
]

# Criando dataframe e gerando uma view temporaria
df = (
        spark.createDataFrame(data)
             .createOrReplaceTempView('fakedata')
    )

print("== Selecionando 5 registros da View Temporaria")
query = """
    SELECT * FROM fakedata LIMIT 5
"""
spark.sql(query).show()
print("===============================================")

# Criacao da tabela delta utilizando o filesystem do proprio container
print("== Criação da Tabela Delta Localmente")
query = """
    CREATE OR REPLACE TABLE tb_fake_data USING DELTA LOCATION '/tmp/tb_fake_data'
    AS SELECT
        id AS id_user,
        name AS nm_usuario,
        email AS nm_email,
        address AS nm_endereco,
        age AS num_idade,
        join_date AS dt_criacao
       FROM fakedata
"""
spark.sql(query)
print("===============================================")

# Selecionando 5 registros a partir da tabela delta pelo filesystem
print("== Selecionando 5 registros a partir da Tabela Delta Criada")
query = """
    SELECT
        *
    FROM tb_fake_data
    LIMIT 5
"""
spark.sql(query).show()
print("===============================================")