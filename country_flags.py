#!/usr/bin/python3
from difflib import SequenceMatcher
import os


class Country:

    country: str
    FLAGS_DIR_PATH = os.path.join("assets", "flags")

    FLAGS = [
        flag.split('.')[0]
        for flag in os.listdir(FLAGS_DIR_PATH)
        if ".png" in flag
    ]

    def __init__(self, country: str):
        self.country = country.lower()

        self.FLAG_PATHS = [
            self._flag_name_to_path(flag)
            for flag in self.FLAGS
        ]

    def _flag_name_to_path(self, flag: str):
        return os.path.join(self.FLAGS_DIR_PATH, f"{flag}.png")

    def matching_flag_name(self):
        ratios = [SequenceMatcher(None, self.country, flag).ratio()
                  for flag in self.FLAGS]
        match_index = ratios.index(max(ratios))
        return self.FLAGS[match_index]

    def matching_flag(self):
        """ Returns an pillow image object representing the flag of the country. """
        from PIL import Image

        flag_name = self.matching_flag_name()
        path = self._flag_name_to_path(flag_name)
        return Image.open(path)
