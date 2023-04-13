from datetime import date, timedelta
from pickle import dump, load
import datetime
from Scrapping import Scrapper
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import pathlib

class Tribune(Scrapper):
    def __init__(self):
        super().__init__()
        self.Tribune_links = []
        self.Tribune_Frame = []
        self.Tribune()

    def Tribune(self):
        General_CAT = ["front", "back",
                       "national", "business", "international", "sports","balochistan","azad-jamu-kashmir-gilgit"]
        Metro_CAT = ["karachi", "lahore", "islamabad"]
        self.Scrap_Tribune(General_CAT, Metro_CAT)

    def Generate_Date_links_for_Tribune(self, GC, MC, mdate):
        Links = []
        for i in GC:
            Links.append("https://tribune.com.pk/listing/" +
                         str(i)+"/"+str(mdate))
        for i in MC:
            Links.append("https://tribune.com.pk/listing/" +
                         str(i)+"/"+str(mdate))

        return Links, mdate

    def Scrap_Tribune(self, GC, MC):
        file = open('start_date.pkl', 'rb')
        start_date = load(file)
        file.close()
        end_date = date(2021, 1, 1)
        delta = timedelta(days=1)
        while start_date >= end_date:
            print(start_date.strftime("%Y-%m-%d"))
            self.Tribune_links, self.Previous_Date = self.Generate_Date_links_for_Tribune(
                GC, MC, start_date)
            Previous_Date_str = self.Previous_Date.strftime('%Y-%m-%d')
            path = str(datetime.datetime.strptime(
            Previous_Date_str, "%Y-%m-%d").year) + "/" + str(Previous_Date_str)
            try:
                os.mkdir(path)
            except:
                pass
            count1 = 0
            count2 = 0
            with requests.Session() as session:
                for i in self.Tribune_links:
                    print("Now Scraping link: ", i)
                    Headers = []
                    Summary = []
                    Read_more = []
                    Links = []
                    Categories = []
                    Pic_url = []
                    webpage = self.req(i)
                    soup = BeautifulSoup(webpage, 'html.parser')
                    for story in soup.findAll('ul'):
                        for j in story.find_all('li'):
                            try:
                                a_tag = j.find('div',attrs={'class':'horiz-news3-caption'})
                                if(a_tag !=None):
                                    start_index = i.find("/listing/") + len("/listing/")
                                    end_index = i.find("/", start_index)
                                    if start_index != -1 and end_index != -1:
                                        word = i[start_index:end_index]
                                    Categories.append(word)
                                    Headers.append(a_tag.h2.text.strip())
                                    Summary.append(a_tag.p.text.strip())
                                    Links.append(a_tag.a['href'])
                                    detail,img = self.extract_readmore(
                                    a_tag.a['href'])
                                    Read_more.append(detail)
                                    Pic_url.append(img)
                            except:
                                continue
                    Date = start_date.strftime("%Y-%m-%d")
                    
                    if (len(Headers)>0):
                        dictionary = {'Header': Headers,
                                    'Summary': Summary, 'Detail': Read_more, 'Link': Links, 'Category': Categories, 'CreationDate': Date, 'Pic_url':Pic_url}
                        dataframe = pd.DataFrame(dictionary)
                        
                        if count1 < len(GC):
                            Spath = path+"/"+GC[count1]+".csv"
                            dataframe.to_csv(Spath)
                            dataframe.insert(0,"Keys",GC[count1])
                            df_json = dataframe.to_dict()
                            if not os.path.exists("jsons/"+path+"/"):
                                os.makedirs("jsons/"+path+"/")
                            with open("jsons/"+path+"/"+"Scrapped.json", 'w') as json_file:
                                    json.dump(df_json, json_file)
                            
                            count1 += 1
                        
                        else:
                            Spath = path+"/"+MC[count2]+".csv"
                            dataframe.to_csv(Spath)
                            dataframe.insert(0,"Keys",MC[count2])
                            df_json = dataframe.to_dict()
                            if not os.path.exists("jsons/"+path+"/"):
                                os.makedirs("jsons/"+path+"/")
                            with open("jsons/"+path+"/"+"Scrapped.json", 'w') as json_file:
                                    json.dump(df_json, json_file)
                            count2 += 1 
            start_date -= delta
            file = open('start_date.pkl', 'wb')
            dump(start_date, file)
            file.close()

    def extract_readmore(self, link):
        detail = ""
        webpage = self.req(link)
        soup = BeautifulSoup(webpage, 'html.parser')
        for reading in soup.find_all("span",attrs= {"class": "story-text"}):
            for p in reading.find_all("p"):
                detail += p.get_text()
                detail += "\n"
        try:
            div_tag = soup.find('div', class_='story-featuredimage')
            img_tag = div_tag.find('div', {'class': 'featured-image-global'}).find('img')
            data_src = img_tag.get('data-src')
        except:
                data_src = ""
        return detail,data_src


Tribune()
