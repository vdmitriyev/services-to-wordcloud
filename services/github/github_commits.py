# coding: utf-8

__author__ = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "-"
__email__ = ""
__status__ = "dev"
__date__ = "25.02.2015"
__description__ = "Tiny python utility that downloads text messages of your commits from particular Github repository."

# GitHub Wrapper
import github as github

#
from datetime import datetime
import os
import json
import pandas as pd
import oauth_info as auth # our local file with the OAuth infos


class TimelineMiner(object):

    def __init__(self, personal_access_token, access_token, access_secret, consumer_key, consumer_secret, user_name, repository_name):

        # access token method 1
        self.personal_access_token = personal_access_token

        # access token method 2
        self.access_token = access_token
        self.access_secret = access_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        # user and repo configs
        self.user_name = user_name
        self.repository_name = repository_name

        self.auth = None
        self.df = pd.DataFrame(columns=['timestamp', 'githubCommitMessage'], dtype='str')

    def authenticate(self):
        """
            (class) -> boolean

            Passing throught authentication and verifying if the right credentials were given.
        """

        if self.personal_access_token is not None:
            self.gh = github.GitHub(access_token = self.personal_access_token)
        else:
            self.gh = github.GitHub(
                        self.consumer_key,
                        self.consumer_secret,
                        self.access_token,
                        self.access_secret)
        try:
            
            some_get = self.gh.users(self.user_name).get()
            print json.dumps(some_get, sort_keys=True, indent=4, separators=(',', ': '))
            return True
        except Exception, ex:
            print '[e] exception {}'.format(str(ex))
            return False
        
        return False

    def get_commits(self):
        """
            (class) -> None

            Getting commits of the particular repository of the GitHub.
        """

        counter = 0
        page = 1

        # one exta requrest to understand math pages commits per page
        commits = self.gh.repos(self.user_name)(self.repository_name).commits.get(author = self.user_name, page = page)
        max_commits_per_page = len(commits)

        while True:
            commits = self.gh.repos(self.user_name)(self.repository_name).commits.get(author = self.user_name, page = page)
            for index in range(len(commits)):
                 commit_message = self.__get_replaced(commits[index]['commit'])
                 commit_date = self.__get_date(commits[index]['commit'])
                 self.df.loc[counter,'githubCommitMessage'] = commit_message
                 self.df.loc[counter,'timestamp'] = commit_date
                 counter += 1

            if max_commits_per_page == len(commits):
                page+=1
            else:
                break
        
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

    def __get_date(self, commit):
        timest = datetime.strptime(commit['author']['date'],"%Y-%m-%dT%H:%M:%SZ")
        date = timest.strftime("%Y-%d-%m %H:%M:%S")
        return date

    def __get_replaced(self, commit):
        _result = commit['message']
        _result = _result.replace('"', '\'')
        _result = _result.replace('\n', ' ')
        return _result
    
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
    
    tm = TimelineMiner(
                        auth.PERSONAL_ACCESS_TOKEN,
                        auth.ACCESS_TOKEN, 
                        auth.ACCESS_TOKEN_SECRET,  
                        auth.CONSUMER_KEY, 
                        auth.CONSUMER_SECRET,
                        auth.USER_NAME,
                        auth.REPOSITORY_NAME
                       )

    print('Authentification successful: %s' %tm.authenticate())
    tm.get_commits()
    tm.make_csv(args.out)
    
