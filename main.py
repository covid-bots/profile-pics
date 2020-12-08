#!/usr/bin/python3
import os
from io import BytesIO
import urllib.request
import urllib.error
import tempfile


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

    def __save_flag(self, url: str, dirpath: str, name: str, file_obj):
        """ Download and save the image in the given `path`, with the given `name`.
        If a `file_obj` is given, downloads the image into the `file_obj` instead. """

        ext = url.split('.')[-1]
        close_file = False

        if file_obj is None:
            # generate a file and open it
            self._assert_valid_dir_path(dirpath)
            name = name.replace("{code}", self.CODE)
            path = os.path.join(dirpath, name + '.' + ext)
            file_obj = open(path, mode="wb")
            close_file = True

        try:
            with urllib.request.urlopen(url) as response:
                data = response.read()
                file_obj.write(data)

        except urllib.error.HTTPError as e:
            raise ValueError(f"No flag found for country '{self.CODE}'")

        finally:
            if close_file:
                file_obj.close()

    def save_flag(self,
                  dirpath: str = os.getcwd(),
                  name="{code}",
                  file_obj=None,
                  ):
        """ Saves the country flag (1:1 ratio), svg format. """
        self.__save_flag(self.flag_url, dirpath=dirpath,
                         name=name, file_obj=file_obj)

    def save_flag_4x3(self,
                      dirpath: str = os.getcwd(),
                      name="{code}_4x3",
                      file_obj=None,
                      ):
        """ Saves the country flag (4:3 ratio), svg format. """
        self.__save_flag(self.flag_4x3_url, dirpath=dirpath,
                         name=name, file_obj=file_obj)

    def flag(self,):
        pass

    def flag_4x3(self,):
        pass
