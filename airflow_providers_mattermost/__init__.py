from ._version import __version__


def get_provider_info() -> dict:
    return {
        'package-name': 'airflow-providers-mattermost',
        'name': 'Mattermost',
        'description': 'Mattermost',
        'connection-types': [
            {
                'connection-type': 'mattermost',
                'hook-class-name': 'airflow_providers_mattermost.hooks.MattermostHook',
            }
        ],
        'versions': [__version__],
    }
