""" Generates and saves profile pictures from all of the
countries supported by the covid API. """

from PIL import Image
from country_flags import Country
import os
import requests
from tqdm import tqdm

# Configurations

FLAG_SIZE = (630, 630)      # width, height (px)
FLAG_POSITION = (251, 304)  # top left xy position (px)

BASE_DIR = os.getcwd()
OUTPUT_FOLDER = os.path.join(BASE_DIR, "profilepics")
os.mkdir(OUTPUT_FOLDER)

# Load base image
base_img = Image.open(os.path.join(
    BASE_DIR, "assets", "profile-pic-template.png"))

# Get countries from API
response = requests.get("https://api.covid19api.com/countries").json()
for country in tqdm(response):
    country_obj = Country(country["Country"])

    # Load the flag
    flag = country_obj.matching_flag().resize(FLAG_SIZE)
    flag_base = Image.new(mode="RGBA",
                          color=(255, 0, 0, 0),
                          size=base_img.size)
    flag_base.paste(flag, FLAG_POSITION)

    # combine flag and template image
    final = Image.alpha_composite(flag_base, base_img)
    save_path = os.path.join(OUTPUT_FOLDER, country["Slug"] + ".png")
    final.save(save_path)
