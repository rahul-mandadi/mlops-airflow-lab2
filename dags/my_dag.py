from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator  # Changed
from datetime import datetime
from src.model_development import load_data, build_model, data_preprocessing, print_data_summary
from src.success_email import send_success_email

# Default arguments for DAG
default_args = {
    'owner': 'MLOps Student',
    'start_date': datetime(2025, 1, 1),
    'retries': 0
}

# Create DAG instance using Airflow 3.0 SDK
with DAG(
    'ad_click_prediction_mlops',
    default_args=default_args,
    description='Compare 3 ML models for ad click prediction with automated email reporting',
    catchup=False,
    tags=['advertising', 'classification', 'model-comparison', 'mlops']
) as dag:

    # Task 1: Load Data
    load_data_task = PythonOperator(
        task_id='load_data_task',
        python_callable=load_data,
    )

    # Task 2: Data Summary
    data_summary_task = PythonOperator(
        task_id='data_summary_task',
        python_callable=print_data_summary,
        op_args=[load_data_task.output],
    )

    # Task 3: Data Preprocessing
    data_preprocessing_task = PythonOperator(
        task_id='data_preprocessing_task',
        python_callable=data_preprocessing,
        op_args=[load_data_task.output],
    )

    # Task 4: Separate Data Outputs
    def separate_data_outputs(**kwargs):
        """Retrieve preprocessed data from XCom and return as tuple."""
        ti = kwargs['ti']
        X_train, X_test, y_train, y_test = ti.xcom_pull(task_ids='data_preprocessing_task')
        return X_train, X_test, y_train, y_test

    separate_data_outputs_task = PythonOperator(
        task_id='separate_data_outputs_task',
        python_callable=separate_data_outputs,
    )

    # Task 5: Build and Compare Models
    build_save_model_task = PythonOperator(
        task_id='build_save_model_task',
        python_callable=build_model,
        op_args=[separate_data_outputs_task.output, "ad_click_model.sav"],
    )

    # Task 6: Send Success Email
    task_send_email = PythonOperator(
        task_id='task_send_email',
        python_callable=send_success_email,
    )

    # Set task dependencies
    load_data_task >> data_summary_task >> data_preprocessing_task >> separate_data_outputs_task >> build_save_model_task >> task_send_email