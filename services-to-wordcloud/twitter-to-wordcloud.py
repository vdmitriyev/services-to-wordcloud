# coding: utf-8

__author__ = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "-"
__email__ = ""
__status__ = "test"
__date__ = "08.02.2015"
__description__ = "Yiny python utility that converts tweets cloud of words."

import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from helper import DirectoryHelper

class DataLoader():

  def load_data_web(self):
    """
      (Class) -> None or DataFrame

      Loading data stored somewhere on the web
    """
    
    #import urllib
    #url with dataset
    #url = "http://www.ats.ucla.edu/stat/data/binary.csv"
    
    #df = pd.read_csv(url)
    #return df
    return None

  def load_data_local(self):
    """
      (Class) -> None or DataFrame

      Loading data stored locally.
    """
    
    # set constants for the folder and file with data
    DATA_FOLDER = '../services/twitter/data/'
    DATA_FILE = 'twitter-data.csv'

    #reading data
    try:
      df = pd.read_csv(DATA_FOLDER + DATA_FILE)
    except Exception, ex:
      print '[e] %s' % str(ex)
      print '[i] it looks like no data were downloaded so far' 

    return df

class TwitterToWordCloud():

  def __init__(self):
    print '[i] initializing class'

    self.STOPWORDS = STOPWORDS
    print '[i] stopwords loaded'

    self.stop_words_configs()
    print '[i] stopwords configured'

    self.df = DataLoader().load_data_local()
    print '[i] data loaded'

    self.data_wrangling()
    print '[i] data formatted'

    self.helper = DirectoryHelper()
    self.helper.prepare_working_directory()
    print '[i] working directory prepared'


  def stop_words_configs(self):
    """
      Configuring stopwords by adding more if required
    """
    more_stopwords = {'innojam', 'video', 'cebit2014'}
    self.STOPWORDS = STOPWORDS.union(more_stopwords)

  def data_wrangling(self):
    """

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

  def load_fonts(self, selected_fonts=None):
    """
      (Class, list) -> dict

      Loading fonts as specified in the list or by itereting folder with fonts.
    """

    BASE_FOLDER = self.helper.upper_directory() + 'fonts\\'

    fonts = {}

    if selected_fonts is not None:
      for font in selected_fonts:
        fonts[font] = BASE_FOLDER + font + '.ttf'
    else:
      files = [f for f in os.listdir(BASE_FOLDER)]
      for f in files:
        if (f[-4:].lower() in ('.ttf')):
          fonts[f[:-4]] = BASE_FOLDER + f
    

    return fonts

  def load_masks(self, selected_masks=None):
    """
      (Class, list) -> dict

        Loading masks as specified in the list or by itereting folder with masks.
    """
    
    BASE_FOLDER = self.helper.upper_directory() + 'masks\\'

    masks = {}
    if selected_masks is not None:
      for mask in selected_masks:
        masks[mask] = BASE_FOLDER + mask + '.png'
    else:
      files = [f for f in os.listdir(BASE_FOLDER)]
      for f in files:
        if (f[-4:].lower() in ('.png')):
          masks[f[:-4]] = BASE_FOLDER + f

    return masks

  def generate_word_cloud(self, fonts, masks, bg_color='white'):
    """
      (Class, list, list, str) -> None
      
      Generating the word clouds with different masks and fonts and saving it as images.
    """

    BASE_FOLDER = 'generated\\'
    STOPWORDS = self.STOPWORDS

    from scipy.misc import imread

    for mask_name in masks:
      _mask_file = imread(masks[mask_name], flatten=True)
      for font_name in fonts:
        _font_file = fonts[font_name]
        _img_name = 'twitter-wordcloud-%s-%s-%s' % (str(font_name), str(mask_name), str(bg_color))
        wordcloud = WordCloud( 
                      font_path=_font_file,
                      stopwords=STOPWORDS,
                      background_color=bg_color,
                      width=1800,
                      height=1400,
                      mask=_mask_file
                     ).generate(self.words)
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.savefig(BASE_FOLDER + _img_name, dpi=300)
        print '[i] image %s.png was generated ' % _img_name


  def process(self):
    """
      Executing all methods relevant to processing.
    """

    some_fonts = ['monaco', 'menlo-regular', 'arvo-regular']
    some_masks = ['twitter_mask']

    #fonts = self.load_fonts(some_fonts)
    #masks = self.load_masks(some_masks)
    fonts = self.load_fonts()
    masks = self.load_masks()

    self.generate_word_cloud(fonts, masks)
    self.generate_word_cloud(fonts, masks, bg_color='black')

def main():
  """
    (None) -> None

    Main method that initiates instance of the class and starts processing.
  """

  twc = TwitterToWordCloud()
  twc.process()

if __name__ == '__main__':
  main()