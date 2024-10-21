# Apache Airflow Mattermost Provider

The package is [Apache Airflow](https://airflow.apache.org/) 
[provider](https://airflow.apache.org/docs/apache-airflow-providers/#provider-packages)
for integrating with [Mattermost](https://mattermost.com/) using 
[webhooks](https://developers.mattermost.com/integrate/webhooks/incoming/)

## Features
* Hook
* Operator
* Notifier

### Hook
Provides custom connection type and sends messages via webhook

![connection](https://github.com/user-attachments/assets/6225ad6a-a83a-4cee-ad32-faeaa0f069a5)

### Operator
To send messages within DAGs, supports templating

```python
from airflow.decorators import dag

from airflow_providers_mattermost.operators import MattermostOperator


@dag(
    dag_id='mattermost_dag'
)
def mattermost():
    send_message_to_mattermost = MattermostOperator(
        task_id='send_message_to_mattermost',
        conn_id='mattermost',
        channel='off-topic',
        message='Hello from {{ dag.dag_id }} in Airflow!'
    )

    send_message_to_mattermost


mattermost()
```

### Notifier
Can be used with `on_*_callbacks` to notify about Task/DAG status

```python
from airflow.decorators import dag

from airflow_providers_mattermost.notifiers import MattermostNotifier
from airflow_providers_mattermost.operators import MattermostOperator


@dag(
    dag_id='mattermost_dag',
    on_success_callback=MattermostNotifier(
        conn_id='mattermost',
        channel='off-topic',
        message='Dag ID: {{ dag.dag_id }} , Run ID: {{ run_id }} has completed',
    ),
    on_failure_callback=MattermostNotifier(
        conn_id='mattermost',
        channel='off-topic',
        message='Dag ID: {{ dag.dag_id }} , Run ID: {{ run_id }} has failed',
    ),
)
def mattermost():
    send_message_to_mattermost = MattermostOperator(
        task_id='send_message_to_mattermost',
        conn_id='mattermost',
        channel='off-topic',
        message='Hello from {{ dag.dag_id }} in Airflow!'
    )

    send_message_to_mattermost


mattermost()
```
