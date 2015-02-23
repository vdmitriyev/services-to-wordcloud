# coding: utf-8

__author__ = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "-"
__email__ = ""
__status__ = "dev"
__date__ = "22.02.2015"
__description__ = "Tiny python utility that downloads blogs from Tumblr."

import pytumblr
from datetime import datetime
import os
import pandas as pd
import oauth_info as auth # our local file with the OAuth infos

class TimelineMiner(object):

    def __init__(self, access_token, access_secret, consumer_key, consumer_secret, user_name):
        self.access_token = access_token
        self.access_secret = access_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.user_name = user_name
        self.auth = None
        self.df = pd.DataFrame(columns=['timestamp', 'tumblrBlog'], dtype='str')


    def authenticate(self):
        """
            (class) -> boolean

            Passing throught authentication and verifying if the right credentials were given.
        """
        
        self.client = pytumblr.TumblrRestClient(
                        self.consumer_key,
                        self.consumer_secret,
                        self.access_token,
                        self.access_secret)
        info = self.client.info()
        try:
            if 'meta' in info:
                if info['meta']['status'] == 401:
                    return False
            else:
                return True
        except Exception, ex:
            print '[e] exception {}'.format(str(ex))
        return False

    def get_blogs(self):
        """
            (class) -> None

            Getting blog posts from the Tumblr and saving them.
        """
        counter = 0
        posts = self.client.posts(self.user_name, type='text') # get posts for a blog
        for entry in posts['posts']:
            blog_text = self.__get_replaced(entry)
            blog_date = self.__get_date(entry)
            self.df.loc[counter,'tumblrBlog'] = blog_text
            self.df.loc[counter,'timestamp'] = blog_date
            counter += 1
        
    def make_csv(self, path):
        """
            (obj, str) -> None

            Checks if the directory 'data' exists, creates it otherwise.
            Saves the data from tumblr text blog in csv using pandas.
        """

        if not os.path.exists('data'):
            os.makedirs('data')

        self.df.to_csv(path, encoding='utf8')
        print '[i] blogs saved into {}'.format(path)

    def __get_date(self, post):
        timest = datetime.strptime(post['date'],"%Y-%m-%d %H:%M:%S GMT")
        date = timest.strftime("%Y-%d-%m %H:%M:%S")
        return date

    def __get_replaced(self, post):
        _post = post['body']
        _post = _post.replace('"', '\'')
        _post = _post.replace('\n', ' ')
        return _post
    
if __name__ == "__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser(
            description='Tiny command line python utility that downloads blogs from Tumblr.',
            formatter_class=argparse.RawTextHelpFormatter,
    epilog='\nExample:\n'\
                './tumblr_blog.py -o my_timeline.csv -k Python,Github')

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
    tm.get_blogs()
    tm.make_csv(args.out)
    
