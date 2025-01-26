# [START import_module]
from airflow.models import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
# [END import_module]

# [START default_args]
default_args = {
    'owner': 'datawaybr',
    'start_date': datetime(2024, 12, 4),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
# [END default_args]

# [START instantiate_dag]
with DAG(
    dag_id='dag-spark-minio-tables',
    default_args=default_args,
    schedule_interval=None,
    tags=['Minio', 'Spark-Operator', 'DeltaTables'],
    catchup=False
) as dag:
    job_spark_stage = SparkKubernetesOperator(
        task_id='job_spark_stage',
        kubernetes_conn_id='kubernetes_minikube_conn',
        namespace='operator',
        application_file='/util/spark/spark-minio-stage-manifest.yaml',
        do_xcom_push=False,
    )
    job_spark_raw = SparkKubernetesOperator(
        task_id='job_spark_raw',
        kubernetes_conn_id='kubernetes_minikube_conn',
        namespace='operator',
        application_file='/util/spark/spark-minio-raw-manifest.yaml',
        do_xcom_push=False,
    )
    job_spark_silver = SparkKubernetesOperator(
        task_id='job_spark_silver',
        kubernetes_conn_id='kubernetes_minikube_conn',
        namespace='operator',
        application_file='/util/spark/spark-minio-silver-manifest.yaml',
        do_xcom_push=False,
    )
# [END instantiate_dag]

# [START task_sequence]
job_spark_stage >> job_spark_raw >> job_spark_silver
# [END task_sequence]