from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd
import numpy as np

# Define a function to preprocess the text
def preprocess_text(text):
    # Tokenize the text
    tokens = text.lower().split()

    # Remove stopwords
    stopwords = set(['a', 'an', 'the', 'and', 'but', 'to', 'of', 'at', 'in', 'on', 'with', 'for', 'by', 'from', 'said'])
    tokens = [token for token in tokens if token not in stopwords]

    # Join the tokens back into a string
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

def Lda(articles, num_topics=1, num_words=1,max_df=0.90, min_df=1):
    """Apply Non-negative Matrix Factorization to the articles and return the topics and weights"""
    vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df,stop_words='english')
    X = vectorizer.fit_transform(articles)
    feature_names = vectorizer.get_feature_names_out()
    lda = LatentDirichletAllocation(n_components=num_topics, max_iter=10, random_state=10).fit(X)
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        topic_words = [feature_names[i] for i in topic.argsort()[:-num_words - 1:-1]]
        topics.extend(topic_words)
    return topics


def topic_model_nmf(articles, num_topics=1, num_words=1,max_df=0.90, min_df=1):
    """Apply Non-negative Matrix Factorization to the articles and return the topics and weights"""
    vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df,stop_words='english')
    X = vectorizer.fit_transform(articles)
    feature_names = vectorizer.get_feature_names_out()
    nmf = NMF(n_components=num_topics, max_iter=1000, random_state=10).fit(X)
    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        # print(type(topic))
        topic_words = [feature_names[i] for i in topic.argsort()[:-num_words - 1:-1]]
        topics.extend(topic_words)
        break
    return topics

def main():
    # Read our file which holds the NEWS
    filename = r'..\Scrapper\2022\2022-12-29\islamabad.csv'
    df = pd.read_csv(filename, index_col=None, header=0, dtype="string")
    for i in range(len(df)):
        topics_nmf = topic_model_nmf(list(preprocess_text(df.iloc[i]["Detail"]).split(" ")), num_topics=5, num_words=5)
        topics_lda = Lda(list(preprocess_text(df.iloc[i]["Detail"]).split(" ")), num_topics=5, num_words=5)
        topics = [topic for topic in topics_lda if topic in topics_nmf]
        print(topics)
if __name__ == '__main__':
    main()