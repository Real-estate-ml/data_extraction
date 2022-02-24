from bs4 import BeautifulSoup
import re

def run():
    #connect to GCP bucket
    #return list of all HTML files (raw)
    html_files = []
    # instantiate connection with Postgre
    for html in html_files:
        # read with BeautifulSoup
        # run cleaning functions
        # store in Postgre
        # Move the raw html file to history bucket

def get_attributes(file):
    soup = BeautifulSoup(file, "html.parser")
    room = soup.find("em", {"class": "feature mobileOnly"})
    superficie = soup.find("em", {"class": "feature"})
    location = soup.find("em", {"class": "infoAdresse"})
    price = soup.find("span", {"class": "infoPrice"})
    location_clean=[]
    superficie_clean = []
    room_clean = []
    price_clean = []
    for i in room:
        regex = re.compile(r'[^\d]+')
        room_clean.append(regex.sub(" ", i.text))
    for i in location:
        regex = re.compile(r'[^\d]+')
        location_clean.append(regex.sub(" ", i.text))
    for i in superficie:
        regex = re.compile(r'[^\d]+')
        superficie_clean.append(regex.sub(" ", i.text))
    for i in price:
        regex = re.compile(r'[^\d]+')
        price_clean.append(regex.sub(" ", i.text))
    return (price_clean, room_clean, location_clean, superficie_clean)


f = open('data_brut.html', "r")
page = f.read()
f.close()
print(get_attributes(page))

