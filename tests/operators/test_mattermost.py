from unittest.mock import MagicMock, patch

from airflow_providers_mattermost.operators import MattermostOperator


class TestMattermostOperator:
    operator = MattermostOperator

    @patch.object(operator, 'hook')
    def test_execute(self, patched_hook: MagicMock) -> None:
        operator = self.operator(
            task_id='mattermost_operator',
            conn_id='mattermost',
            channel='general',
            message='hello',
            username='Airflow',
            icon_url='https://cdn.something.com/icon.png',
            icon_emoji='grin',
            type_='custom_type',
            props={
                'card': 'text',
            },
            priority='standard',
            requested_ack=False,
            persistent_notifications=False,
        )

        operator.execute(MagicMock())

        operator.hook.return_value.run.assert_called_once_with(
            channel='general',
            message='hello',
            username='Airflow',
            icon_url='https://cdn.something.com/icon.png',
            icon_emoji='grin',
            type_='custom_type',
            props={
                'card': 'text',
            },
            priority='standard',
            requested_ack=False,
            persistent_notifications=False,
        )
