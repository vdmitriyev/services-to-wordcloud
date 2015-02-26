# coding: utf-8

__author__ = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.3.0"
__maintainer__ = "-"
__email__ = ""
__status__ = "dev"
__date__ = "08.02.2015"
__description__ = "Tiny python utility that converts tweets into cloud of words."

import re
from helper_wordcloud import ServiceToWordCloud

""" Class to convert twitter data (tweets) into Word Cloud"""
class TwitterServiceToWC(ServiceToWordCloud):

  def __init__(self, *args, **kwargs):
    """
      (obj, *args, **kwargs) -> None

      Initializing the parent class as well as intializing data wrangler
    """

    super(TwitterServiceToWC, self).__init__(*args, **kwargs)

    # configuring stopwords
    twitter_stopwords = {'innojam', 'video', 'cebit2014', 'c'}
    self.config_stopwords(twitter_stopwords)

    # wrangling twitter data
    self.wrangle_data()

  def wrangle_data(self):
    """
      (obj) -> None

      Wranling with data before porcessing it
    """
    # join tweets to a single string
    words = ' '.join(self.df['tweet'])

    # remove URLs, RTs, and twitter handles
    no_urls_no_tags = " ".join([word for word in words.split() 
                              if 'http' not in word
                                and not word.startswith('@')
                                and word != 'RT'
                              ])
    self.words = no_urls_no_tags

    print '[i] data formatted'

""" Class to convert your twitter user locations into Word Cloud"""
class TwitterLocationsServiceToWC(ServiceToWordCloud):

  def __init__(self, *args, **kwargs):
    """
      (obj, *args, **kwargs) -> None

      Initializing the parent class as well as intializing data wrangler
    """

    super(TwitterLocationsServiceToWC, self).__init__(*args, **kwargs)

    # configuring stopwords
    #twitter_stopwords = {'innojam', 'video', 'cebit2014'}
    #self.config_stopwords(twitter_stopwords)

    # wrangling twitter data
    self.wrangle_data()

  def wrangle_data(self):
    """
      (obj) -> None

      Wranling with data before porcessing it
    """

    def to_latin(plain):
      """
        (str) -> str

        Internal method that counvers non-latin names to the latin ones.
        Method requires the name specification inside arrays (non latin and latin arrays):
          - non_latin_list
          - latin_list
      """

      non_latin_list = ['Россия', 'Казахстан', 'Алматы']
      latin_list = ['Russia', 'Kazakhstan', 'Almaty']

      for index, value in enumerate(non_latin_list):
        if plain.lower() == value.lower():
          return latin_list[index]
      return plain

    # join locations to a single string
    words = ''
    for value in self.df['location']:
      words += ' ' + to_latin(str(value))

    # removing special symbols 
    reg_exp = '[",]'
    words = re.sub(reg_exp, " ", words)

    # remove nans, @ and URLs
    cleaned_data = " ".join([word for word in words.split() 
                              if 'http' not in word
                                and not word.startswith('@')
                                and word != 'nan'
                              ])

    self.words = cleaned_data

    print '[i] data formatted'

def process_tweets():
  # setting params for word cloud
  data_file = 'twitter-data.csv'
  data_folder = '../services/twitter/data/'
  save_directory = 'generated-twitter-twee'
  service_name = 'twitter-wordcloud-twee'
  fonts = None
  masks = ['square-mask']

  service = TwitterServiceToWC(data_file, data_folder, save_directory)
  #owc.process(service_name)
  service.process(service_name, fonts, masks)

def process_users_locations():

  # setting params for word cloud
  data_file = 'twitter-user-location-data.csv'
  data_folder = '../services/twitter/data/'
  save_directory = 'generated-twitter-loc'
  service_name = 'twitter-wordcloud-loc'
  fonts = ['eater-regular', 'sirinstencil-regular', 'ribeye-regular']
  masks = ['twitter-mask']

  service = TwitterLocationsServiceToWC(data_file, data_folder, save_directory)
  #owc.process(service_name)
  service.process(service_name, fonts, masks)

def main():
  """
    (None) -> None

    Main method that initiates instance of the class and starts processing.
  """
  process_tweets()
  #process_users_locations()

if __name__ == '__main__':
  main()