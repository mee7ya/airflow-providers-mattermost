from unittest.mock import MagicMock, patch

from airflow_providers_mattermost.notifiers import MattermostNotifier


class TestMattermostNotifier:
    notifier = MattermostNotifier

    @patch.object(notifier, 'hook')
    def test_execute(self, patched_hook: MagicMock) -> None:
        notifier = self.notifier(
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

        notifier.notify(MagicMock())

        notifier.hook.return_value.run.assert_called_once_with(
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
