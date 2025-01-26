import os
from pyspark.sql import SparkSession

# Criar uma SparkSession com as configurações para MinIO
spark = (
    SparkSession
    .builder.appName("Minio_raw_data")
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
bucket_path = "s3a://stage-sandbox01/dados_fake/fake_data.csv"

# Leitura do CSV no MinIO
df = (
    spark.read.csv(bucket_path, header=True)
         .createOrReplaceTempView('fakedata')
)

print("===============================================")

print("== Criação da Tabela Delta Localmente")
query = """
    CREATE OR REPLACE TABLE tb_fake_data USING DELTA LOCATION 's3a://raw-sandbox01/delta/tb_fake_data'
    AS SELECT
        id,
        name,
        email,
        address,
        age,
        join_date
       FROM fakedata
"""
spark.sql(query)
print("===============================================")