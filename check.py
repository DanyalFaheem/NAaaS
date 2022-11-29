from nltk.stem.wordnet import WordNetLemmatizer
import spacy
from fuzzywuzzy import fuzz
import re
import pandas as pd
# import threading
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nlp = spacy.load('en_core_web_sm', disable=['ner', 'textcat'])


class parser():
    def __init__(self):
        pass

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

    def Get_location(self, read_more, header):
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
        self.city = max(cities, key=cities.get)
        self.cities = cities


    def read(self):
        # def read(self):
        df = pd.read_csv('2022/2022-09-12/front-page.csv')
        list = df.values.tolist()
        for i in range(len(list)):
            self.Get_location(list[i][3],list[i][2])
            print("News: ",i+1,"city: ",self.cities)
            # location,
                            #   args=(list[3][3], list[3][2],))
        # t2 = threading.Thread(target=print_cube, args=(10,))

        # starting thread 1
        # t1.start()
        # starting thread 2
        # t2.start()

        # wait until thread 1 is completely executed
        # t1.join()
        # wait until thread 2 is completely executed
        # t2.join()
        # print(self.Get_location(list[0][3], list[0][2]))
        # print(list[3][2])
        # sentiment = SentimentIntensityAnalyzer()
        # sent_1 = sentiment.polarity_scores(list[3][2])

        # print("Sentiment of text:", sent_1)


obj = parser()
obj.read()
