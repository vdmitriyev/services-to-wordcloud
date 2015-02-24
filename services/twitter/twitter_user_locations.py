#!/usr/bin/env python

__author__ = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "-"
__email__ = ""
__status__ = "dev"
__date__ = "24.02.2015"
__description__ = "Tiny python utility that downloads locations of your twitter followers."

import os
import pandas as pd
import twitter
from datetime import datetime
import oauth_info as auth # our local file with the OAuth infos

class TimelineMiner(object):

    def __init__(self, access_token, access_secret, consumer_key, consumer_secret, user_name):
        self.access_token = access_token
        self.access_secret = access_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.user_name = user_name
        self.auth = None
        self.df = pd.DataFrame(columns=['screen_name', 'id', 'location'], dtype='str')


    def authenticate(self):
        self.auth = twitter.Twitter(auth=twitter.OAuth(self.access_token, 
                    self.access_secret, self.consumer_key, 
                    self.consumer_secret))
        return bool(isinstance(self.auth, twitter.api.Twitter))
        

    def get_list_of_users(self):
        """
            (obj) -> None


        """

        counter = 0
        lookup_ids = list()
        
        def _fire_lookup(counter, look_up):
            follower_ids = self.auth.users.lookup(user_id=look_up)
            for follower in follower_ids:
                #self.df.loc[counter,'screen_name'] = follower['screen_name']
                #self.df.loc[counter,'id'] = follower['id']
                self.df.loc[counter,'location'] = follower['location']
                counter += 1

        follower_ids = self.auth.followers.ids(screen_name=self.user_name)
     
        for account_id in follower_ids['ids']:
            lookup_ids.append(account_id)
            if len(lookup_ids) == 100:
                _fire_lookup(counter, lookup_ids)
                lookup_ids = list()
                counter +=100

        if len(lookup_ids) > 0:
            _fire_lookup(counter, lookup_ids)
        
    def make_csv(self, path):
        """
            (obj, str) -> None

            Checks if the directory 'data' exists, creates it otherwise.
            Saves the data from twitter in csv using pandas.
        """
        if not os.path.exists('data'):
            os.makedirs('data')
        self.df.to_csv(path, encoding='utf8')
        print '[i] tweets saved into %s' % path

    def __get_date(self, timeline, tweet):
        timest = datetime.strptime(timeline[tweet]['created_at'],
                                      "%a %b %d %H:%M:%S +0000 %Y")
        date = timest.strftime("%Y-%d-%m %H:%M:%S")
        return date

if __name__ == "__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser(
            description='A command line tool to download your personal twitter user locations.',
            formatter_class=argparse.RawTextHelpFormatter,
    epilog='\nExample:\n'\
                './twitter_user_locations.py -o my_timeline.csv -k Python,Github')

    parser.add_argument('-o', '--out', help='Filename for creating the output CSV file.')    
    parser.add_argument('-v', '--version', action='version', version='v. 1.0.0')
    
    args = parser.parse_args()
    
    if not args.out:
        print('Please provide a filename for creating the output CSV file.')
        quit()
    
    tm = TimelineMiner(auth.ACCESS_TOKEN, 
                       auth.ACCESS_TOKEN_SECRET,  
                       auth.CONSUMER_KEY, 
                       auth.CONSUMER_SECRET,
                       auth.USER_NAME)
   
        
    print('Authentification successful: %s' %tm.authenticate())
    tm.get_list_of_users()
    tm.make_csv(args.out)
    
