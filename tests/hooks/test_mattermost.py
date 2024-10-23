from functools import partial
from unittest.mock import MagicMock, patch

from pytest import mark, raises
from requests import HTTPError, Response, Session

from airflow_providers_mattermost.hooks import MattermostHook


class TestMattermostHook:
    hook = MattermostHook

    @patch.dict(
        'os.environ',
        AIRFLOW_CONN_MATTERMOST='mattermost://:SECRETVERYKEY@myhost.com:1234/https',
    )
    def test_get_conn_request(self) -> None:
        request, _ = self.hook('mattermost').get_conn()

        assert request.method == 'POST'
        assert request.url == 'https://myhost.com:1234/hooks/SECRETVERYKEY'

    @patch.dict(
        'os.environ',
        AIRFLOW_CONN_MATTERMOST='mattermost://:SECRETVERYKEY@myhost.com:1234/https',
    )
    @patch.object(Session, 'send', return_value=Response())
    @mark.parametrize(
        'status_code, data',
        (
            (200, b'{}'),
            (502, b'{}'),
        ),
    )
    def test_run(self, patched_send: MagicMock, status_code: int, data: bytes) -> None:
        patched_send.return_value.status_code = status_code
        patched_send.return_value._content = data

        call = partial(
            self.hook('mattermost').run,
            channel='general',
            message='hello',
            username='Airflow',
        )
        match status_code:
            case 200:
                call()
            case _:
                with raises(HTTPError):
                    call()
