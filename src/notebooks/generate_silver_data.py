import os
from pyspark.sql import SparkSession

# Criar uma SparkSession com as configurações para MinIO
spark = (
    SparkSession
    .builder.appName("Minio_silver_data")
    # MinIO deps
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk-bundle:1.11.901") # dependencias do minio
    .config("spark.hadoop.fs.s3a.endpoint", "http://dlkdataway-hl.storage:9000") # caminho do service do minio no kubernetes
    .config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID"))
    .config("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY"))
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    # DeltaLake deps
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.databricks.delta.retentionDurationCheck.enabled", "true")
    .config("spark.databricks.delta.checkpointInterval", "10")
    .config("spark.delta.logLevel", "DEBUG")
    # MapReduce warnings
    .config("spark.hadoop.mapreduce.job.metrics.exclude-types", "*") # Evita o warning da não localização do hadoop-metrics
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") # Evita o warning Using standard FileOutputCommitter
    .config("spark.hadoop.mapreduce.outputcommitter.factory.scheme.s3a", "org.apache.hadoop.fs.s3a.commit.S3ACommitterFactory") # Evita o warning Using standard FileOutputCommitter
    .config("spark.hadoop.fs.s3a.committer.name", "directory") # ou 'partitioned' dependendo do caso
    .config("spark.hadoop.fs.s3a.committer.magic.enabled", "true") # Habilite 'true' se estiver usando magic committer
    .getOrCreate()
)

# Caminho para o bucket do MinIO (usando a sintaxe s3a://)
bucket_path = "s3a://raw-sandbox01/delta/tb_fake_data/"

print("== Leitura dos Dados Raw")
# Leitura da tabela Delta
df = (
    spark.read
         .format("delta")
         .load(bucket_path)
         .createOrReplaceTempView('rawdata')
)

print("===============================================")

print("== Criação da Tabela Silver")
query = """
    CREATE OR REPLACE TABLE tb_curated_data USING DELTA LOCATION 's3a://silver-sandbox01/delta/tb_curated_data'
    AS SELECT
        id AS id_user,
        name AS nm_usuario,
        email AS nm_email,
        address AS nm_endereco,
        age AS num_idade,
        join_date AS dt_criacao
       FROM rawdata
"""
spark.sql(query)
print("===============================================")
print("== Finalizando processo")