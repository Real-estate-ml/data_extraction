# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import re
import logging
import os
from google.cloud import storage
import pandas as pd
import argparse

BUCKET = "ml-esme-real-estate-data"

parser = argparse.ArgumentParser()
parser.add_argument('--date', required=True, help='Acquisition date to extract')

args = parser.parse_args()
extraction_date = args.date
print("The extracting service for {} is starting...".format(extraction_date))


client = storage.Client()
data_path = BUCKET + extraction_date

html_files = []
# Se connecter au bucket et récupérer un fichier
for blob in client.list_blobs(BUCKET, prefix="logic-immo/raw/"+extraction_date):
    html_files.append(blob.download_as_string())

price_clean = []
room_clean = []
superficie_clean = []
location_clean = []

def get_attributes(files):
    for i in range(0, len(files)):
        soup = BeautifulSoup(files[i], "html.parser")

        # Price
        try:
            # On récupère les prix des biens sur Paris
            price = soup.find("span", {"class": "infoPrice"})
            for i in price:
                regex = re.compile(r'[^\d]+')
                price_clean.append(regex.sub("", i.text))
        except:
            price_clean.append("None")

        # Room
        try:
            # On récupère les prix des biens sur Paris
            room = soup.find("em", {"class": "feature mobileOnly"})
            for i in room:
                regex = re.compile(r'[^\d]+')
                room_clean.append(regex.sub("", i.text))
        except:
            room_clean.append("None")

        # Arrondissement
        try:
            # On récupère les prix des biens sur Paris
            location = soup.find("em", {"class": "infoAdresse"})
            for i in location:
                regex = re.compile(r'[^\d]+')
                location_clean.append(regex.sub("", i.text))
        except:
            location_clean.append("None")

        # Superficie
        try:
            # On récupère les prix des biens sur Paris
            superficie = soup.find("em", {"class": "feature"})
            for i in superficie:
                regex = re.compile(r'[^\d]+')
                superficie_clean.append(regex.sub("", i.text))
        except:
            superficie_clean.append("None")

    print(len(price_clean), len(room_clean), len(location_clean), len(superficie_clean))
    df_Datas = pd.DataFrame({"Prix": price_clean, "Rooms": room_clean, "Cdp": location_clean, "Surface": superficie_clean})
    return df_Datas

def export_csv_to_gcs(csv_name):
    bucket = client.bucket(BUCKET)
    blob = bucket.blob("logic-immo/clean/{}/{}".format(extraction_date, csv_name))
    blob.upload_from_filename(csv_name)

# Création dataframe
df_Datas = get_attributes(html_files)

#Drop number of arrondissment and clean
df_Datas['Adresse'] = df_Datas['Cdp'].str.extract(r'(75\d{3}\-?)')
df_Datas = df_Datas.drop(['Cdp'], axis=1)

# Export en CSV
csv_name = "df_Datas.csv"
df_Datas.to_csv(csv_name)
print(df_Datas)

export_csv_to_gcs(csv_name)
print("The CSV file has been exported to Google Cloud Storage")