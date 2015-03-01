# coding: utf-8
#!/usr/bin/env python

__author__ = 'Viktor Dmitriyev'
__copyright__ = 'Copyright 2015, Viktor Dmitriyev'
__credits__ = ['Viktor Dmitriyev']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = '-'
__email__ = ''
__status__ = 'dev'
__date__ = '26.01.2015'
__description__ = 'Helper for the crawler that manages directory'

import os
import string
import random
import codecs
import shutil
from time import gmtime, strftime

RAND_RANGE = 7


class DirectoryHelper():

    """Class to help managing directories."""

    def __init__(self, proposed_dir=None):
        """
            (obj, str) -> None

            Initializing the class.
        """

        WORK_DIRECTORY = 'generated'
        if proposed_dir is not None:
            WORK_DIRECTORY = proposed_dir

        self.current_dir = os.path.dirname(os.path.abspath(__file__)) + '\\'
        self.work_dir = self.current_dir + WORK_DIRECTORY + '\\'

    def clear_directory(self, directory):
        """
            (obj, str) -> None

            Clears given 'directory'.
        """

        for root, dirs, files in os.walk(directory):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def create_directory_ondemand(self, directory):
        """
            (obj, str) -> None

            Creating directory on demand.
        """

        if not os.path.exists(directory):
            os.makedirs(directory)

    def prepare_working_directory(self):
        """
            (obj) -> None

            Prepearing current directory for working:
                -    checking if temp folder is existing and creating it;
                -    clearing temp directory;
                -
        """

        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)

        self.clear_directory(self.work_dir)

    def move_from_work_directory(self):
        """
            (obj) -> None

            Current method will implement versioning of publication.
        """

    def upper_directory(self):
        """
            (obj) -> None

            Identify upper directory.
        """

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        up_dir = cur_dir[:cur_dir.rfind('\\')] + '\\'
        return up_dir

    def save_file(self, file_name, text, encoding='utf-8'):
        """
            (obj, str, str, str) -> None

            Save to 'file_name' given 'text'.
        """
        _file = codecs.open(file_name, 'w', encoding)
        _file.write(text)
        _file.close()

    def save_img_file(self, file_name, img, ):
        """
            (obj,str,str) -> None

            Save to 'file_name' given 'img'.
        """
        _file = codecs.open(file_name, 'wb')
        _file.write(img)
        _file.close()

        # with open(file_name, 'w') as content_file:
        #     content = content_file.write(text)

    def read_file(self, file_name):
        """
            (obj, str) -> (str)

            Reads text from 'file_name' and return it
        """
        with open(file_name, 'r') as file_input:
            file_content = file_input.read()
        return file_content

    def read_file_utf8(self, file_name):
        """
            (obj, str) -> (str)

            Reads text from 'file_name' as UTF-8 and return it
        """

        with codecs.open(file_name, 'r', encoding='utf8') as f:
            file_content = f.read()

        return file_content

    def gen_file_name(self, extention='.html', name=None):
        """
            (obj, str) -> (str)

            Generate file name
        """

        rand_path_range = ''.join(
            random.choice(string.ascii_lowercase + string.digits) for x in range(RAND_RANGE))
        if name is None:
            new_file_name = strftime(
                '%Y-%m-%d', gmtime()) + '-' + rand_path_range + extention
        else:
            new_file_name = name + '-' + rand_path_range + extention

        return new_file_name
