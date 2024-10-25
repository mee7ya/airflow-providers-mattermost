from contextlib import nullcontext
from functools import partial
from typing import TYPE_CHECKING
from unittest.mock import patch

from pytest import mark, raises
from requests import HTTPError, Response, Session

from airflow_providers_mattermost.hooks import MattermostHook
from airflow_providers_mattermost.hooks.mattermost import log as mattermost_log

if TYPE_CHECKING:
    from unittest.mock import MagicMock

    from _pytest.logging import LogCaptureFixture


class TestMattermostHook:
    hook = MattermostHook
    log = mattermost_log

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
        'status_code, data, icon_url, type_',
        (
            (200, b'{}', 'https://cdn.something.com/icon.png', None),
            (200, b'{}', None, 'type'),
            (200, b'{}', None, None),
            (502, b'{}', None, None),
        ),
    )
    def test_run(
        self,
        patched_send: 'MagicMock',
        status_code: int,
        data: bytes,
        icon_url: str | None,
        type_: str | None,
        caplog: 'LogCaptureFixture',
    ) -> None:
        patched_send.return_value.status_code = status_code
        patched_send.return_value._content = data

        call = partial(
            self.hook('mattermost').run,
            channel='general',
            message='hello',
            username='Airflow',
            icon_url=icon_url,
            icon_emoji='grin',
            type_=type_,
            props={
                'card': 'text',
            },
        )
        with (
            raises(ValueError, match="'type_' must start with 'custom_'")
            if type_ is not None and not type_.startswith('custom_')
            else nullcontext()
        ):
            match status_code:
                case 200:
                    call()
                case _:
                    with raises(HTTPError):
                        call()

        if icon_url:
            assert "'icon_emoji' will override 'icon_url'" in caplog.messages
