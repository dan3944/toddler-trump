import html
import logging
import os
import sys
import urllib.parse

import nltk
import tweepy

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')

auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_KEY_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)


class UserListener(tweepy.StreamListener):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def on_status(self, status):
        if status.user.screen_name != self.user:
            return

        text = status.extended_tweet['full_text'] if status.truncated else status.text
        text = html.unescape(text).strip()
        logging.info('Trump tweeted: %s', text)
    
        if text.startswith('RT @') or is_url(text) or status.in_reply_to_status_id:
            logging.info('Skipping')
        else:
            if text.startswith('.@'):
                text = text[1:]

            toddler = toddlerify(text)

            if status.is_quote_status:
                suffix = '\n' + status.quoted_status_permalink['url']
                toddler = toddler[: 280 - len(suffix)] + suffix

            logging.info('Tweet: %s', toddler)
            api.update_status(toddler)

    def on_error(self, status_code):
        logging.error('Response status code: %s', status_code)
        return True


def is_url(string):
    try:
        parsed = urllib.parse.urlparse(string)
        return parsed.scheme and parsed.netloc
    except ValueError:
        return False


def toddlerify(string):
    words = [word for word in string.split()
             if len(word) >= 2 and word[0] not in ('@', '#')]

    if not words:
        return ('Mommy, ' + string)[:280]

    if words[0].isupper():
        toddler = 'MOMMY, ' + string
    elif should_lowercase(string):
        toddler = 'Mommy, ' + string[0].lower() + string[1:]
    else:
        toddler = 'Mommy, ' + string

    if words[-1].isupper() and len(toddler) <= 271:
        toddler += ' WAAAHHH!'

    return toddler[:280]


def should_lowercase(string):
    starts_with_proper_noun = nltk.pos_tag(string.split())[0][1] in ('NNP', 'NNPS')
    starts_with_i = string[:2] in ('I ', "I'")
    return not (starts_with_proper_noun or starts_with_i)


if __name__ == '__main__':
    handle = sys.argv[1] if len(sys.argv) >= 2 else 'realDonaldTrump'
    logging.info('Handle: %s', handle)
    user_id = api.lookup_users(screen_names=[handle])[0].id_str
    stream = tweepy.Stream(auth=api.auth, listener=UserListener(handle))

    while True:
        logging.info('Starting stream for user_id %s', user_id)

        try:
            stream.filter(follow=[user_id])
        except:
            logging.exception('Stream interrupted')
