from unittest.mock import patch, Mock, MagicMock
import requests
import pytest

from twitter import Twitter


class ResponseGetMock(object):
    def json(self):
        return {'avatar_url': 'test'}


@pytest.fixture(params=[None, 'python'])
def username(request):
    return request.param


@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, username, request, monkeypatch):
    if request.param == 'list':
        twitter = Twitter(username=username)
    elif request.param == 'backend':
        twitter = Twitter(backend=backend, username=username)

    return twitter


def test_twitter_initialization(twitter):
    assert twitter

# w dekoratorze patch nie można użyć obikktu twitter z fixture
@patch.object(Twitter, 'get_user_avatar', return_value='test')
def test_twitter_single_message(avatar_mock, twitter):
    # with patch('twitter.Twitter.get_user_avatar', return_value='test'):
    # with patch.object(twitter, 'get_user_avatar', return_value='test'):
    twitter.tweet("Test message")
    assert twitter.tweet_messages == ["Test message"]


def test_twitter_long_message(twitter):
    with pytest.raises(Exception):
        twitter.tweet("test" * 41)
    assert twitter.tweet_messages == []


def test_initialize_two_twitter_classes(backend):
    twitter1 = Twitter(backend=backend)
    twitter2 = Twitter(backend=backend)

    twitter1.tweet('Test 1')
    twitter1.tweet('Test 2')

    assert twitter2.tweet_messages == ['Test 1', 'Test 2']


@pytest.mark.parametrize("expected, message", (
        (["first"], "Test #first message"),
        (["first"], "#first message"),
        (["first"], "#FIRST message"),
        (["first"], "test message #first"),
        (["first", "second"], "test message #first #second")
))
def test_tweet_with_hashtags(expected, message, twitter):
    assert twitter.find_hashtags(message) == expected


# należy dodać argument avatar_mock do funkcji testowej, innaczej patch z dekoratora się nie wykona
@patch.object(Twitter, 'get_user_avatar', return_value='test')
def test_tweet_with_username(avatar_mock, twitter):
    if not twitter.username:
        pytest.skip()

    twitter.tweet('Test message')
    assert twitter.tweets == [{'message': 'Test message', 'avatar': 'test', 'hashtags': []}]
    avatar_mock.assert_called()


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_username2(avatar_mock, twitter):
    if not twitter.username:
        pytest.skip()

    twitter.tweet('Test message')
    assert twitter.tweets == [{'message': 'Test message', 'avatar': 'test', 'hashtags': []}]
    avatar_mock.assert_called()


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_hashtag_mock(avatar_mock, twitter):
    twitter.find_hashtags = Mock()
    twitter.find_hashtags.return_value = ['first']
    twitter.tweet('Test #second')
    assert twitter.tweets[0]['hashtags'] == ['first']
    twitter.find_hashtags.assert_called()
    twitter.find_hashtags.assert_called_with('Test #second')


def test_twitter_version(twitter):
    twitter.version = MagicMock()
    twitter.version.__eq__.return_value = '2.0'
    assert twitter.version == '2.0'

@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_twitter_get_all_hashtags(avatar_mock, twitter):
    twitter.tweet('Test #first')
    twitter.tweet('Test #second')
    twitter.tweet('Test #third')
    assert twitter.get_all_hashtags() == {'first', 'second', 'third'}


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_twitter_get_all_hashtags_notfound(avatar_mock, twitter):
    twitter.tweet('Test third')
    assert twitter.get_all_hashtags() == "No hashtags found"










