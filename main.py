from bs4 import BeautifulSoup
import re
import logging
import os
import cloudstorage as gcs
from google.cloud import storage
import pandas as pd


# Se connecter au bucket et récupérer un fichier
html_files = []
for i in range(1, 41):
    client = storage.Client()
    bucket = client.get_bucket('ml-esme-real-estate-data')
    blob = bucket.get_blob('logic-immo/apartment_ad_'+str(i)+'_18-02-2022.html')
    html_files.append(blob.download_as_string())
    print(len(html_files))


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
            price_clean.append("None")

        # Arrondissement
        try:
            # On récupère les prix des biens sur Paris
            location = soup.find("em", {"class": "infoAdresse"})
            for i in location:
                regex = re.compile(r'[^\d]+')
                location_clean.append(regex.sub("", i.text))
        except:
            price_clean.append("None")

        # Superficie
        try:
            # On récupère les prix des biens sur Paris
            superficie = soup.find("em", {"class": "feature"})
            for i in superficie:
                regex = re.compile(r'[^\d]+')
                superficie_clean.append(regex.sub("", i.text))
        except:
            price_clean.append("None")

    df_Datas = pd.DataFrame({"Prix": price_clean, "Rooms": room_clean, "Adresse": location_clean, "Surface": superficie_clean})
    return df_Datas


# Création dataframe
df_Datas = get_attributes(html_files)

#Drop number of arrondissment and clean
df_Datas['Code_postal'] = df_Datas['Adresse'].str.extract(r'(75\d{3}\-?)')
df_Datas = df_Datas.drop(['Adresse'], axis=1)

# Export en CSV
df_Datas.to_csv(r'df_Datas.csv')
print(df_Datas)


"""
def get_attributes(file):
    soup = BeautifulSoup(file, "html.parser")
    room = soup.find("em", {"class": "feature mobileOnly"})
    superficie = soup.find("em", {"class": "feature"})
    location = soup.find("em", {"class": "infoAdresse"})
    price = soup.find("span", {"class": "infoPrice"})
    details =[]
    for i in room:
        regex = re.compile(r'[^\d]+')
        details.append(int(regex.sub("", i.text)))
    for i in location:
        regex = re.compile(r'[^\d]+')
        details.append(int(regex.sub("", i.text)))
    for i in superficie:
        regex = re.compile(r'[^\d]+')
        details.append(int(regex.sub("", i.text)))
    for i in price:
        regex = re.compile(r'[^\d]+')
        details.append(int(regex.sub("", i.text)))
    return (details)


print(get_attributes(html_files[0]))
"""

