import pytest

from twitter import Twitter

# nieporządana uruchamia się czy jest potrzebna czy nie przed kazdym testem
# @pytest.fixture(autouse=True)
# def prepare_backend_file():
#     with open('test.txt', "w"):
#         pass

@pytest.fixture
def backend(tmpdir):
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file


# można wywołąć fixture dwa razy na jednej klasie
# parametr name pozwala nadać inną nazwę funckji fixture niż zwracany parametr
@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, request):
    if request.param == 'list':
        twitter = Twitter()
    elif request.param == 'backend':
        twitter = Twitter(backend=backend)
    return twitter


def test_twitter_initialization(twitter):
    assert twitter


def test_twitter_single_message(twitter):
    twitter.tweet("Test message")
    assert twitter.tweet_messages == ["Test message"]


def test_twitter_long_message(twitter):
    with pytest.raises(Exception):
        twitter.tweet("test"*41)
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


