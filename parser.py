# Importing modules for Temporal extraction 
from nltk.stem.wordnet import WordNetLemmatizer
import spacy
from fuzzywuzzy import fuzz
import re
import pandas as pd
import glob
import pathlib
import json
# from sutime import SUTime
from datetime import datetime
import datefinder
import numpy as np
import csv
import os
from pyspark.sql import *
from pyspark import *


nlp = spacy.load('en_core_web_sm', disable=['ner', 'textcat'])


class TimeTag:
    def __init__(self, date, textType, appearence, count):
        self.date = date
        self.textType = textType
        self.appearence = appearence
        self.count = count
        self.weight = 0.0
        self.calculateWeight()

    def calculateWeight(self):
        if self.textType == "Header":
            self.weight = 10 * (1/self.appearence) * self.count
        elif self.textType == "Summary":
            self.weight = 5 * (1/self.appearence) * self.count
        elif self.textType == "Details":
            self.weight = 2 * (1/self.appearence) * self.count
    
    def __repr__(self):
        print({"date": self.date, "weight": self.weight, "count": self.count, "type": self.textType})



class parser():
    def __init__(self):
        self.index = {}

    # Function to clean the string
    def clean(self, doc):
        # Convert all alphabets to lower case
        doc = doc.lower()
        # Loading string in to nlp model 
        doc = nlp(doc)
        # Tokenizing the string

        tokens = [tokens.lower_ for tokens in doc]
        # Removing all stopping words from the string
        tokens = [tokens for tokens in doc if (tokens.is_stop == False)]
        # Removing all punctuation from the string
        tokens = [tokens for tokens in tokens if (tokens.is_punct == False)]
        # Changing all verbs to its base form (changing - > change , changed -> change etc)
        try:
            final_token = [WordNetLemmatizer().lemmatize(token.text)
                       for token in tokens]
        except:
            # If modules are not loaded properly 
            import nltk
            nltk.download('wordnet')
            nltk.download('omw-1.4')
            final_token = [WordNetLemmatizer().lemmatize(token.text)
                       for token in tokens]
        
        # Returning back the final string 
        return " ".join(final_token)

    
    # Converting string into sentences 
    def sentences(self, text):
        # split sentences and questions
        text = re.split('[.?]', text)
        clean_sent = []
        for sent in text:
            clean_sent.append(sent)
        return clean_sent

    # Load cities from data set provided by ECP Election commission of Pakistan
    def load_cities(self, file):
        # Loading dataset
        df = pd.read_csv(file)
        # Droping NULL rows
        df = df.dropna()
        # Extracting location col
        df = df["Locations"]
        # Converting Data frame to sorted list in lower case
        Data_of_region = df.values.tolist()
        Data_of_region = [each_city.lower() for each_city in Data_of_region]
        Data_of_region = list(dict.fromkeys(sorted(Data_of_region)))
        # Storing indexes of each alphabet starting index
        index = dict()
        # Helping variables to store indexes
        flag = False
        push = False
        current_alphabet = ""
        start = 0
        finish = 0
        # Creating index hash
        for i in range(len(Data_of_region)):
            if i != 0 and Data_of_region[i][0] != Data_of_region[i][0]:
                flag = True
                push = True
                finish = i-1
            if push == True:
                index[current_alphabet] = finish
            if flag == False:
                start = i
                current_alphabet = Data_of_region[i][0]
                index.__setitem__(current_alphabet, start)
        self.index = index
        self.Data_of_region = Data_of_region

    def createTags(self, tags):
        tagValues = []
        newTags = []
        for tag in tags:
            try: 
                tagValues.append(list(datefinder.find_dates(tag["value"]))[0])
                newTags.append(tag)
            except:
                pass
        tagValues, indices, counts = np.unique(tagValues, return_index=True, return_counts=True)
        newTags = [newTags[index] for index in indices]
        newtags = []
        for i in range(len(newTags)):
            newtags.append(TimeTag(tagValues[i], newTags[i]["textType"], newTags[i]["start"], counts[i]))
        return newtags

    def addTextType(self, tags, textType):
        for tag in tags:
            tag["textType"] = textType
        return tags

    # FGet location from the extracted news 
    def Get_location(self, read_more, header):
        if len(self.index) <= 0:
            # Loading data set of ECP Election commission of Pakistan 
            self.load_cities("Alldata_refined.csv")
        # Clean header of news
        header = self.clean(header)
        # Split header
        header = header.split()
        # Generate sentences from the article  
        text = self.sentences(self.clean(read_more))
        # Dictionary to store the City counts from news
        cities = dict()
        for i in text:
            # For each sentence in the article load it in nlp model
            doc = nlp(i)
            # A skipper variable  
            jump = 0
            # Foe each word in the sentence 
            for token in range(len(doc)):
                try:
                    # If the word is already explored skip the iteration
                    if token < jump:
                        continue
                    jump = 0
                    # Check if the extracted word is a proper noun
                    if doc[token].pos_ == "PROPN":
                        flag = False
                        # Extracting the start and end index where the first alphabet of proper noun matches with the the location loaded
                        # From ECP data
                        end = self.index[doc[token].text.lower()[0]]
                        if end == self.index['a']:
                            start = 0
                        else:
                            start = chr(ord(doc[token].text.lower()[0])-1)
                            # print(self.index, start)
                            start = self.index[start]
                            start += 1
                        area_count = 0
                        previous = ""
                        # Check only those entries which first alphabet matches with the first alphabet of proper noun
                        for areas in range(start, end):
                            words = self.Data_of_region[areas].split()
                            subtoken = token
                            checker = []
                            # Check the match (not exact matching of the noun and the location)
                            if fuzz.ratio(doc[subtoken].text.lower(),words[0])>=95:
                                checker.append(words[0])
                                for iterator in range(len(words)-1):
                                    # If first token matches extract more data from sentence and compare it for full name of the location
                                    if subtoken + (iterator + 1 ) < len(doc):
                                        if fuzz.ratio(doc[subtoken + iterator+1 ].text.lower(),words[iterator+1])>=70:
                                            checker.append(words[iterator+1])
                                city = ' '.join(checker)
                                # If noun and the location matches (turn on the match flag)
                                if len(previous) < len(city): 
                                    area_count = len(checker)
                                    flag = True
                                    previous = city
                                else:
                                    city = previous
                        # Check if the extracted location has any match with the header
                        if flag:
                            match = False
                            word1 = ""
                            word2 = ""
                            if token != 0:
                                word1 = doc[token-1].text.lower()
                            # Storing the number of extra read we did from the text
                            # Thus we can skip those token in the next iteration 
                            jump = token + area_count
                            if jump + 1 < len(doc):
                                word2 = doc[jump+1].text.lower()
                            if word1 in header or word2 in header:
                                match = True
                            # If the sentence in which the location is found has any co relation with the header increase its weight 
                            if city in cities:
                                if match:
                                    cities[city] += 3
                                else:
                                    cities[city] += 1
                            else:
                                if match:
                                    cities.__setitem__(city, 3)
                                else:
                                    cities.__setitem__(city, 1)
                except:
                    continue
        # Extract the maximum count which will represent the focused locaiton of the news
        self.city = max(cities, key=cities.get, default="null")
        if self.city == 0:
            print(cities)
        df = pd.read_csv("Alldata_refined.csv")
        # Droping NULL rows
        df = df.dropna()
        # Extracting location col
        # df = df["Locations"]
        df["Locations"] = df["Locations"].apply(lambda x: x.upper())
        # print(df["Locations"])
        if df[df["Locations"] == self.city.upper()].empty:
            if self.city != "null":
                flag = False
                cityList = sorted(((v,k) for k,v in cities.items()), reverse=True)
                for city in cityList:
                    if df[df["Locations"] == city[1].upper()].empty == False:
                        self.city = city[1]
                        flag = True
                        break
            
            if flag == False: 
                self.city = "null"
        self.cities = cities

    def Get_Time(self, data, sutime, timeData):
        tags = []
        # timeData[data[0]] = dict()

        headerParse = sutime.parse(data[1], reference_date=data[6])
        headerParse = self.addTextType(headerParse, "Header")
        
        summaryParse = sutime.parse(data[2], reference_date=data[6])
        summaryParse = self.addTextType(summaryParse, "Summary")
        
        details = data[3]
        lines = details.split('\n')
        del lines[-2]
        details = '\n'.join(lines)
        detailsParse = sutime.parse(details, reference_date=data[6])
        detailsParse = self.addTextType(detailsParse, "Details")
        
        tags = headerParse + summaryParse + detailsParse
        # print(tags)
        try:
            tags = self.createTags(tags)
        # print(tags)
            tags = sorted(tags, key=lambda x: x.weight, reverse=True)
            timeData["focusTime"] = tags[0].date.date().strftime('%Y-%m-%d')
        except:
            timeData["focusTime"] = data[6]
        
        timeData["CreationDate"] = data[6]
        
        timeData["Header"] = dict()
        timeData["Header"]["Text"] = data[1]
        timeData["Header"]["Tags"] = headerParse
        
        timeData['Summary'] = dict()
        timeData['Summary']["Text"] = data[2]
        timeData['Summary']["Tags"] = summaryParse
        
        timeData['Details'] = dict()
        timeData['Details']["Text"] = details
        timeData['Details']["Tags"] = detailsParse

        timeData['Link'] = data[4]
        timeData['Category'] = data[5]
        return timeData

    def read(self, dataFrame):

        # print(dataFrame)
        self.Get_location(dataFrame["Detail"], dataFrame["Header"])
        return self.city




def main():
    # sutime = SUTime()
    li = []
    Parser = parser()
    # sc = SparkContext(appName="MyApp")
    import findspark
    findspark.init()
    spark = SparkSession.builder.appName("NAaaS").getOrCreate()
    print("Code ran till here 5")   
    print("SPARK: ", spark)
    # for filename in glob.iglob(r'islamabad.csv', recursive=True):
    # df = spark.read.csv(r"/opt/bitnami/spark/parser/Parser/islamabad.csv", header=True, inferSchema=True)
        # path = pathlib.PurePath(filename)
        # print("Code ran till here 0")   
        # fileName = path.name[:-4]
    df = pd.read_csv(r"islamabad.csv", index_col=None, header=0, dtype="string")
        # print(df.to_markdown())
        # df['Creation_Date'] = path.parent.name
        # df['Link'] = "https://www.dawn.com/newspaper/" + fileName + "/" + path.parent.name
        # li.append(df)
        # df = pd.concat(li, axis=0, ignore_index=True)
    rows = df.to_dict('records')
    # rdd = df.rdd
    rdd = spark.sparkContext.parallelize(rows)
        # # print(rdd.collect())
    # rdd = df.rdd
    print("Code ran till here 1")
    result = rdd.map(Parser.read)
    print("Code ran till here 2")
    print(result.collect())
    spark.stop()
        # for i in range(len(df)):
        #     # print(list(df.loc[i])[5])
        #     # results = dict()
        #     city = Parser.read(df.loc[i])   
        #     print(city)
    #         if city != "null":
    #             results = Parser.Get_Time(list(df.loc[i]), sutime, results)
    #             results["focusLocation"] = city
    #             resultsDF = pd.DataFrame(results)
    #             resultsDF = resultsDF.transpose()
    #             del resultsDF["Tags"]
    #             resultsDF = resultsDF.transpose()
    #             # resultsDF = resultsDF.iloc[:, 1:]
    #             # print(resultsDF.to_markdown())
    #             # print(resultsDF.head(1))
    #             resultsDF.to_csv("Results.csv", mode='a', header=not os.path.exists("Results.csv"), index=False)
    #         else:
    #             continue
    # os.remove("Results.csv")
    # # print(df.head(1))

main()
