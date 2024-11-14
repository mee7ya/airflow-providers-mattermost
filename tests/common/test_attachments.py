from dataclasses import asdict

from airflow_providers_mattermost.common.attachments import Attachment, Field


class TestAttachments:
    def test_to_dict(self) -> None:
        attachment = Attachment(
            fallback='fallback',
            color='#000000',
            pretext='pretext',
            text='text',
            author_name='Author',
            author_icon='https://example.com/icon.png',
            author_link='https://example.com/',
            title='title',
            title_link='https://example.com/title/',
            fields=[
                Field(
                    short=True,
                    title='field_title_1',
                    value='field_value_1',
                ),
                Field(
                    short=False,
                    title='field_title_2',
                    value='field_value_2',
                ),
            ],
            image_url='https://example.com/image.png',
        )

        assert asdict(attachment) == {
            'fallback': 'fallback',
            'color': '#000000',
            'pretext': 'pretext',
            'text': 'text',
            'author_name': 'Author',
            'author_icon': 'https://example.com/icon.png',
            'author_link': 'https://example.com/',
            'title': 'title',
            'title_link': 'https://example.com/title/',
            'fields': [
                {
                    'short': True,
                    'title': 'field_title_1',
                    'value': 'field_value_1',
                },
                {
                    'short': False,
                    'title': 'field_title_2',
                    'value': 'field_value_2',
                },
            ],
            'image_url': 'https://example.com/image.png',
        }
