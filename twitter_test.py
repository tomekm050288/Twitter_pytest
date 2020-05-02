import pytest

from twitter import Twitter


#można wywołąć fixture dwa razy nan
@pytest.fixture(params=[None, "test.txt"])
def twitter(request):
    twitter = Twitter(backend=request.param)
    yield twitter
    twitter.delete()


def test_twitter_initialization(twitter):
    assert twitter


def test_twitter_single_message(twitter):
    twitter.tweet("Test message")
    assert twitter.tweets == ["Test message"]


def test_twitter_long_message(twitter):
    with pytest.raises(Exception):
        twitter.tweet("test"*41)
    assert twitter.tweets == []


@pytest.mark.parametrize("expected, message", (
        (["first"], "Test #first message"),
        (["first"], "#first message"),
        (["first"], "#FIRST message"),
        (["first"], "test message #first"),
        (["first", "second"], "test message #first #second")
        ))
def test_tweet_with_hashtags(expected, message, twitter):
    assert twitter.find_hashtags(message) == expected


