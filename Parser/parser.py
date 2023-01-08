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

    def clean(self, doc):
        doc = doc.lower()
        doc = nlp(doc)
        tokens = [tokens.lower_ for tokens in doc]
        tokens = [tokens for tokens in doc if (tokens.is_stop == False)]
        tokens = [tokens for tokens in tokens if (tokens.is_punct == False)]
        try:
            final_token = [WordNetLemmatizer().lemmatize(token.text)
                       for token in tokens]
        except:
            import nltk
            nltk.download('wordnet')
            nltk.download('omw-1.4')
            final_token = [WordNetLemmatizer().lemmatize(token.text)
                       for token in tokens]
        

        return " ".join(final_token)

    # split sentences

    def sentences(self, text):
        # split sentences and questions
        text = re.split('[.?]', text)
        clean_sent = []
        for sent in text:
            clean_sent.append(sent)
        return clean_sent

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

    def Get_location(self, read_more, header):
        if len(self.index) <= 0:
            self.load_cities("Alldata_refined.csv")
        header = header.lower()
        header = self.clean(header)
        header = header.split()
        text = self.sentences(self.clean(read_more))
        cities = dict()
        for i in text:
            doc = nlp(i)
            jump = 0
            for token in range(len(doc)):
                try:
                    if token < jump:
                        continue
                    jump = 0
                    if doc[token].pos_ == "PROPN":
                        flag = False
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
                        for areas in range(start, end):
                            words = self.Data_of_region[areas].split()
                            subtoken = token
                            checker = []
                            if fuzz.ratio(doc[subtoken].text.lower(),words[0])>=95:
                                checker.append(words[0])
                                for iterator in range(len(words)-1):
                                    if subtoken + (iterator + 1 ) < len(doc):
                                        if fuzz.ratio(doc[subtoken + iterator+1 ].text.lower(),words[iterator+1])>=70:
                                            checker.append(words[iterator+1])
                                city = ' '.join(checker)
                                if len(previous) < len(city): 
                                    area_count = len(checker)
                                    flag = True
                                    previous = city
                                else:
                                    city = previous
                        if flag:
                            match = False
                            word1 = ""
                            word2 = ""
                            if token != 0:
                                word1 = doc[token-1].text.lower()
                            jump = token + area_count
                            if jump + 1 < len(doc):
                                word2 = doc[jump+1].text.lower()
                            if word1 in header or word2 in header:
                                match = True
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
    # Find spark library to automatically find and start the Spark instance that is installed on the system, 
    # without having to manually specify the path to the Spark home directory
    import findspark
    findspark.init()
    # Create a Spark Session
    spark = SparkSession.builder.appName("NAaaS").getOrCreate()
    print("Code ran till here 5")   
    print("SPARK: ", spark)
    # for filename in glob.iglob(r'islamabad.csv', recursive=True):
    # df = spark.read.csv(r"/opt/bitnami/spark/parser/Parser/islamabad.csv", header=True, inferSchema=True)
        # path = pathlib.PurePath(filename)
        # print("Code ran till here 0")   
        # fileName = path.name[:-4]
    # Read the file as a pandas dataframe
    df = pd.read_csv(r"islamabad.csv", index_col=None, header=0, dtype="string")
        # print(df.to_markdown())
        # df['Creation_Date'] = path.parent.name
        # df['Link'] = "https://www.dawn.com/newspaper/" + fileName + "/" + path.parent.name
        # li.append(df)
        # df = pd.concat(li, axis=0, ignore_index=True)
    # Convert the dataframe to a dictionary
    rows = df.to_dict('records')
    # rdd = df.rdd
    # Convert it into rdd list of elements to run on multiple worker on spark
    rdd = spark.sparkContext.parallelize(rows)
        # # print(rdd.collect())
    # rdd = df.rdd
    print("Code ran till here 1")
    # RUn the Parser.read function on all elements in the rdd
    result = rdd.map(Parser.read)
    print("Code ran till here 2")
    # Print the result after implementing the function
    print(result.collect())
    # Stop the Spark session
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
