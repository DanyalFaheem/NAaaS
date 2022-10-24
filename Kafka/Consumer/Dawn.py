from Scrapping import Scrapper
import os
from bs4 import BeautifulSoup
import datetime
import requests
import pandas as pd


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
        self.Dawn_links, self.Previous_Date = self.Generate_Date_links_for_Dawn(
            General_CAT, Metro_CAT)
        self.Scrap_Dawn(General_CAT, Metro_CAT)

    def Generate_Date_links_for_Dawn(self, GC, MC):
        Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
        Previous_Date = Previous_Date.strftime('%Y-%m-%d')
        Links = []
        for i in GC:
            Links.append("https://www.dawn.com/newspaper/" +
                         str(i)+"/"+str(Previous_Date))
        for i in MC:
            Links.append("https://www.dawn.com/newspaper/" +
                         str(i)+"/"+str(Previous_Date))

        return Links, Previous_Date

    def Scrap_Dawn(self, GC, MC):
        path = str(datetime.datetime.strptime(
            self.Previous_Date, "%Y-%m-%d").year) + "/" + str(self.Previous_Date)
        try:
            os.mkdir(path)
        except:
            pass
        count1 = 0
        count2 = 0
        flag = False
        with requests.Session() as session:
            for i in self.Dawn_links:
                Headers = []
                Summary = []
                Read_more = []
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
                            detail = self.extract_readmore(links[0]['href'])
                            Read_more.append(detail)
                            read_more = True
                dictionary = {'Header': Headers,
                              'Summary': Summary, 'Detail': Read_more}
                dataframe = pd.DataFrame(dictionary)

                if count1 < len(GC):
                    Spath = path+"/"+GC[count1]+".csv"
                    self.savefile(Spath, dataframe)
                    count1 += 1
                else:
                    Spath = path+"/"+MC[count2]+".csv"
                    self.savefile(Spath, dataframe)
                    count2 += 1

    def extract_readmore(self, link):
        detail = ""
        webpage = self.req(link)
        soup = BeautifulSoup(webpage, 'html.parser')
        for reading in soup.find_all('article'):
            for p in reading.find_all("div",  attrs={"class": "story__content overflow-hidden text-4 sm:text-4.5 pt-1 mt-1"}):
                detail += p.get_text()
        return detail


Dawn()
