import os
from pyspark.sql import SparkSession

# Criar uma SparkSession com as configurações para MinIO
spark = (
    SparkSession
    .builder.appName("Minio_stage_data")
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

# Manually Create Data
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

# Criar DataFrame a partir dos dados
df = spark.createDataFrame(data)

# Caminho para o bucket do MinIO (usando a sintaxe s3a://)
bucket_path = "s3a://stage-sandbox01/dados_fake/fake_data.csv"

# Gravar o DataFrame como CSV no MinIO
df.write.csv(bucket_path, mode="overwrite", header=True)