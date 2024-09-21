from typing import Any

import requests
from airflow.hooks.base import BaseHook


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

    def get_conn(self) -> Any:
        # TODO: Sessions
        raise NotImplementedError()

    def send(self, conn_id: str, channel: str, message: str) -> None:
        conn = self.get_connection(conn_id)
        url = f'{conn.schema}://{conn.host}:{conn.port}/hooks/{conn.password}'
        # TODO: Raise error on bad response
        requests.post(
            url,
            json={
                'channel': channel,
                'text': message,
            },
        )
