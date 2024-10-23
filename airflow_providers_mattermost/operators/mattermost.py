from airflow.models import BaseOperator
from airflow.utils.context import Context

from airflow_providers_mattermost.hooks import MattermostHook


class MattermostOperator(BaseOperator):
    template_fields = [
        'message',
    ]
    hook = MattermostHook

    def __init__(
        self,
        *,
        conn_id: str,
        channel: str,
        message: str,
        username: str | None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.channel = channel
        self.message = message
        self.username = username

    def execute(self, context: Context) -> None:
        self.hook(self.conn_id).run(
            channel=self.channel, message=self.message, username=self.username
        )
