# coding: utf-8

# maing testing library
import pyorcid

# additional libraries
import os
import json
import codecs

# loading bibtex parser
import bibtexparser

# setting logging to the DEBUG mode
import logging

#logging.getLogger("#orcid#").setLevel(logging.DEBUG)
logging.getLogger("#orcid#").setLevel(logging.INFO)


class OrcidPublicationAbstracts():

    def __init__(self, orcid_id, csv_file_name):

        self.data = {}

        self.orcid_id = orcid_id
        print '[i] ORCID {} will be processed'.format(self.orcid_id)
        self.csv_file_name = csv_file_name

        self.orcid = pyorcid.get(self.orcid_id)
        print '[i] data of from the ORCID retrieved'

    def save_bibtex(self, bibtex, file_name='orcid-bibtex-output', encoding='utf-8'):
        """
        (dict, str, str) -> None
        Saving bibtex to the file, grouped by year.
        """

        if not os.path.exists('data'):
            os.makedirs('data')

        full_path = 'data\\' + file_name + '.bib'
        _file = codecs.open(full_path, 'w', encoding)

        for key in bibtex:
            _file.write("%%%%%%%%%%%%%%%% \n%% %s \n%%%%%%%%%%%%%%%%\n\n" % key)
            bibtex_group = ''
            for value in bibtex[key]:
                bibtex_group += value + '\n\n'
            _file.write(bibtex_group)

        _file.close()

        print '[i] bibtex was created, check following file: %s ' % (file_name)

    def bibtex_abstracts(self):
        """
            (class) -> dict()

            Method takes as an input object with all publications from ORCID and forms dict with it.
        """

        bibtex = {}
        for value in self.orcid.publications:
            if value.citation.citation_type == 'BIBTEX':
                if value.publicationyear not in bibtex:
                    bibtex[value.publicationyear] = list()
                    bibtex[value.publicationyear].append(value.citation.citation)
                else:
                    bibtex[value.publicationyear].append(value.citation.citation)
            else:
                print '[i] this publications is having no BIBTEX {}'.format(value)

        self.save_bibtex(bibtex)

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

        self.bibtex_abstracts()
        #self.save_csv(self.csv_file_name)


def main():
  """
    (None) -> None

    Main method that initiates instance of the class and starts processing.
  """

  _orcid_id = '0000-0001-5661-4587'  
  
  csv_file_name = "orcid-publication-abstracts"
  op = OrcidPublicationAbstracts(_orcid_id, csv_file_name)
  op.process()

if __name__ == '__main__':
  main()