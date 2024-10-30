from typing import TYPE_CHECKING, Any

from airflow.models import BaseOperator

from airflow_providers_mattermost.common.types import Priority
from airflow_providers_mattermost.hooks import MattermostHook

if TYPE_CHECKING:
    from airflow.utils.context import Context


class MattermostOperator(BaseOperator):
    template_fields = ['message', 'props']
    hook = MattermostHook

    def __init__(
        self,
        *,
        conn_id: str,
        channel: str,
        message: str,
        username: str | None,
        icon_url: str | None = None,
        icon_emoji: str | None = None,
        type_: str | None = None,
        props: dict[str, str] | None = None,
        priority: Priority = 'standard',
        requested_ack: bool = False,
        persistent_notifications: bool = False,
        session_kwargs: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.channel = channel
        self.message = message
        self.username = username
        self.icon_url = icon_url
        self.icon_emoji = icon_emoji
        self.type_ = type_
        self.props = props
        self.priority = priority
        self.requested_ack = requested_ack
        self.persistent_notifications = persistent_notifications
        self.session_kwargs = session_kwargs

    def execute(self, context: 'Context') -> None:
        self.hook(self.conn_id).run(
            channel=self.channel,
            message=self.message,
            username=self.username,
            icon_url=self.icon_url,
            icon_emoji=self.icon_emoji,
            type_=self.type_,
            props=self.props,
            priority=self.priority,
            requested_ack=self.requested_ack,
            persistent_notifications=self.persistent_notifications,
            session_kwargs=self.session_kwargs,
        )
