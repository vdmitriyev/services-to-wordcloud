# coding: utf-8

__author__ = 'Viktor Dmitriyev'
__copyright__ = 'Copyright 2015, Viktor Dmitriyev'
__credits__ = ['Viktor Dmitriyev']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = '-'
__email__ = ''
__status__ = 'dev'
__date__ = '28.02.2015'
__description__ = 'Tiny python utility that converts comments fomr habrahabr.ru to the cloud of words.'

import re
import sys
from helper_wordcloud import ServiceToWordCloud
from helper_directory import DirectoryHelper

# configd for teh CSV
#CSV_FIELD_NAME = 'habrComments'

# configuring stop words
stop_words_folder = 'stopwords'
stop_words_files = ['stop-words_russian_1_ru.txt', 'stop-words_russian_2_ru.txt']


class HabrServiceToWC(ServiceToWordCloud):

    """Class to convert twitter data (tweets) into Word Cloud."""

    def __init__(self, csv_field_name, *args, **kwargs):
        """
          (obj, *args, **kwargs) -> None

          Initializing the parent class as well as intializing data wrangler
        """

        super(HabrServiceToWC, self).__init__(*args, **kwargs)
        # configuring stopwords

        self.config_stopwords()

        # wrangling twitter data
        self.wrangle_data(csv_field_name)

    def config_stopwords(self):
        """
          (obj) -> None

        """

        # processing custom stop words from specified files
        custom_stopwords = list()
        dh = DirectoryHelper()
        for sw_file in stop_words_files:
            sw_fullpath = stop_words_folder + '\\' + sw_file
            sw_file = dh.read_file_utf8(sw_fullpath)
            for sw_single in sw_file.split('\n'):
                custom_stopwords.append(sw_single[:-1])

        # adding fetched stopwords
        super(HabrServiceToWC, self).config_stopwords(custom_stopwords)

    def wrangle_data(self, csv_field_name):
        """
          (obj) -> None

          Wranling with data before porcessing
        """

        assert csv_field_name is not None, \
            'csv_field_name should not be None\ncheck variable'

        # join all data from the tumblr entries to a single string
        words = ' '.join(self.df[csv_field_name])

        # simple html and other special symbols removal
        reg_exp = '(<.*?>)|(&.*?;)'
        no_html_words = re.sub(reg_exp, ' ', words)

        # remove rowds with URLs, # and &
        no_urls_words = ' '.join([word for word in no_html_words.split()
                                  if 'http' not in word
                                  # and not word.startswith('@')
                                  ])

        self.words = no_urls_words
        print '[i] data formatted'

def process_comments():

    # setting params for word cloud
    data_file = 'habr-user-comments.csv'
    data_folder = '../services/habr/data/'
    save_directory = 'generated-habr-comments'
    service_name = 'habr-wordcloud'
    fonts = ['clearsans-regular']
    masks = ['habr-logo-h-inverted-mask', 'habr-logo-inverted-mask']
    masks = ['square-mask']

    csv_field_name = 'habrComments'

    service = HabrServiceToWC(data_file=data_file, 
                                data_folder=data_folder, 
                                save_directory=save_directory, 
                                csv_field_name=csv_field_name)
    
    service.process(service_name, fonts, masks)

def process_articles():
    
    # setting params for word cloud
    data_file = 'habr-articles.csv'
    data_folder = '../services/habr/data/'
    save_directory = 'generated-habr-articles'
    service_name = 'habr-wordcloud'
    fonts = ['clearsans-regular']
    masks = ['jet-mask']

    csv_field_name = 'habrArticles'

    service = HabrServiceToWC(data_file=data_file, 
                                data_folder=data_folder, 
                                save_directory=save_directory, 
                                csv_field_name=csv_field_name)

    service.process(service_name, fonts, masks)

def main():
    """
      (None) -> None

      Main method that initiates instance of the class and starts processing.
    """
    process_comments()
    process_articles()

    
if __name__ == '__main__':
    # setting system default encoding to the UTF-8
    reload(sys)
    sys.setdefaultencoding('UTF8')

    main()
