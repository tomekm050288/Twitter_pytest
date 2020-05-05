import pytest
import requests
from twitter import Twitter


# nieporządana uruchamia się czy jest potrzebna czy nie przed kazdym testem
# @pytest.fixture(autouse=True)
# def prepare_backend_file():
#     with open('test.txt', "w"):
#         pass


class ResponseGetMock(object):
    def json(self):
        return {'avatar_url': 'test'}


# fixture to wyłączania zapytań z request
@pytest.fixture(autouse=True)
def no_request(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.fixture
def backend(tmpdir):
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file


@pytest.fixture(params=[None, 'python'])
def username(request):
    return request.param


# można wywołąć fixture dwa razy na jednej klasie
# parametr name pozwala nadać inną nazwę funckji fixture niż zwracany parametr
@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, username, request, monkeypatch):
    if request.param == 'list':
        twitter = Twitter(username=username)
    elif request.param == 'backend':
        twitter = Twitter(backend=backend, username=username)

    # def monkey_return():
    #     return 'test'

    # monkeypatch.setattr(twitter, 'get_user_avatar', monkey_return)
    # return twitter

    def monkey_return(url):
        return ResponseGetMock()

    monkeypatch.setattr(requests, 'get', monkey_return)
    return twitter


def test_twitter_initialization(twitter):
    assert twitter


def test_twitter_single_message(twitter):
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


def test_tweet_with_username(twitter):
    if not twitter.username:
        pytest.skip()

    twitter.tweet('Test message')
    assert twitter.tweets == [{'message': 'Test message', 'avatar': 'test', 'hashtags': []}]
