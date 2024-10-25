import logging
from typing import Any

from airflow.hooks.base import BaseHook
from requests import Request, Session

log = logging.getLogger(__name__)


class MattermostHook(BaseHook):
    conn_name_attr = 'mattermost_conn_id'
    default_conn_name = 'mattermost_default'
    conn_type = 'mattermost'
    hook_name = 'Mattermost'

    @classmethod
    def get_connection_form_widgets(cls) -> dict[str, Any]:
        return super().get_connection_form_widgets()

    @classmethod
    def get_ui_field_behaviour(cls) -> dict[str, Any]:
        return {
            'hidden_fields': ['login', 'extra'],
            'relabeling': {
                'password': 'Webhook Key',
            },
        }

    def __init__(self, conn_id: str, logger_name: str | None = None) -> None:
        super().__init__(logger_name)
        self.conn_id = conn_id

    def get_conn(self) -> tuple[Request, Session]:
        conn = self.get_connection(self.conn_id)
        return Request(
            'POST', f'{conn.schema}://{conn.host}:{conn.port}/hooks/{conn.password}'
        ), Session()

    def run(
        self,
        channel: str,
        message: str,
        username: str | None = None,
        icon_url: str | None = None,
        icon_emoji: str | None = None,
        type_: str | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        if icon_url is not None and icon_emoji is not None:
            log.warning("'icon_emoji' will override 'icon_url'")

        if type_ is not None and not type_.startswith('custom_'):
            raise ValueError("'type_' must start with 'custom_'")

        request, session = self.get_conn()
        with session:
            request.json = {
                'channel': channel,
                'text': message,
                'username': username,
                'icon_url': icon_url,
                'icon_emoji': icon_emoji,
                'type': type_,
                'props': props,
            }
            response = session.send(request.prepare())
        response.raise_for_status()
