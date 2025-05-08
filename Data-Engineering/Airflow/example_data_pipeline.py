"""
Sample Airflow DAG

This is a simple example of an Airflow DAG that demonstrates:
1. Basic setup with proper imports
2. Task dependencies
3. Multiple operator types
4. Best practices for DAG configuration
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


def process_data(ti=None):
    """
    A simple Python function that processes data.
    In a real-world scenario, this could perform data transformations.

    Args:
        ti: TaskInstance object automatically passed by Airflow in newer versions
    """
    print("Processing data...")
    # Sample data to pass between tasks
    return {"processed_count": 100}


def analyze_results(ti=None):
    """
    A function that analyzes the results from the previous task.
    Demonstrates using XCom to pass data between tasks.

    Args:
        ti: TaskInstance object automatically passed by Airflow in newer versions
    """
    processed_data = ti.xcom_pull(task_ids='process_data')
    processed_count = processed_data.get('processed_count', 0)

    print(f"Analyzing results for {processed_count} processed items")
    return {"status": "success", "analyzed_count": processed_count}


# Define default arguments for the DAG
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='data_pipeline',
    description='A sample data processing pipeline',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['sample', 'tutorial'],
    access_control={'All': {'can_read', 'can_edit', 'can_delete'}},
) as dag:

    # Start task
    start = EmptyOperator(task_id='start', doc_md="Marks the beginning of the DAG execution")

    # Task to fetch data
    fetch_data = BashOperator(
        task_id='fetch_data',
        bash_command='echo "Fetching data from source..." && sleep 5',
        doc_md="Simulates fetching data from an external source",
    )

    # Task to process data
    process_data = PythonOperator(
        task_id='process_data', python_callable=process_data, doc_md="Processes the fetched data and returns a count"
    )

    # Task to analyze results
    analyze_results = PythonOperator(
        task_id='analyze_results', python_callable=analyze_results, doc_md="Analyzes the processed data"
    )

    # Task to generate report
    generate_report = BashOperator(
        task_id='generate_report',
        bash_command='echo "Generating final report..."',
        doc_md="Generates a report based on the analysis",
    )

    # End task
    end = EmptyOperator(task_id='end', doc_md="Marks the end of the DAG execution")

    # Define the workflow
    start >> fetch_data >> process_data >> analyze_results >> generate_report >> end
