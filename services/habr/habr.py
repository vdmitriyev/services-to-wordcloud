# coding: utf-8
#!/usr/bin/env python

__author__     = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "-"
__email__     = ""
__status__     = "dev"
__date__    = "28.02.2015"
__description__ = "Web crawler that uses beautifulsoup package to crawl comments from habrahabr.ru portal of specified user."

import os
import sys
import urllib2
import codecs
from time import sleep
from bs4 import BeautifulSoup

# crawler configs
SLEEP_TIME_IN_SECONDS = 2

# CSV configs
CSV_FIELD_NAME = u'habrEntries'
CSV_DELIM = u','

class BSCrawler():

    UA = 'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.2.9) Gecko/20100913 Firefox/3.6.9'

    def __init__(self):
        print '[i] crawling of habrahabr commnets was initialted'

    def crawl_dynamic(self):
        """
            (obj) -> None

            Method that extracts urls from 'dispatcher' in a dynamic way.
            It means that the initial URL pattern should contain {} to be replaced further.
        """
        for url in self.dispatcher_dynamic:
            print '[i] following url is going to be parsed in a dynamic way:\n {}'.format(url)
            self.dynamic_url = url
            user_name = self.dispatcher_dynamic[url][1]
            file_name = self.dispatcher_dynamic[url][2]
            try:
                self.dispatcher_dynamic[url][0](self, user_name, file_name)
            except Exception, ex:
                print '[e] exception {}'.format(str(ex))
                print '[i] error while crawling web page'

    def download_document(self, url):
        """
            (obj,str) -> (str)

            Downloading html page and storing inside string.
        """

        html = None
        try:
            req = urllib2.Request(url=url, headers={'User-Agent': self.UA})
            hdl = urllib2.urlopen(req)
            html = hdl.read()
        except Exception,ex:
            print '[e] exception: {}'.format(str(ex))

        return html

    def process_comments(self, user_name, file_name):
        """
            (obj) -> None
            Processing comments from habrahabr.
        """

        def internal_parser(html):
            """
                (str) -> dict
                Internal parser that parses given html accoding to it's structure.
            """
            soup = BeautifulSoup(html)
            fetched = list()
            comments = soup.findAll('div', attrs={'class':'message html_format '})
            for entry in comments:
                fetched.append(entry.get_text(strip=True))
            return fetched

        result_csv = list()
        cnt_page, cnt_comments = 0, 0

        while True:
            cnt_page += 1
            str_page = 'page{}'.format(cnt_page)
            url_to_download = self.dynamic_url.format(user_name, str_page)

            # priting info about url to be processed
            print '[i] url to download {}'.format(url_to_download)

            fetched_comments = internal_parser(self.download_document(url_to_download))

            if len(fetched_comments) > 0:
                for comment in fetched_comments:
                    cnt_comments += 1
                    result_csv.append([cnt_comments, comment])
            else:
                break

            # setting the main script to sleep for some seconds
            sleep(SLEEP_TIME_IN_SECONDS)

        data = {}
        data['entries'] = result_csv

        print '[i] all comments were extracted'

        self.save_csv(data, file_name)

    def process_article(self, user_name, file_name):
        """
            (obj) -> None
            Processing articles from habrahabr.
        """

        def internal_parser(html):
            """
                (str) -> dict
                Internal parser that parses given html accoding to it's structure.
            """
            soup = BeautifulSoup(html)
            fetched = list()
            entries = soup.findAll('div', attrs={'class':'content html_format'})
            for entry in entries:
                fetched.append(entry.get_text(strip=True))
            return fetched

        result_csv = list()
        url_to_download = self.dynamic_url

        print '[i] url to download {}'.format(url_to_download)

        fetched = internal_parser(self.download_document(url_to_download))
        for i, row in enumerate(fetched):
            result_csv.append([i, row])

        data = {}
        data['entries'] = result_csv

        print '[i] article was extracted'
        self.save_csv(data, file_name)

    def save_csv(self, data, file_name):
        """
            (obj, str) -> None

            Checks if the directory 'data' exists, creates it otherwise.
            Saves the data to the csv using pandas.
        """

        if not os.path.exists('data'):
            os.makedirs('data')

        def normalize_data(input_data):
            """
                (str) -> (str)
                Interenal method that normalizes data
            """
            return input_data.replace(CSV_DELIM, '')

        # forming header
        _csvdata = u'Number' + CSV_DELIM + CSV_FIELD_NAME + u'\n'
        for row in data['entries']:
            _csvdata += str(row[0]) + CSV_DELIM + normalize_data(row[1]) + u'\n'

        # saving to csv
        full_path = 'data' + '\\' + file_name
        _file = codecs.open(full_path, 'w', 'utf8')
        _file.write(_csvdata)
        _file.close()

        print '[i] entries from habr were saved into "{}"'.format(full_path)

    # dispatchers for extract and parsing multiple web pages
    dispatcher_dynamic = {
            #'http://habrahabr.ru/users/{}/comments/{}': [process_comments, "darx", "habr-user-comments.csv"],
            #'http://habrahabr.ru/users/{}/comments/{}': [process_comments, "freetonik", "habr-user-comments.csv"],
            'http://habrahabr.ru/users/{}/comments/{}': [process_comments, "vdmitriyev", "habr-user-comments.csv"],
            'http://habrahabr.ru/company/makeitlab/blog/251865/': [process_article, "makeitlab", "habr-articles.csv"]
        }

def main():

    crawler = BSCrawler()
    crawler.crawl_dynamic()

if __name__ == '__main__':

    # setting system default encoding to the UTF-8
    reload(sys)
    sys.setdefaultencoding('UTF8')

    # initiating main processing
    main()
