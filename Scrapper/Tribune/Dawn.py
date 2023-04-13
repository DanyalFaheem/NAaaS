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

class Dawn(Scrapper):
    def __init__(self):
        super().__init__()
        self.Dawn_links = []
        self.Dawn_Frame = []
        self.Dawn()

    def Dawn(self):
        General_CAT = ["front-page", "back-page",
                       "national", "business", "international", "sport"]
        Metro_CAT = ["karachi", "lahore", "islamabad", "peshawar"]
        self.Scrap_Dawn(General_CAT, Metro_CAT)

    def Generate_Date_links_for_Dawn(self, GC, MC, mdate):
        Links = []
        for i in GC:
            Links.append("https://www.dawn.com/newspaper/" +
                         str(i)+"/"+str(mdate))
        for i in MC:
            Links.append("https://www.dawn.com/newspaper/" +
                         str(i)+"/"+str(mdate))

        return Links, mdate

    def Scrap_Dawn(self, GC, MC):
        file = open('start_date.pkl', 'rb')
        start_date = load(file)
        file.close()
        end_date = date(2021, 1, 1)
        delta = timedelta(days=1)
        while start_date >= end_date:
            self.Dawn_links, self.Previous_Date = self.Generate_Date_links_for_Dawn(
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
            flag = False
            with requests.Session() as session:
                for i in self.Dawn_links:
                    print("Now Scraping link: ", i)
                    Headers = []
                    Summary = []
                    Read_more = []
                    Links = []
                    Categories = []
                    webpage = self.req(i)
                    soup = BeautifulSoup(webpage, 'html.parser')
                    for story in soup.findAll('article'):
                        for head in story.find_all("h2"):
                            Headers.append(head.text.strip())
                        sum_flag = False
                        read_more = False
                        for summary in story.find_all("div"):
                            if sum_flag == False:
                                Summary.append(summary.text.strip())
                                sum_flag = True
                            elif read_more == False:
                                detail = ""
                                links = summary.findAll('a')
                                detail = self.extract_readmore(
                                    links[0]['href'])
                                Read_more.append(detail)
                                read_more = True
                        category = pathlib.Path(i).parts[-2]
                        Categories.append(category)
                        Links.append(links[0]['href'])
                        Date = start_date.strftime("%Y-%m-%d")
                        print(Date, type(Date))
                    dictionary = {'Header': Headers,
                                  'Summary': Summary, 'Detail': Read_more, 'Link': Links, 'Category': Categories, 'CreationDate': Date}
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
        # print(link)
        soup = BeautifulSoup(webpage, 'html.parser')
        for reading in soup.find_all('article'):
            for p in reading.find_all("div",  attrs={"class": "story__content overflow-hidden text-4 sm:text-4.5 pt-1 mt-1"}):
                detail += p.get_text()
        return detail


Dawn()
