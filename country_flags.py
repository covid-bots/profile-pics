#!/usr/bin/python3
from difflib import SequenceMatcher
import babel
import babel.languages
import os


class Country:

    FLAGS_DIR_PATH = os.path.join("assets", "flags")

    FLAGS = [
        flag.split('.')[0]
        for flag in os.listdir(FLAGS_DIR_PATH)
        if ".png" in flag
    ]

    def __init__(self, country_code: str):
        self._assert_valid_country_code(country_code)

        base_lang = babel.Locale('en')

        self.__code = country_code.upper()
        self.__name = base_lang.territories[self.code]
        self.__lang_code = self.get_territory_language_code(self.code).upper()
        self.__lang_locale = babel.Locale(self.lang_code.lower())
        self.__lang_name = self.lang_locale.get_display_name(base_lang)

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name

    @property
    def lang_code(self):
        return self.__lang_code

    @property
    def lang_locale(self):
        return self.__lang_locale

    @property
    def lang_name(self):
        return self.__lang_name

    @staticmethod
    def get_territory_language_code(code: str):
        info = babel.languages.get_territory_language_info(code)
        return max(info, key=lambda lang_code: info[lang_code]["population_percent"])

    @staticmethod
    def _assert_valid_country_code(code: str):
        """ Assert that the country code passed as a parameter is valid.
        Raises an Type/Value Errors if needed. """

        if not isinstance(code, str):
            raise TypeError("Country code must be a string")

        if len(code) != 2:
            raise ValueError("Country code must be a 2 character string")

    def matching_flag_name(self):
        ratios = [SequenceMatcher(None, self.name, flag).ratio()
                  for flag in self.FLAGS]
        match_index = ratios.index(max(ratios))
        return self.FLAGS[match_index]

    def _flag_name_to_path(self, flag: str):
        return os.path.join(self.FLAGS_DIR_PATH, f"{flag}.png")

    def matching_flag(self):
        """ Returns an pillow image object representing the flag of the country. """
        from PIL import Image

        flag_name = self.matching_flag_name()
        path = self._flag_name_to_path(flag_name)
        return Image.open(path)
