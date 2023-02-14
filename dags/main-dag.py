from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.dummy_operator import DummyOperator

from functions.db_connection import connection
from functions.get_data_from_api import getData
from functions.load_time_dim import load_time
from functions.load_report_dim import load_report
from functions.load_loc_dim import load_location
from functions.load_cat_dim import load_category
from functions.load_fact import load_fact
from functions.load_inc_cat import load_inc_cat

myconnection = connection() 
def close_connection():
    myconnection.close()
default_args = {
    'owner' : 'Hazem',
    'start_date': datetime(2023, 1, 30),
    'retries': 0,
    'retry_delay': timedelta(seconds=5)
}

with DAG('crime-analysis', default_args = default_args, schedule_interval='@daily', template_searchpath=['/usr/local/airflow/db_data_airflow/'], catchup=False) as dag:

    # t_create_table = MySqlOperator(task_id="create-table-if-not-exists", mysql_conn_id="mysql_conn", sql="createTable.sql")
    t_fetch_data = PythonOperator(task_id="fetch-data", python_callable=getData, op_kwargs={'connection':myconnection})
    # t_create_connection = PythonOperator(task_id="create_conenction", python_callable=connection)
    # t_load_data = MySqlOperator(task_id="load-data", mysql_conn_id="mysql_conn", sql="loadData.sql")
    t_load_time_dim = PythonOperator(task_id="load_time_dim", python_callable=load_time, op_kwargs={'connection':myconnection})
    t_load_report_dim = PythonOperator(task_id="load_report_dim", python_callable=load_report, op_kwargs={'connection':myconnection})
    t_load_loc_dim = PythonOperator(task_id="load_loc_dim", python_callable=load_location, op_kwargs={'connection':myconnection})
    t_load_cat_dim = PythonOperator(task_id="load_cat_dim", python_callable=load_category, op_kwargs={'connection':myconnection})
    t_dummy1 = DummyOperator(task_id="dummy")
    t_load_fact = PythonOperator(task_id="load_fact", python_callable=load_fact, op_kwargs={'connection':myconnection})
    t_load_inc_cat_dim = PythonOperator(task_id="load_inc_cat", python_callable=load_inc_cat, op_kwargs={'connection':myconnection})
    t_dummy2 = DummyOperator(task_id="dummy2")
    t_close_connection = PythonOperator(task_id="close_connection", python_callable=close_connection)
    t_fetch_data  >> [t_load_time_dim, t_load_report_dim, t_load_loc_dim, t_load_cat_dim] >> t_dummy1 >> [t_load_fact, t_load_inc_cat_dim] >> t_dummy2 >> t_close_connection