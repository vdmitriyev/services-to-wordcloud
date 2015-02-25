# coding: utf-8

__author__ = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "-"
__email__ = ""
__status__ = "dev"
__date__ = "24.02.2015"
__description__ = "Tiny python utility that converts commits from github into cloud of words."

import re
from helper_wordcloud import ServiceToWordCloud

# configd for teh CSV
CSV_FIELD_NAME = 'githubCommitMessage'

""" Class to convert twitter data (tweets) into Word Cloud"""
class GithubrServiceToWC(ServiceToWordCloud):

  def __init__(self, *args, **kwargs):
    """
      (obj, *args, **kwargs) -> None

      Initializing the parent class as well as intializing data wrangler
    """

    super(GithubrServiceToWC, self).__init__(*args, **kwargs)

    # configuring stopwords
    # own_stopwords = {'pdf', 'programming', 'book', 'c', 'guide'}
    # self.config_stopwords(own_stopwords)

    # wrangling twitter data
    self.wrangle_data()

  def wrangle_data(self):
    """
      (obj) -> None

      Wranling with data before porcessing
    """

    # join all data from the tumblr entries to a single string
    words = ' '.join(self.df[CSV_FIELD_NAME])

    # simple html and other special symbols removal 
    reg_exp = "(<.*?>)|(&.*?;)"
    no_html_words = re.sub(reg_exp, " ", words)

    # remove rowds with URLs, # and & 
    no_urls_words = " ".join([word for word in no_html_words.split() 
                              if 'http' not in word
                                #and not word.startswith('@')
                              ])

    self.words = no_urls_words
    print '[i] data formatted'

def main():
  """
    (None) -> None

    Main method that initiates instance of the class and starts processing.
  """

  # setting params for word cloud
  data_file = 'github-commits-data.csv'
  data_folder = '../services/github/data/'
  save_directory = 'generated-github'
  service_name = 'github-wordcloud'
  fonts = None
  masks = ['github-logo-inverted', 'github-logo-original']

  service = GithubrServiceToWC(data_file, data_folder, save_directory)
  service.process(service_name, fonts, masks)

if __name__ == '__main__':
  main()

