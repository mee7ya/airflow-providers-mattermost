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
        )

        # We get warning from Safeguard about executing operators outside TaskInstance
        # would be nice to suppress it for tests
        operator.execute(MagicMock())

        operator.hook.return_value.run.assert_called_once_with(
            channel='general',
            message='hello',
            username='Airflow',
        )
