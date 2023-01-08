from Scrapping import Scrapper
import os
from bs4 import BeautifulSoup
import datetime
import requests
import pandas as pd


# Creating Dawn class to scrapp dawn data
# Inherited basic functionality from Scrapper class
class Dawn(Scrapper):
    def __init__(self):
        super().__init__()
        self.Dawn_links = []
        self.Dawn_Frame = []
        self.Dawn()

    def Dawn(self):
        # All News catagories available on the site
        General_CAT = ["front-page", "back-page",
                       "national", "business", "international", "sport"]
        # Catagories specific to the metro city available on the site
        Metro_CAT = ["karachi", "lahore", "islamabad", "peshawar"]
        # Calling function to generate link allowing to access each catagories 
        self.Dawn_links, self.Previous_Date = self.Generate_Date_links_for_Dawn(
            General_CAT, Metro_CAT)
        # Initiate scrapping
        self.Scrap_Dawn(General_CAT, Metro_CAT)

    # Function that can generate links to access define catagories
    def Generate_Date_links_for_Dawn(self, GC, MC):
        # Initializing the date (News links usually have date-catagories kind of syntax )
        Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
        Previous_Date = Previous_Date.strftime('%Y-%m-%d')
        Links = []
        # GC stands for General category 
        for i in GC:
            Links.append("https://www.dawn.com/newspaper/" +
                         str(i)+"/"+str(Previous_Date))
        # MC for Metro city catagories
        for i in MC:
            Links.append("https://www.dawn.com/newspaper/" +
                         str(i)+"/"+str(Previous_Date))

        return Links, Previous_Date

    # Scrapper that will take the links (in Dawn case it has two kind of links general category and metro city category)
    def Scrap_Dawn(self, GC, MC):
        # Creating directory to store the data specific to the category with in the directory created by scrapper module init()
        path = str(datetime.datetime.strptime(
            self.Previous_Date, "%Y-%m-%d").year) + "/" + str(self.Previous_Date)
        try:
            os.mkdir(path)
        except:
            pass
        count1 = 0
        count2 = 0
        flag = False
        # session request loop
        with requests.Session() as session:
            for i in self.Dawn_links:
                # We need header summary and article of the news 
                Headers = []
                Summary = []
                Read_more = []
                # Requesting the link 
                webpage = self.req(i)
                # Creating the bs4 object
                soup = BeautifulSoup(webpage, 'html.parser')
                # Getting article tag
                for story in soup.findAll('article'):
                    # Finding h2 tag
                    for head in story.find_all("h2"):
                        # Append it as header 
                        Headers.append(head.text.strip())
                    # Variable required for logic
                    sum_flag = False
                    read_more = False
                    # Getting all div tags inside the article tag
                    for summary in story.find_all("div"):
                        # If summary is not extracted yet
                        if sum_flag == False:
                            # Append the summary
                            Summary.append(summary.text.strip())
                            # Make summary extraction true avoid replication of summary 
                            sum_flag = True
                        # If article is not yet extracted 
                        elif read_more == False:
                            detail = ""
                            # Find href from summary tag
                            links = summary.findAll('a')
                            # Extract the entire article
                            detail = self.extract_readmore(links[0]['href'])
                            # Append the article
                            Read_more.append(detail)
                            read_more = True
                # Creating dictionary 
                dictionary = {'Header': Headers,
                              'Summary': Summary, 'Detail': Read_more}
                # Type casting dictionary to data frame to store in csv file
                dataframe = pd.DataFrame(dictionary)

                # Check if the current count is on General category 
                if count1 < len(GC):
                    # Add the category name in saving ( easy to determine which category news are present in the file)
                    Spath = path+"/"+GC[count1]+".csv"
                    # Save file
                    self.savefile(Spath, dataframe)
                    count1 += 1
                # Else if general cottagey list is exhausted thus Metro city news have to be saved
                else:
                    # Add the category name in saving ( easy to determine which category news are present in the file)
                    Spath = path+"/"+MC[count2]+".csv"
                    # Save file
                    self.savefile(Spath, dataframe)
                    count2 += 1
    # Function to extract the entire article of the news
    def extract_readmore(self, link):
        detail = ""
        webpage = self.req(link)
        # Generating request to for scrapping
        soup = BeautifulSoup(webpage, 'html.parser')
        # From page extract all the article tags
        for reading in soup.find_all('article'):
            # from all article tags get the specific tags mentioned in the class
            for p in reading.find_all("div",  attrs={"class": "story__content overflow-hidden text-4 sm:text-4.5 pt-1 mt-1"}):
                detail += p.get_text()
        # Send back the extracted article from the scrapped raw page data
        return detail


