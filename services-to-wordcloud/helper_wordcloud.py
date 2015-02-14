# coding: utf-8

__author__ = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "-"
__email__ = ""
__status__ = "dev"
__date__ = "14.02.2015"
__description__ = "Helper class for wordcloud."

import os
from helper_directory import DirectoryHelper

class WordCloudHelper():

  def __init__(self, work_dir=None):
    """
      (obj, str) -> None

      Initializing the class.
    """

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

