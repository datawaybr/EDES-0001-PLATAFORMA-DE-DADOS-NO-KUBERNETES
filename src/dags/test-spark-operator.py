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
    #'email': ['<seu email aqui>'],
    #'email_on_failure': True,
    #'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}
# [END default_args]

# [START instantiate_dag]
with DAG(
    dag_id='test-spark-operator',
    default_args=default_args,
    schedule_interval=None,
    tags=['Test', 'Spark-Operator'],
    catchup=False
) as dag:
    # Se Comunica com o Spark Operator através da connection criada na UI
    # O Spark Operator submete a aplicação via parametros do manifesto
    # O Airflow tem permissão pra observar o namespace do spark operator
    job_spark_demo = SparkKubernetesOperator(
        task_id='job_spark_demo',
        kubernetes_conn_id='kubernetes_minikube_conn',
        namespace='operator',
        application_file='/util/spark/spark-demo-manifest.yaml',
        do_xcom_push=False,
    )

    cccc = SparkKubernetesOperator(
        task_id='job_spark_demo',
        kubernetes_conn_id='kubernetes_minikube_conn',
        namespace='operator',
        application_file='/util/spark/spark-demo-manifest.yaml',
        do_xcom_push=False,
    )

    bbbb = SparkKubernetesOperator(
        task_id='job_spark_demo',
        kubernetes_conn_id='kubernetes_minikube_conn',
        namespace='operator',
        application_file='/util/spark/spark-demo-manifest.yaml',
        do_xcom_push=False,
    )
# [END instantiate_dag]

# [START task_sequence]
job_spark_demo
# [END task_sequence]