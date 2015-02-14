# coding: utf-8

__author__ = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.1.0"
__maintainer__ = "-"
__email__ = ""
__status__ = "dev"
__date__ = "14.02.2015"
__description__ = "Tiny python utility that converts ORCID publication titles into cloud of words."

import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from helper_wordcloud import WordCloudHelper

class DataLoader():

  def load_webdata(self):
    """
      (class) -> None

      Loading data stored somewhere on the web
    """
    
    #import urllib
    #url with dataset
    #url = "http://www.ats.ucla.edu/stat/data/binary.csv"
    
    #df = pd.read_csv(url)
    #return df
    return None

  def load_localdata(self):
    """
      (class) -> DataFrame

      Loading data stored locally.
    """
    
    # set constants for the folder and file with data
    DATA_FOLDER = '../services/orcid/data/'
    DATA_FILE = 'orcid-publication-titles.csv'

    #reading data
    try:
      df = pd.read_csv(DATA_FOLDER + DATA_FILE)
    except Exception, ex:
      print '[e] %s' % str(ex)
      print '[i] it looks like no data were downloaded so far' 

    return df

class TwitterToWordCloud():

  def __init__(self, save_directory=None):
    """
      (obj) -> None

      Initializing the class.
    """
    
    print '[i] initializing class'

    if save_directory is None:
      save_directory = 'generated-orcid'
    print '[i] generated pngs will be saved inside "{}"'.format(save_directory)

    self.wc_helper = WordCloudHelper(save_directory)
    print '[i] initialing helper class'
    

    self.STOPWORDS = STOPWORDS
    print '[i] stopwords loaded'
    
    self.df = DataLoader().load_localdata()
    print '[i] data loaded'

    self.config_stopwords()
    print '[i] stopwords configured'

    self.wrangle_data()
    print '[i] data formatted'

  def config_stopwords(self):
    """
      (obj) -> None

      Configuring stopwords by adding more if required
    """
    more_stopwords = {'innojam', 'video', 'cebit2014'}
    self.STOPWORDS = STOPWORDS.union(more_stopwords)

  def wrangle_data(self):
    """
      (obj) -> None

      Wranling with data before porcessing it
    """

    # join ORCID publication titles to a single string
    words = ' '.join(self.df['pubtitle'])

    # remove URLs, RTs, and twitter handles
    cleaned_collection = " ".join([word for word in words.split()])
    self.words = cleaned_collection

  
  def generate_word_cloud(self, fonts, masks, name_prefix='some-wordcloud', bg_color='white'):
    """
      (obj, list, list, str) -> None
      
      Generating the word clouds with different masks and fonts and saving it as images.
    """

    if name_prefix is None:
      name_prefix = 'some-wordcloud'

    BASE_FOLDER = self.wc_helper.save_dir
    STOPWORDS = self.STOPWORDS
    print BASE_FOLDER

    from scipy.misc import imread

    for mask_name in masks:
      _mask_file = imread(masks[mask_name], flatten=True)
      _mask_width = len(_mask_file[0]) + 1
      _mask_height = len(_mask_file) + 1
      for font_name in fonts:
        _font_file = fonts[font_name]
        _img_name = '%s-%s-%s-%s' % (str(name_prefix), str(font_name), str(mask_name), str(bg_color))
        wordcloud = WordCloud( 
                      font_path=_font_file,
                      stopwords=STOPWORDS,
                      background_color=bg_color,
                      width=_mask_width,
                      height=_mask_height,
                      mask=_mask_file
                     ).generate(self.words)
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.savefig(BASE_FOLDER + _img_name, dpi=300)
        print '[i] image %s.png was generated ' % _img_name


  def process(self):
    """
      (obj) -> None

      Executing all methods relevant to processing.
    """
    some_fonts = ['monaco', 'menlo-regular', 'arvo-regular']
    #some_fonts = ['monaco']
    some_masks = ['r_and_d-01']

    fonts = self.wc_helper.load_fonts(some_fonts)
    masks = self.wc_helper.load_masks(some_masks)
    #fonts = self.wc_helper.load_fonts()
    #masks = self.wc_helper.load_masks()

    self.generate_word_cloud(fonts, masks, name_prefix='orcid-wordcloud')
    self.generate_word_cloud(fonts, masks, name_prefix='orcid-wordcloud', bg_color='black')

def main():
  """
    (None) -> None

    Main method that initiates instance of the class and starts processing.
  """

  twc = TwitterToWordCloud()
  twc.process()

if __name__ == '__main__':
  main()