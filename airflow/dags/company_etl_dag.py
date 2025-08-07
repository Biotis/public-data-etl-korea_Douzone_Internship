from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# src 폴더 경로를 PYTHONPATH에 추가
dag_path = os.path.abspath(os.path.dirname(__file__))
src_path = os.path.join(dag_path, '..', '..', 'src')
sys.path.append(os.path.abspath(src_path))

# src 내 모듈 import
from collect.dart_collector import extract_and_save_data
from proprecessing.proprecessed import standardize_company_data
from validate.validator import validate_biz_numbers
from transform.transformer import transform_with_metadata
from export.exporter import export_to_csv

from config import DART_API_KEY, NTS_API_KEY, DATA_PATH, BATCH_SIZE


default_args = {
    'owner': 'seungil',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'company_etl_pipeline',
    default_args=default_args,
    description='기업 마스터 데이터 ETL 파이프라인',
    schedule='@weekly',
    catchup=False,
    tags=['ETL', 'biznum']
)

t1 = PythonOperator(
    task_id='collect_data',
    python_callable=lambda: extract_and_save_data(
        api_key=DART_API_KEY, 
        start_index=0, 
        end_index=BATCH_SIZE, 
        filename=f"{DATA_PATH}raw_dart_data.xlsx"
    ),
    dag=dag
)

t2 = PythonOperator(
    task_id='standardize_data',
    python_callable=lambda: standardize_company_data(
        f"{DATA_PATH}raw_dart_data.xlsx",
        f"{DATA_PATH}proprecessed_company_data.xlsx"
    ),
    dag=dag
)

t3 = PythonOperator(
    task_id='validate_data',
    python_callable=lambda: validate_biz_numbers(
        f"{DATA_PATH}proprecessed_company_data.xlsx",
        f"{DATA_PATH}validated_company_data.xlsx",
        NTS_API_KEY
    ),
    dag=dag
)

t4 = PythonOperator(
    task_id='transform_data',
    python_callable=lambda: transform_with_metadata(
        f"{DATA_PATH}validated_company_data.xlsx",
        f"{DATA_PATH}metadata_enriched_data.xlsx"
    ),
    dag=dag
)

t1 >> t2 >> t3 >> t4
