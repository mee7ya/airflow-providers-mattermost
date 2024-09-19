FROM apache/airflow:2.10.0
COPY dist/airflow_providers_mattermost-0.1.0-py3-none-any.whl .
RUN pip install airflow_providers_mattermost-0.1.0-py3-none-any.whl