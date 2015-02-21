# coding: utf-8

# main library for ORCID
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

    def __init__(self, orcid_id, csv_file_name, load=True):
        """
            (class, str, str, boolean) -> None

            Method that initialtes all very first activities.
        """

        self.load = load
        self.data = {}

        self.orcid_id = orcid_id
        print '[i] ORCID {} will be processed'.format(self.orcid_id)
        self.csv_file_name = csv_file_name

        if self.load:
            self.orcid = pyorcid.get(self.orcid_id)
            print '[i] data of from the ORCID retrieved'
        else:
            print '[i] data won\'t be loaded, the already loaded bibtex will be used'

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

        print '[i] bibtex was created, check following file: {}'.format(full_path)

    def extract_bibtex(self):
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

    def parse_bibtex(self, full_path=None):
        """
            (class, str) -> None
        """

        if full_path is None:
            full_path = 'data\\orcid-bibtex-output.bib'

        with open(full_path) as bibtex_file:
            bibtex_str = bibtex_file.read()

        bib_database = bibtexparser.loads(bibtex_str)
        self.data['pubabstract'] = list()
        for _bibtex in bib_database.entries:
            try:
                self.data['pubabstract'].append(_bibtex['abstract'])
            except Exception, ex:
                print '[e] exception {}'.format(str(ex))

    def save_csv(self, file_name=None):
        """
            (obj, str) -> None

            Checks if the directory 'data' exists, creates it otherwise.
            Saves the data from twitter in csv using pandas.
        """

        if file_name is None:
            file_name = self.csv_file_name

        if not os.path.exists('data'):
            os.makedirs('data')

        # coverting data into csv
        _csv_data = "pubabstract" + "\n"
        for value in self.data["pubabstract"]:
            _csv_data += value.replace(',', '') + "\n"

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

        if self.load:
            self.extract_bibtex()

        self.parse_bibtex()
        self.save_csv()

def main():
  """
    (None) -> None

    Main method that initiates instance of the class and starts processing.
  """

  _orcid_id = '0000-0001-5661-4587'  
  
  csv_file_name = "orcid-publications-abstracts"
  opa = OrcidPublicationAbstracts(_orcid_id, csv_file_name, load=True)
  opa.process()

if __name__ == '__main__':
  main()