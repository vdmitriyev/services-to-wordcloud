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
__description__ = "Main class and some helper class for the word cloud"

import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from helper_directory import DirectoryHelper

"""Main class that transerf the service data to the word cloud."""
class ServiceToWordCloud(object):
  def __init__(self, data_file, data_folder, save_directory=None):
    """
      (obj) -> None

      Initializing the class.
    """
    
    print '[i] initializing class'

    if save_directory is None:
      save_directory = 'generated-noname-service'

    print '[i] generated pngs will be saved inside "{}"'.format(save_directory)

    self.wc_helper = WordCloudHelper(save_directory)
    print '[i] initialing helper class'
    
    self.STOPWORDS = STOPWORDS
    print '[i] stopwords loaded'
    
    self.df = DataLoader().localdata(data_file, data_folder)
    print '[i] data loaded'

    self.config_stopwords()
    print '[i] stopwords configured'

    # self.wrangle_data()
    

  def config_stopwords(self, more_stopwords=None):
    """
      (obj) -> None

      Configuring stopwords by adding more if required
    """

    if more_stopwords is not None:
      self.STOPWORDS = STOPWORDS.union(more_stopwords)

  def wrangle_data(self, df_field):
    """
      (obj) -> None

      Wranling with data before porcessing it
    """

    assert df_field is not None, \
          "df_field should not be None\ncheck vairable or override wrangle_data() method"

    # joining together words from the dataset
    words = ' '.join(self.df[df_field])

    # remove URLs, RTs, and twitter handles
    cleaned_collection = " ".join([word for word in words.split()])
    self.words = cleaned_collection

    print '[i] data formatted'

  
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


  def process(self, service_name=None, fonts=None, masks=None):
    """
      (obj) -> None

      Executing all methods relevant to processing.
    """

    if service_name is None:
      service_name = 'noname-service-wordcloud'

    if fonts is None:
      fonts = self.wc_helper.load_fonts()
    else:
      fonts = self.wc_helper.load_fonts(fonts)


    if masks is None:
      masks = self.wc_helper.load_masks()
    else:
      masks = self.wc_helper.load_masks(masks)


    self.generate_word_cloud(fonts, masks, name_prefix=service_name)
    self.generate_word_cloud(fonts, masks, name_prefix=service_name, bg_color='black')

"""Class that is responsinble for data masks and fonts."""
class WordCloudHelper():

  def __init__(self, work_dir=None):
    """
      (obj, str) -> None

      Initializing the class.
    """

    # assert work_dir is not None, \
    #       "work_dir should not be None"

    self.dir_helper = DirectoryHelper(work_dir)
    self.save_dir = self.dir_helper.work_dir
    self.dir_helper.prepare_working_directory()

    print '[i] working directory prepared'

  def load_fonts(self, selected_fonts=None):
    """
      (obj, list) -> dict

      Loading fonts as specified in the list or by itereting folder with fonts.
    """

    BASE_FOLDER = self.dir_helper.upper_directory() + 'fonts\\'

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
        (obj, list) -> dict

        Loading masks as specified in the list or by itereting folder with masks.
    """
    
    BASE_FOLDER = self.dir_helper.upper_directory() + 'masks\\'

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

""" Class that is responsinble for data load."""
class DataLoader():

  def webdata(self):
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

  def localdata(self, data_file, data_folder):
    """
      (class) -> DataFrame

      Loading data stored locally.
    """

    assert data_file is not None, \
          "data_file should not be None"
    assert data_folder is not None, \
          "data_folder should not be None"

    #reading data
    try:
      df = pd.read_csv(data_folder + data_file, encoding='utf-8')
    except Exception, ex:
      print '[e] %s' % str(ex)
      print '[i] it looks like no data were downloaded so far' 

    return df
