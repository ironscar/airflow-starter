# Airflow starter

## Introduction

- Airflow is an open source platform for developing, scheduling and monitoring batch-oriented workloads
- Airflow is not meant for continuously-running, event-driven or streaming workloads
- Airflow workflows are DAGs (Direct Acyclic Graph) defined in Python code
- Airflow is a distributed system with the following components:
  - `scheduler`: monitors all tasks and triggers the task instances once their dependencies are complete
  - `dag-processor`: parses DAG files
  - `webserver`: webserver is available at http://localhost:8080
  - `worker`: executes tasks given by scheduler
  - `triggerer`: runs an event loop for deferrable tasks
  - `init`: initialization service
  - `postgres`: database
  - `redis`: broker that forwards messages from scheduler to worker

---

## Docker setup

- We can use a docker-compose file specified by the official docs and just use our custom images for postgres, redis and airflow
  - make sure with `docker-compose --version` that its major version v2 as the yml might not work with v1
- Before we start airflow, we need to prepare the environment
  - create necessary files and directories
    - create folders for `dags`, `logs`, `plugins` and `config` in `opts/airflow`
    - create a `.env` file in `opts/airflow` with `AIRFLOW_UID=50000` (use `AIRFLOW_UID=$(id -u)` in Linux)
  - initialize the database with `docker-compose up airflow-init`
    - this creates a login with user and password as `airflow`
- This is not suitable for a production deployment
- To clean up and start from scratch if things go wrong
  - Run `docker-compose down --volumes --remove-orphans`
  - Run `docker volume -f prune` for good measure (just in case there are other unused local volumes)
  - Remove the entire source directory

- Now to start airflow, we do `docker-compose up` which creates following containers:
  - 1 airflow-worker
  - 1 airflow-scheduler
  - 1 airflow-webserver
  - 1 airflow-dag-processor
  - 1 postgres database
  - 1 redis message queue
- Issues on startup:
  - redis is unhealthy for some reason
    - fixed by adding `ALLOW_EMPTY_PASSWORD=yes` as environment variable in `docker-compose.yml`
  - Now api-server failed to start due to authentication manager not configured [FIX]
    - seems like due to `No module named 'airflow.providers.fab'`
    - also seems like the FabAuthManager only works for airflow above v2.9.0
    - TRIALS:
      - thus we will use the default `SimpleAuthManager` which is not meant for PROD deployments [FAIL]
      - tried directly running `docker-compose up` without `airflow-init` [FAIL]
      - used airflow 2.10.5 and this issue got fixed [FIX]
  - Invalid choice `api-server`
    - let's change the command on `airflow-apiserver` to `webserver` and rename container accordingly [FIX]
  - Dag-processor keeps restarting (but was able to login for the first time)
    - change `standalone_dag_processor` to `True` because config gets generated with False [FIX]
  - Api-server still showing unhealthy
    - updated health-check to just `http://localhost:8080` and now it creates worker as well [FIX]
  - The command never ends due to the health-checks
    - we can run `docker-compose up -d` [FIX]
      - but using this doesn't log it if we append `> up.log` to above
- We can now login on `localhost:8080` with the `airflow` and `airflow` default credentials
  - turns out we can directly run `docker-compose up` to do everything
    - `airflow-init` is not necessarily required unless it is to generate the `airflow.cfg` file and update the dag_processor config
  - to stop the setup but not remove the containers/volumes, we can run `docker-compose stop`
  - to start everything again, we can run `docker-compose start`
  - it takes about a minute for everything to start up and about 30 seconds longer for the worker to get started (probably because of the health-check though)
    - if the worker doesn't start due to webserver being unhealthy, just run `docker compose run airflow-worker airflow info`

---

## First DAG Run

- Setup a `my_tutorial_dag.py` in dags folder and that automatically updates in all of the containers' `/opt/airflow/dags` which is what is set for `airflow.cfg` dags_folder
- To run airflow commands, we can exec into the containers as `docker exec -it <containerId> /bin/bash`
- Once we did, there were python compilation errors so we fixed it by `pip install apache-airflow-providers-standard` in all the containers except redis and postgres
- Then we restarted all the containers using `docker-compose stop/start` and then it finally shows up on UI
- Now, if we add a new DAG file or a new DAG in same file in host directory, it shows up automatically after refreshing the WEB-UI
- We can delete it from host directory but it doesn't automatically delete on refreshing the WEB-UI (even though its removed from the containers) but we can manually delete it from the WEB-UI
- Changing the DAG file, like the flow of tasks for example, also updates on the UI in some time or we can choose to `Reparse DAG` from the UI
- We can do `Trigger DAG` from WEB-UI and it will run the tasks in the DAG
  - in the graph tab, we can select the corresponding tasks, and then see the XCom tab if there are any return values (including logging from echo command tasks)
  - after selecting the task, going to Details tab, we can also see the task description and other details
- The first DAG was written using the traditional operators like `BashOperator`

---

## Tutorials

### Pythonic DAG with Taskflow API

- The taskflow API is designed to make code simpler and easier to maintain

- Continue from https://airflow.apache.org/docs/apache-airflow/2.10.2/tutorial/taskflow.html

---
