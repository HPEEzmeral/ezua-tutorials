"""
Model Training and Evaluation DAG

This DAG handles the training of multiple models, evaluates their accuracy,
and branches to different paths based on the best model's performance.
"""

from datetime import datetime, timedelta
from random import randint

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator


def choose_best_model(ti) -> str:
    """
    Evaluate model accuracies and choose branch based on best model performance.

    Args:
        ti: Task instance object for XCom access

    Returns:
        str: Task ID to branch to ('accurate' or 'inaccurate')
    """
    accuracies = ti.xcom_pull(task_ids=['training_model_A', 'training_model_B', 'training_model_C'])

    if max(accuracies) > 8:
        return 'accurate'
    return 'inaccurate'


def train_model(model: str) -> int:
    """
    Train a specific model and return its accuracy score.

    Args:
        model: Model identifier

    Returns:
        int: Accuracy score (1-10)
    """
    # In a real scenario, this would contain actual model training logic
    return randint(1, 10)


# Define default arguments for the DAG
default_args = {
    'owner': 'data_science_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id="model_training_pipeline",
    description="Pipeline to train and evaluate multiple machine learning models",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['machine_learning', 'model_training'],
    access_control={'All': {'can_read', 'can_edit', 'can_delete'}},
) as dag:
    # Create training tasks for each model
    training_model_tasks = [
        PythonOperator(
            task_id=f"training_model_{model_id}",
            python_callable=train_model,
            op_kwargs={"model": model_id},
            doc_md=f"Trains model {model_id} and returns an accuracy score between 1-10.",
        )
        for model_id in ['A', 'B', 'C']
    ]

    # Create task to choose the best model
    choosing_best_model = BranchPythonOperator(
        task_id="choosing_best_model",
        python_callable=choose_best_model,
        doc_md="Evaluates model accuracies and branches based on the best model's performance.",
    )

    # Define success path
    accurate = BashOperator(
        task_id="accurate",
        bash_command="echo 'Model accuracy is acceptable. Proceeding with deployment.'",
        doc_md="Executed when at least one model has an accuracy score > 8.",
    )

    # Define failure path
    inaccurate = BashOperator(
        task_id="inaccurate",
        bash_command="echo 'Model accuracy is insufficient. Additional training needed.'",
        doc_md="Executed when all models have accuracy scores ≤ 8.",
    )

    # Define task dependencies
    training_model_tasks >> choosing_best_model >> [accurate, inaccurate]
