from typing import TYPE_CHECKING

from airflow.notifications.basenotifier import BaseNotifier

from airflow_providers_mattermost.common.types import Priority
from airflow_providers_mattermost.hooks import MattermostHook

if TYPE_CHECKING:
    from airflow.utils.context import Context

    from airflow_providers_mattermost.common.attachments import Attachment


class MattermostNotifier(BaseNotifier):
    """
    Notifier to be used with ``on_x_callback``.

    Shares same params as :class:`.MattermostOperator`
    """

    template_fields = ['message', 'props']
    hook = MattermostHook  #: :meta private:

    def __init__(
        self,
        conn_id: str,
        channel: str,
        message: str,
        attachments: list['Attachment'] | list[dict] | None = None,
        username: str | None = None,
        icon_url: str | None = None,
        icon_emoji: str | None = None,
        type_: str | None = None,
        props: dict[str, str] | None = None,
        priority: Priority = 'standard',
        requested_ack: bool = False,
        persistent_notifications: bool = False,
    ) -> None:
        super().__init__()
        self.conn_id = conn_id
        self.channel = channel
        self.message = message
        self.attachments = attachments
        self.username = username
        self.icon_url = icon_url
        self.icon_emoji = icon_emoji
        self.type_ = type_
        self.props = props
        self.priority = priority
        self.requested_ack = requested_ack
        self.persistent_notifications = persistent_notifications

    def notify(self, context: 'Context') -> None:
        """
        :meta private:
        """

        self.hook(self.conn_id).run(
            channel=self.channel,
            message=self.message,
            attachments=self.attachments,
            username=self.username,
            icon_url=self.icon_url,
            icon_emoji=self.icon_emoji,
            type_=self.type_,
            props=self.props,
            priority=self.priority,
            requested_ack=self.requested_ack,
            persistent_notifications=self.persistent_notifications,
        )
