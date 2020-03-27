from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

def print_hello():
    return 'Hello world!'

dag = DAG('dag_scrape', description='Simple tutorial DAG',
          start_date=datetime(2017, 3, 20), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)

scraping_operator = BashOperator(
    task_id='scraping',
    bash_command='python ~/web_scraping/src/pullDataFromWebsite.py ~/web_scraping/input/address.txt ~/web_scraping/input/classes.txt ~/web_scraping/output/test1.csv',
    dag=dag
)


dummy_operator >> scraping_operator
dummy_operator >> hello_operator