from contextlib import nullcontext
from typing import TYPE_CHECKING, get_args
from unittest.mock import patch

from pytest import mark, raises
from requests import HTTPError, Response, Session

from airflow_providers_mattermost.common.attachments import Attachment
from airflow_providers_mattermost.common.types import Priority
from airflow_providers_mattermost.hooks import MattermostHook
from airflow_providers_mattermost.hooks.mattermost import log as mattermost_log

if TYPE_CHECKING:
    from unittest.mock import MagicMock

    from _pytest.logging import LogCaptureFixture


@patch.dict(
    'os.environ',
    AIRFLOW_CONN_MATTERMOST='mattermost://:SECRETVERYKEY@myhost.com:1234/https',
)
@patch.object(Session, 'send', return_value=Response())
class TestMattermostHook:
    hook = MattermostHook
    log = mattermost_log

    def test_get_conn_request(self, patched_send: 'MagicMock') -> None:
        request, _ = self.hook('mattermost').get_conn()

        assert request.method == 'POST'
        assert request.url == 'https://myhost.com:1234/hooks/SECRETVERYKEY'

    @mark.parametrize('status_code', (200, 502))
    def test_run_status_code_error(
        self, patched_send: 'MagicMock', status_code: int
    ) -> None:
        patched_send.return_value.status_code = status_code
        patched_send.return_value._content = b'{}'

        with raises(HTTPError) if status_code != 200 else nullcontext():
            self.hook('mattermost').run(
                channel='general',
                message='hello',
            )

    @mark.parametrize('type_', ('custom_type', 'type'))
    def test_run_type_error(self, patched_send: 'MagicMock', type_: str) -> None:
        patched_send.return_value.status_code = 200
        patched_send.return_value._content = b'{}'

        with (
            raises(ValueError, match="'type_' must start with 'custom_'")
            if not type_.startswith('custom_')
            else nullcontext()
        ):
            self.hook('mattermost').run(
                channel='general',
                message='hello',
                type_=type_,
            )

    @mark.parametrize('priority', ('standard', 'non-standard'))
    def test_run_priority_error(self, patched_send: 'MagicMock', priority: str) -> None:
        patched_send.return_value.status_code = 200
        patched_send.return_value._content = b'{}'

        with (
            raises(
                ValueError,
                match="'priority' must be one of 'standard', 'important', 'urgent'",
            )
            if priority not in get_args(Priority)
            else nullcontext()
        ):
            self.hook('mattermost').run(
                channel='general',
                message='hello',
                priority=priority,
            )

    @mark.parametrize(
        'icon_url, icon_emoji',
        (
            (
                ('https://cdn.something.com/icon.png', None),
                (None, 'grin'),
                ('https://cdn.something.com/icon.png', 'grin'),
            )
        ),
    )
    def test_run_icon_override_warning(
        self,
        patched_send: 'MagicMock',
        icon_url: str | None,
        icon_emoji: str | None,
        caplog: 'LogCaptureFixture',
    ) -> None:
        patched_send.return_value.status_code = 200
        patched_send.return_value._content = b'{}'

        self.hook('mattermost').run(
            channel='general',
            message='hello',
            icon_url=icon_url,
            icon_emoji=icon_emoji,
        )
        if icon_url is not None and icon_emoji is not None:
            assert "'icon_emoji' will override 'icon_url'" in caplog.messages
        else:
            assert "'icon_emoji' will override 'icon_url'" not in caplog.messages

    @mark.parametrize(
        'message, attachments',
        (
            (
                ('hello', None),
                (None, [Attachment(text='hello')]),
                ('hello', [Attachment(text='hello')]),
                (None, None),
            )
        ),
    )
    def test_run_message_or_attachments_error(
        self,
        patched_send: 'MagicMock',
        message: str | None,
        attachments: list[Attachment] | list[dict] | None,
    ) -> None:
        patched_send.return_value.status_code = 200
        patched_send.return_value._content = b'{}'

        with (
            raises(ValueError, match="Either 'message' or 'attachments' must be set")
            if message is None and not attachments
            else nullcontext()
        ):
            self.hook('mattermost').run(
                channel='general',
                message=message,
                attachments=attachments,
            )
