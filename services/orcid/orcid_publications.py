# coding: utf-8

# maing testing library
import pyorcid

# additional libraries
import os
import json
import codecs

# setting logging to the DEBUG mode
import logging

#logging.getLogger("#orcid#").setLevel(logging.DEBUG)
logging.getLogger("#orcid#").setLevel(logging.INFO)

class OrcidPublications():

    def __init__(self, orcid_id, csv_file_name):

        self.data = {}

        self.orcid_id = orcid_id
        print '[i] ORCID {} will be processed'.format(self.orcid_id)
        self.csv_file_name = csv_file_name

        self.orcid = pyorcid.get(self.orcid_id)
        print '[i] data of from the ORCID retrieved'

    def author_keywords(self):
        """
            (obj) -> None

            Printing keywords of the authors
        """

        keywords = self.orcid.keywords
        print keywords
        for key_word in keywords:
            print key_word

    def author_publications(self):
        """
            (obj) -> list

            Printing author publications
        """

        self.data['pubtitle'] = list()
        publications = self.orcid.publications
        for value in publications:
            self.data['pubtitle'].append(value.title)

    def save_csv(self, file_name):
        """
            (obj, str) -> None

            Checks if the directory 'data' exists, creates it otherwise.
            Saves the data from twitter in csv using pandas.
        """

        if not os.path.exists('data'):
            os.makedirs('data')

        # coverting data into csv
        _csv_data = "pubtitle" + "\n"
        for value in self.data["pubtitle"]:
            _csv_data += value + "\n"

        # saving to the csv file
        full_path = 'data\\' + file_name + '.csv'
        _csv_file = codecs.open(full_path, 'w', 'utf8')
        _csv_file.write(_csv_data)
        _csv_file.close()

        print '[i] orcid publications saved into "{}"'.format(full_path)

    def process(self):
        """
            (obj) -> None
            Extrating publication titles from ORCID and saving into CSVs
        """

        self.author_publications()
        self.save_csv(self.csv_file_name)


def main():
  """
    (None) -> None

    Main method that initiates instance of the class and starts processing.
  """

  alfonso_orcid_id = '0000-0001-8855-5569'  
  
  csv_file_name = "orcid-publication-titles"
  op = OrcidPublications(alfonso_orcid_id, csv_file_name)
  op.process()

if __name__ == '__main__':
  main()