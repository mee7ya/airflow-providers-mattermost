from airflow.notifications.basenotifier import BaseNotifier
from airflow.utils.context import Context

from airflow_providers_mattermost.hooks import MattermostHook


class MattermostNotifier(BaseNotifier):
    template_fields = [
        'message',
    ]
    hook = MattermostHook

    def __init__(self, conn_id: str, channel: str, message: str) -> None:
        super().__init__()
        self.conn_id = conn_id
        self.channel = channel
        self.message = message

    def notify(self, context: Context) -> None:
        self.hook(self.conn_id).run(channel=self.channel, message=self.message)
