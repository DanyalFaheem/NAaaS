from Scrap import Scrapper
from bs4 import BeautifulSoup
import requests
import time
import re
import csv
import datetime
import pandas as pd
import os


def update_csv(file_name, update_dict):
    # Read existing CSV file
    with open(file_name, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames

    # Check if header matches and update existing rows
    for i, row in enumerate(rows):
        if row['Header'] in update_dict['Header']:
            j = update_dict['Header'].index(row['Header'])
            for k in headers:
                if k in update_dict and k != 'Header':
                    row[k] = update_dict[k][j]

    # Add new rows for headers that didn't match
    for i, header in enumerate(update_dict['Header']):
        if header not in [row['Header'] for row in rows]:
            new_row = {'Header': header}
            for k in headers:
                if k in update_dict and k != 'Header':
                    new_row[k] = update_dict[k][i]
            rows.append(new_row)

    # Write updated CSV file
    with open(file_name, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def get_minutes_since_update(s):
    # Extract the time information using regular expressions
    match = re.search(
        r'updated\s+(\d+)\s+(?:hour|minute)s?(?:\s+(\d+)\s+minute)?s?\s+ago', s, re.IGNORECASE)
    if match:
        # Get the number of minutes based on the time information
        hours, minutes = match.groups()
        if s[match.end(1)+1] == 'm' or s[match.end(1)+1] == 'M' :
            return int(hours)
        else:
            minutes = 0
        minutes += int(hours) * 60
    else:
        # Extract the date information using regular expressions
        match = re.search(
            r'updated\s+(\w+)\s+(\d+),\s+(\d+)', s, re.IGNORECASE)
        if match:
            return -1

        # If no time or date information found, return -1
        return -1

    return minutes



news_holder = dict()


class Tribune(Scrapper):
    def __init__(self):
        super().__init__()
        self.link = "https://tribune.com.pk/latest"
        self.Tribune()

    def Tribune(self):
        self.Scrap_Tribune()

    def Scrap_Tribune(self):
        flag_1 = True
        iterator = 2
        attach_string = "?page="
        i = self.link
        while (flag_1):
            with requests.Session() as session:
                print("Now Scraping link: ", i)
                Headers = []
                Summary = []
                Read_more = []
                Links = []
                Categories = []
                Pic_url = []
                webpage = self.req(i)
                soup = BeautifulSoup(webpage, 'html.parser')
                for story in soup.findAll('ul', attrs={'class': 'tedit-shortnews listing-page'}):
                    for j in story.find_all('li'):
                        append_flag = False
                        a_tag = j.find(
                            'div', attrs={'class': 'horiz-news3-caption'})
                        if (a_tag != None):
                            minutes = get_minutes_since_update(a_tag.span.text)
                            if a_tag.h2.text in news_holder:
                                value = news_holder[a_tag.h2.text]
                                if minutes == -1:
                                    flag_1 = False
                                elif minutes < value:
                                    append_flag = True
                                elif minutes >= value:
                                    print("Working fine")
                            else:
                                if minutes == -1:
                                    flag_1 = False
                                else:
                                    news_holder[a_tag.h2.text] = minutes
                                    append_flag = True

                            if append_flag:
                                Categories.append("Live")
                                Headers.append(a_tag.h2.text.strip())
                                Summary.append(a_tag.p.text.strip())
                                Links.append(a_tag.a['href'])
                                detail, img = self.extract_readmore(
                                    a_tag.a['href'])
                                Read_more.append(detail)
                                Pic_url.append(img)

                if (len(Headers) > 0):
                    Date = datetime.datetime.today().strftime('%Y-%m-%d')
                    dictionary = {'Header': Headers,
                                  'Summary': Summary, 'Detail': Read_more, 'Link': Links, 'Category': Categories, 'CreationDate': Date,  'Pic_url': Pic_url}
                    try:
                        df = pd.DataFrame(dictionary)
                        df.to_csv("Live.csv", mode='a', header=not os.path.exists("Live.csv"), index=False)
                        # update_csv("Live.csv", dictionary)
                    except:
                        pass

                i = self.link
                i = i + attach_string + str(iterator)
                iterator = iterator + 1
                if (flag_1 == False):
                    break
                print("Flag value", flag_1)

    def extract_readmore(self, link):
        detail = ""
        webpage = self.req(link)
        soup = BeautifulSoup(webpage, 'html.parser')
        for reading in soup.find_all("span", attrs={"class": "story-text"}):
            for p in reading.find_all("p"):
                detail += p.get_text()
                detail += "\n"
        div_tag = soup.find('div', class_='story-featuredimage')
        img_tag = div_tag.find(
            'div', {'class': 'featured-image-global'}).find('img')
        data_src = img_tag.get('data-src')
        return detail, data_src


while(True):
    Tribune()
    print(news_holder)
    # Wait for 10 minutes
    time.sleep(600)