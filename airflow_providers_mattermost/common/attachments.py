from dataclasses import dataclass


@dataclass
class Field:
    """
    For use inside :class:`.Attachment` as ``fields`` param
    """

    short: bool | None = None
    title: str | None = None
    value: str | None = None


@dataclass
class Attachment:
    """
    Instances of this dataclass can be passed as ``attachments`` param in :class:`.MattermostOperator`, :class:`.MattermostNotifier`

    For params description refer to `Mattermost attachments`_

    .. _Mattermost attachments:
       https://developers.mattermost.com/integrate/reference/message-attachments/
    """

    fallback: str | None = None
    color: str | None = None
    pretext: str | None = None
    text: str | None = None
    author_name: str | None = None
    author_icon: str | None = None
    author_link: str | None = None
    title: str | None = None
    title_link: str | None = None
    fields: list[Field] | None = None
    image_url: str | None = None
