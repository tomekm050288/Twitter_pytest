import os
import re


class Twitter:

    version = '1.0'

    def __init__(self, backend=None):
        self._tweets = []
        self.backend = backend
        if self.backend and not os.path.exists(self.backend):
            with open(self.backend, "w"):
                pass


    @property
    def tweets(self):
        if self.backend and not self._tweets:
            with open(self.backend) as twitter_file:
                self._tweets = [line.rstrip("\n") for line in twitter_file]
        return self._tweets

    def tweet(self, message):
        if len(message) > 160:
            raise Exception("Message to long.")
        self.tweets.append(message)
        if self.backend:
            with open(self.backend, 'w') as twitter_file:
                twitter_file.write("\n".join(self.tweets))

    def delete(self):
        if self.backend:
            os.remove(self.backend)

    def find_hashtags(self, message):
        return [m.lower() for m in re.findall("#(\w+) ?", message)]



twitter = Twitter()

print(twitter.version)


