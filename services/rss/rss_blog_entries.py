# coding: utf-8

# main package for RSS parsing
import feedparser

# additional libraries
import os
import json
import codecs

# setting logging to the DEBUG mode
import logging

#logging.getLogger("#orcid#").setLevel(logging.DEBUG)
logging.getLogger("#orcid#").setLevel(logging.INFO)

# configd for teh CSV
CSV_FIELD_NAME = 'rssEntry'
CSV_DELIM = ','

class RSSParser():

    def __init__(self, rss_url, csv_file_name):

        self.data = {}

        self.rss_url = rss_url
        print '[i] rss url will be processed {} '.format(self.rss_url)
        self.csv_file_name = csv_file_name

        self.rss_data = feedparser.parse(self.rss_url)
        print '[i] data retrieved from rss'

    
    def parse_rss(self):
        """
            (obj) -> list

            Printing author publications
        """

        def normalize_data(input_data):
            """
                (str) -> (str)

                Interenal method that normalizes data from the feed
            """
            result = input_data.replace(CSV_DELIM,"")
            result = result.replace("\n","")
            return result

        rss = self.rss_data
        self.data[CSV_FIELD_NAME] = list()
        for index in range(len(rss.entries)):
            try:
                self.data[CSV_FIELD_NAME].append(normalize_data(rss.entries[index].content[0].value))
            except Exception, ex:
                print '[e] exception {}'.format(str(ex))

    def save_csv(self, file_name=None):
        """
            (obj, str) -> None

            Checks if the directory 'data' exists, creates it otherwise.
            Saves the data from twitter in csv using pandas.
        """

        if not os.path.exists('data'):
            os.makedirs('data')

        if file_name is None:
            file_name = self.csv_file_name

        # coverting data into csv
        _csv_data = 'ID' + CSV_DELIM + CSV_FIELD_NAME + '\n'
        for index, value in enumerate(self.data[CSV_FIELD_NAME]):
            _csv_data += str(index) + CSV_DELIM + value + '\n'

        # saving to the csv file
        full_path = 'data\\' + file_name + '.csv'
        _csv_file = codecs.open(full_path, 'w', 'utf8')
        _csv_file.write(_csv_data)
        _csv_file.close()

        print '[i] rss data saved into "{}"'.format(full_path)

    def process(self):
        """
            (obj) -> None
            Extrating publication titles from ORCID and saving into CSVs
        """

        self.parse_rss()
        self.save_csv()


def main():
  """
    (None) -> None

    Main method that initiates instance of the class and starts processing.
  """

  rss_url = 'https://vdmitriyev.wordpress.com/feed/'
  
  csv_file_name = "rss-entries"
  rss = RSSParser(rss_url, csv_file_name)
  rss.process()

if __name__ == '__main__':
  main()