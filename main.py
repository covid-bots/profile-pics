#!/usr/bin/python3
import os
from io import BytesIO
import urllib.request
import urllib.error


class Country:

    CODE: str

    def __init__(self, country_code: str):
        self._assert_valid_country_code(country_code)
        self.CODE = country_code.lower()

    @staticmethod
    def _assert_valid_country_code(code: str):
        """ Assert that the country code passed as a parameter is valid.
        Raises an Type/Value Errors if needed. """

        if not isinstance(code, str):
            raise TypeError("Country code must be a string")

        if len(code) != 2:
            raise ValueError("Country code must be a 2 character string")

    @staticmethod
    def _assert_valid_dir_path(dirpath: str):
        if not os.path.isdir(dirpath):
            raise ValueError("Path is not a directory")

    @property
    def flag_url(self):
        """ Returns a url to svg image (1:1 ratio) representing the country flag.
        Using the "flag icon css" library, created by lipis.
        https://github.com/lipis/flag-icon-css
        """

        return f"https://raw.githubusercontent.com/lipis/flag-icon-css/master/flags/1x1/{self.CODE}.svg"

    @property
    def flag_4x3_url(self):
        """ Returns a url to svg image (4:3 ratio) representing the country flag.
        Using the "flag icon css" library, created by lipis.
        https://github.com/lipis/flag-icon-css
        """

        return f"https://raw.githubusercontent.com/lipis/flag-icon-css/master/flags/4x3/{self.CODE}.svg"

    def __save_flag(self, url: str, dirpath: str, name: str):
        self._assert_valid_dir_path(dirpath)

        # generate saving path
        ext = url.split('.')[-1]
        name = name.replace("{code}", self.CODE)
        save_path = os.path.join(dirpath, name + '.' + ext)

        # download the image
        try:
            urllib.request.urlretrieve(url, save_path)
        except urllib.error.HTTPError as e:
            raise ValueError(f"No flag found for country '{self.CODE}'")

    def save_flag(self,
                  dirpath: str = os.getcwd(),
                  name="{code}"
                  ):
        self.__save_flag(self.flag_url, dirpath=dirpath, name=name)

    def save_4x3_flag(self,
                      dirpath: str = os.getcwd(),
                      name="{code}_4x3"
                      ):
        self.__save_flag(self.flag_4x3_url, dirpath=dirpath, name=name)
