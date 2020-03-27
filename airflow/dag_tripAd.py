from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

def print_hello():
    return 'Hello world!'

dag = DAG('dag_tripAD', description='TripAdvisor_pipeline_test',
          start_date=datetime(2020, 3, 13), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)

scrapingTripAd_operator = BashOperator(
    task_id='scrapingTripAd',
    bash_command='python ~/web_scraping/src/scrapeTripadvisor.py ~/web_scraping/input/address.txt ~/web_scraping/output/tpd_insert.csv',
    dag=dag
)

loading_operator = BashOperator(
    task_id='loading_to_mysql',
    bash_command='python ~/web_scraping/src/connectMysql.py ~/web_scraping/output/tpd_insert.csv',
    dag=dag
)

dummy_operator >> scrapingTripAd_operator >> loading_operator
dummy_operator >>hello_operator