# https://blog.insightdatascience.com/scheduling-spark-jobs-with-airflow-4c66f3144660
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import boto3
from botocore.client import Config
from airflow.models import Variable

s3 = boto3.resource('s3',
                    endpoint_url=os.getenv('MLFLOW_S3_ENDPOINT_URL'),
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                    config=Config(signature_version='s3v4'),
                    region_name=os.getenv('AWS_DEFAULT_REGION'))

file2count = str(Variable.get("wordcount_filename"))
local_data_dir = '/usr/local/airflow/scripts/data/'

# Define the DAG object
default_args = {
    'owner': 'lpalum',
    'depends_on_past': False,
    'start_date': datetime(2020, 10, 15),
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}
dag = DAG('wordcount', default_args=default_args,
          schedule_interval=timedelta(1))


def read_s3_file(filename):
    return s3.Bucket('data').download_file(filename, local_data_dir + filename)


def write_s3_file(filename):
    s3.Bucket('data').upload_file(local_data_dir + filename, filename)


# [START readfile]
read_the_file = PythonOperator(
    task_id='read_s3_file',
    python_callable=read_s3_file,
    op_kwargs={'filename': file2count},
    dag=dag,
)
# [END readfile]


# [START wordcount]
wordcount = BashOperator(
    task_id='wordcount',
    bash_command='spark-submit --master spark://spark-master:7077 /usr/local/airflow/scripts/wordcount.py /usr/local/airflow/scripts/data/%s' % file2count,
    dag=dag)
# [END wordcount]

# [START writefile]
write_the_file = PythonOperator(
    task_id='write_s3_file',
    python_callable=write_s3_file,
    op_kwargs={'filename': file2count+".out"},
    dag=dag,
)
# [END writefile]


read_the_file >> wordcount >> write_the_file
