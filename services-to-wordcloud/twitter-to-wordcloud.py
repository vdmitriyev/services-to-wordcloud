# coding: utf-8

__author__ = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.2.0"
__maintainer__ = "-"
__email__ = ""
__status__ = "dev"
__date__ = "08.02.2015"
__description__ = "Tiny python utility that converts tweets into cloud of words."

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
    twitter_stopwords = {'innojam', 'video', 'cebit2014'}
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

def main():
  """
    (None) -> None

    Main method that initiates instance of the class and starts processing.
  """

  # setting params for word cloud
  data_file = 'twitter-data.csv'
  data_folder = '../services/twitter/data/'
  save_directory = 'generated-twitter'
  service_name = 'twitter-wordcloud'
  fonts = ['monaco']
  masks = ['twitter_mask']

  service = TwitterServiceToWC(data_file, data_folder, save_directory)
  #owc.process(service_name)
  service.process(service_name, fonts, masks)

if __name__ == '__main__':
  main()