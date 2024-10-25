from typing import TYPE_CHECKING

from airflow.notifications.basenotifier import BaseNotifier

from airflow_providers_mattermost.hooks import MattermostHook

if TYPE_CHECKING:
    from airflow.utils.context import Context


class MattermostNotifier(BaseNotifier):
    template_fields = ['message', 'props']
    hook = MattermostHook

    def __init__(
        self,
        conn_id: str,
        channel: str,
        message: str,
        username: str | None = None,
        icon_url: str | None = None,
        icon_emoji: str | None = None,
        type_: str | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__()
        self.conn_id = conn_id
        self.channel = channel
        self.message = message
        self.username = username
        self.icon_url = icon_url
        self.icon_emoji = icon_emoji
        self.type_ = type_
        self.props = props

    def notify(self, context: 'Context') -> None:
        self.hook(self.conn_id).run(
            channel=self.channel,
            message=self.message,
            username=self.username,
            icon_url=self.icon_url,
            icon_emoji=self.icon_emoji,
            type_=self.type_,
            props=self.props,
        )
