import pytest
from mastodon_client import MastodonClient


@pytest.fixture
def mastodon():
    return MastodonClient(api_token="test_token", api_url="https://mastodon.social")


def test_post_to_mastodon(mastodon, monkeypatch):
    def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200

        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    assert mastodon.post_to_mastodon("Test message") == True
