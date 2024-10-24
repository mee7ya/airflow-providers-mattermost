FROM apache/airflow:2.10.2
COPY dist/airflow_providers_mattermost-* .
RUN pip install --find-links=. airflow_providers_mattermost