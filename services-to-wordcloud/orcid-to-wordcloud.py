# coding: utf-8

__author__ = "Viktor Dmitriyev"
__copyright__ = "Copyright 2015, Viktor Dmitriyev"
__credits__ = ["Viktor Dmitriyev"]
__license__ = "MIT"
__version__ = "1.3.0"
__maintainer__ = "-"
__email__ = ""
__status__ = "dev"
__date__ = "14.02.2015"
__description__ = "Tiny python utility that converts ORCID publication titles into cloud of words."

from helper_wordcloud import ServiceToWordCloud

""" Class to conver publication titles from ORCID into Word Cloud"""
class OrcidTitlesServiceToWC(ServiceToWordCloud):

	def __init__(self, *args, **kwargs):
		"""
		(obj, *args, **kwargs) -> None
		Initializing the parent class as well as intializing data wrangler
		"""

		super(OrcidTitlesServiceToWC, self).__init__(*args, **kwargs)
		df_field = 'pubtitle'
		self.wrangle_data(df_field)

""" Class to conver publication abstracts from ORCID into Word Cloud"""
class OrcidAbstractsServiceToWC(ServiceToWordCloud):
	def __init__(self, *args, **kwargs):
		"""
		(obj, *args, **kwargs) -> None

		Initializing the parent class as well as intializing data wrangler
		"""

		super(OrcidAbstractsServiceToWC, self).__init__(*args, **kwargs)
		df_field = 'pubabstract'
		self.wrangle_data(df_field)

def process_titles():
  # setting params for word cloud
  data_file = 'orcid-publications-titles.csv'
  data_folder = '../services/orcid/data/'
  save_directory = 'generated-orcid'
  service_name = 'orcid-titles-wordcloud'
  fonts = ['monaco']
  masks = ['r-and-d-mask']

  owc = OrcidTitlesServiceToWC(data_file, data_folder, save_directory)
  #owc.process(service_name)
  owc.process(service_name, fonts, masks)


def process_abstracts():
  # setting params for word cloud
  data_file = 'orcid-publications-abstracts.csv'
  data_folder = '../services/orcid/data/'
  save_directory = 'generated-orcid'
  service_name = 'orcid-abstracts-wordcloud'
  fonts = ['monaco']
  masks = ['square-mask']

  owc = OrcidAbstractsServiceToWC(data_file, data_folder, save_directory)
  #owc.process(service_name)
  owc.process(service_name, fonts, masks)


def main():
  """
    (None) -> None

    Main method that initiates instance of the class and starts processing.
  """
  
  #process_titles():
  process_abstracts()

if __name__ == '__main__':
  main()

