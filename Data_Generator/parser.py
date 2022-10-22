from nltk.stem.wordnet import WordNetLemmatizer
import spacy
import re
import pandas as pd
nlp = spacy.load('en_core_web_sm', disable=['ner', 'textcat'])


class parser():
    def __init__(self):
        pass

    def clean(doc):
        doc = doc.lower()
        doc = nlp(doc)
        tokens = [tokens.lower_ for tokens in doc]
        tokens = [tokens for tokens in doc if (tokens.is_stop == False)]
        tokens = [tokens for tokens in tokens if (tokens.is_punct == False)]
        final_token = [WordNetLemmatizer().lemmatize(token.text)
                       for token in tokens]

        return " ".join(final_token)

    # split sentences

    def sentences(text):
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
        self.load_cities()
        header = header.lower()
        header = self.clean(header)
        header = header.split()
        text = self.sentences(self.clean(read_more))
        cities = dict()
        for i in text:
            doc = nlp(i)
            for token in range(len(doc)):
                if doc[token].pos_ == "PROPN":
                    flag = False
                    end = self.index[doc[token].text.lower()[0]]
                    if end == self.index['a']:
                        start = 0
                    else:
                        start = chr(ord(doc[token].text.lower()[0])-1)
                        while (True):
                            if start in self.index:
                                start = self.index[start]-1
                                break
                            else:
                                start = chr(ord(start)-1)
                    area_count = 0
                    for areas in range(start, end):
                        words = self.Data_of_region[areas].split()
                        subtoken = token
                        checker = []
                        for iterator in range(len(words)):
                            if subtoken + iterator < len(doc):
                                if doc[subtoken+iterator].text.lower() == words[iterator]:
                                    checker.append(1)
                        if len(checker) == len(words):
                            city = ' '.join(words)
                            area_count = len(words[iterator])
                            flag = True
                            break
                    if flag:
                        match = False
                        word1 = ""
                        word2 = ""
                        if token != 0:
                            word1 = doc[token-1].text.lower()
                        subtoken = token + area_count
                        if subtoken + 1 < len(doc):
                            word2 = doc[subtoken+1].text.lower()
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
        return cities
