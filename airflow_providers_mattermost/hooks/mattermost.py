from typing import Any

from airflow.hooks.base import BaseHook


class MattermostHook(BaseHook):
    conn_name_attr = 'mattermost_conn_id'
    default_conn_name = 'mattermost_default'
    conn_type = 'mattermost'
    hook_name = 'Mattermost'

    @classmethod
    def get_ui_field_behaviour(cls) -> dict[str, Any]:
        return {
            'hidden_fields': ['login', 'schema', 'extra'],
            'relabeling': {
                'password': 'Webhook Key',
            },
        }
