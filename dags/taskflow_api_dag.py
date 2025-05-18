import json

from airflow.decorators import dag, task

@dag(
    schedule = None,
    tags = ["personal", "example"]
)
def taskflow_api_dag():
    """
        ### Taskflow API DAG
        This is a simple data pipeline example which demonstrates the use of
        the TaskFlow API using three simple tasks for Extract, Transform, and Load.
        Documentation that goes along with the Airflow TaskFlow API tutorial is
        located
    """

    @task()
    def extract():
        """
            #### Extract task
             A simple Extract task to get data ready for the rest of the data
            pipeline. In this case, getting data is simulated by reading from a
            hardcoded JSON string.
        """
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        order_data_dict = json.loads(data_string)
        return order_data_dict
    
    @task()
    def transform(order_data_dict: dict):
        """
            #### Transform task
            A simple Transform task which takes in the collection of order data and
            computes the total order value.
        """
        total_order_val = 0
        for value in order_data_dict.values():
            total_order_val += value
        return total_order_val
    
    @task()
    def load(total_order_value: float):
        """
        #### Load task
        A simple Load task which takes in the result of the Transform task and
        instead of saving it to end user review, just prints it out.
        """
        print(f"Total order value is: {total_order_value:.2f}")
    
    order_data = extract()
    total_order_value = transform(order_data)
    load(total_order_value)

taskflow_api_dag()
