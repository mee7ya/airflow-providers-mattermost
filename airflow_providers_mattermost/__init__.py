__version__ = '0.1.0'


def get_provider_info() -> dict:
    return {
        'package-name': 'airflow-providers-mattermost',
        'name': 'Mattermost',
        'description': 'Mattermost Apache Airflow providers',
        'connection-types': [
            {
                'connection-type': 'mattermost',
                'hook-class-name': 'airflow_providers_mattermost.hooks.MattermostHook',
            }
        ],
        'versions': [__version__],
    }
