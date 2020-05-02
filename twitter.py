import re


class Twitter:

    version = '1.0'

    def __init__(self):
        self.tweets = []

    def tweet(self, message):
        if len(message) > 160:
            raise Exception("Message to long.")
        self.tweets.append(message)

    def delete(self):
        print("It's the end")

    def find_hashtags(self, message):
        return [m.lower() for m in re.findall("#(\w+) ?", message)]



twitter = Twitter()

print(twitter.version)


