#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
This is an example dag for using the KubernetesPodOperator.
"""
import logging

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import \
    KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# log = logging.getLogger(__name__)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'kubernetes_sample',
    default_args=default_args,
    schedule_interval=timedelta(minutes=10),
    tags=['example'],
    access_control={
        'role_hpedemo-user05': {
            'can_read',
            'can_edit'
        }
    }
)

start = DummyOperator(task_id='run_this_first', dag=dag)

python_task = KubernetesPodOperator(namespace='default',
                                    image="python:3.6",
                                    cmds=["python", "-c"],
                                    arguments=["print('hello world')"],
                                    labels={"foo": "bar"},
                                    name="passing-python",
                                    task_id="passing-task-python",
                                    get_logs=True,
                                    dag=dag
                                    )

bash_task = KubernetesPodOperator(namespace='default',
                                  image="ubuntu:16.04",
                                  cmds=["bash", "-cx"],
                                  arguments=["date"],
                                  labels={"foo": "bar"},
                                  name="passing-bash",
                                  # is_delete_operator_pod=False,
                                  task_id="passing-task-bash",
                                  get_logs=True,
                                  dag=dag
                                  )

python_task.set_upstream(start)
bash_task.set_upstream(start)
