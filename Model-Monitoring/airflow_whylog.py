import logging
from datetime import datetime
import os
import pandas as pd
import whylogs as why
from whylogs.core.constraints.factories import greater_than_number

from airflow.models.dag import DAG
from airflow.operators.python import get_current_context
from airflow.operators.python import PythonOperator
from whylogs_provider.operators.whylogs import (
    WhylogsConstraintsOperator,
    WhylogsSummaryDriftOperator,
)

def file_path(relative_path):
    dir = os.path.dirname(os.path.abspath(__file__))
    split_path = relative_path.split("/")
    new_path = os.path.join(dir, *split_path)
    return new_path
    
prof_path_target="/mnt/shared/airflow-whylog/profile_wine_target.bin"
prof_path_ref="/mnt/shared/airflow-whylog/profile_wine_ref.bin"
html_path="/mnt/shared/airflow-whylog/Profile_wine.html"

def profile_data_target(data_path=file_path("data/wine.csv")):
    df = pd.read_csv(data_path)
    result = why.log(df)
    result.writer("local").write(dest=prof_path_target)
def profile_data_ref(data_path=file_path("data/wine1.csv")):
    df = pd.read_csv(data_path)
    result = why.log(df)
    result.writer("local").write(dest=prof_path_ref)


with DAG(
    dag_id='whylogs-wine-quality',
    schedule_interval=None,
    start_date=datetime.now(),
    max_active_runs=1,
    tags=['responsible', 'data_transformation'],
) as dag:


    profile_data_target = PythonOperator(task_id="profile_data_target", python_callable=profile_data_target)
    profile_data_ref = PythonOperator(task_id="profile_data_ref", python_callable=profile_data_ref)


    is_in_range = WhylogsConstraintsOperator(
        task_id="is_in_range",
        profile_path=prof_path_target,
        reader="local",
        constraint=greater_than_number(column_name="quality", number=4)
    )
    summary_drift = WhylogsSummaryDriftOperator(
        task_id="drift_report",
        target_profile_path=prof_path_target,
        reference_profile_path=prof_path_ref,
        reader="local",
        write_report_path=html_path
    )

    (
        profile_data_target>>profile_data_ref>>is_in_range>> summary_drift
    )
