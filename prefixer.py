import os
import sys
import tweepy

API_KEY = os.environ['API_KEY']
API_KEY_SECRET = os.environ['API_KEY_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class UserListener(tweepy.StreamListener):
    def __init__(self, user):
        super(UserListener, self).__init__()
        self.user = user

    def on_status(self, status):
        if status.user.screen_name != self.user:
            return

        status = status.text
        print('\n', status)
    
        if status.startswith('RT @'):
            print('Retweet - skipping')
            return # skip retweets

        if status.isupper():
            toddler = 'MOMMY, ' + status

            if len(toddler) <= 271:
                toddler += ' WAAAHHH!'

        else:
            toddler = 'Mommy, ' + status[0].lower() + status[1:]

        if len(toddler) <= 280:
            print('Tweeting:', toddler)
            api.update_status(toddler)
        else:
            print("Couldn't tweet - length", len(toddler))
            print(toddler)
    
    def on_error(self, status_code):
        print('\n***ERROR: Status Code', status_code)
        return True


if __name__ == '__main__':
    handle = sys.argv[1] if len(sys.argv) >= 2 else 'realDonaldTrump'
    print('Handle:', handle)
    user_id = api.lookup_users(screen_names=[handle])[0].id_str

    tweepy \
        .Stream(auth=api.auth, listener=UserListener(handle)) \
        .filter(follow=[user_id])
