# imports
from datetime import datetime, timedelta

# operators
from airflow.providers.standard.operators.bash import BashOperator

# DAG object to instantiate DAGs
from airflow.models.dag import DAG

# init DAG with default arguments passed to every operator (we can override them per task)
with DAG(
    "my_tutorial_dag",
    default_args = {
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    },
    description = "My First Airflow DAG",
    schedule = timedelta(days=1),
    start_date = datetime(2025,5,18),
    catchup = False,
    tags = ["personal","example"]
) as dag:
    # then we create tasks by instantiating operators

    t1 = BashOperator(
        doc_md = "This task prints the date",
        task_id = "print_date",
        bash_command = "date"
    )

    t2 = BashOperator(
        doc_md = "This task makes the job sleep for 5 seconds",
        task_id = "sleep",
        bash_command = "sleep 5"
    )

    t3 = BashOperator(
        doc_md = "This task prints hello world",
        task_id = "print_hello",
        bash_command = "echo 'hello world'"
    )

    # here we define the actual flow of the DAG
    t1 >> t2 >> t3
