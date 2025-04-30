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

## Docker init & run

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
  - 1 postgres database
  - 1 redis message queue
- Issues on startup:
  - redis is unhealthy for some reason
    - fixed by adding `ALLOW_EMPTY_PASSWORD=yes` as environment variable in `docker-compose.yml`
  - Now api-server failed to start due to authentication manager not configured [FIX]
    - seems like due to `No module named 'airflow.providers.fab'`
- We can now login on `localhost:8080` with the `airflow` default credentials

---

## Tutorials

- Continue from https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html

---
