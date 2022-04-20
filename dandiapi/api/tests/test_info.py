from django.conf import settings
import versioneer

from dandiapi.api.views.info import schema_url


def test_rest_info(api_client):
    resp = api_client.get('/api/info/')
    assert resp.status_code == 200
    assert resp.json() == {
        'schema_version': settings.DANDI_SCHEMA_VERSION,
        'schema_url': schema_url,
        'version': versioneer.get_version(),
        'cli-minimal-version': '0.14.2',
        'cli-bad-versions': [],
        'services': {
            'api': {'url': settings.DANDI_API_URL},
            'webui': {'url': settings.DANDI_WEB_APP_URL},
            'jupyterhub': {'url': settings.DANDI_JUPYTERHUB_URL},
        },
    }
