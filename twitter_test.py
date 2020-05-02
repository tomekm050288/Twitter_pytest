import unittest
from twitter import Twitter


class TwitterTest(unittest.TestCase):

    def setUp(self):
        self.twitter = Twitter()

    def test_initialization(self):
        self.assertTrue(self.twitter)

    def test_tweet_single(self):
        #when
        self.twitter.tweet("Test message")
        #then
        self.assertEqual(self.twitter.tweets, ["Test message"])


if __name__ == '__main__':
    unittest.main()