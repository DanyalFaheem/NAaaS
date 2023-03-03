from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import csv
import numpy as np

def read_csv(file_path):
    """Read the csv file and return a list of articles"""
    articles = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader) # skip header row
        for row in reader:
            articles.append(row[0])
    return articles

# Define a function to preprocess the text
def preprocess_text(text):
    # Tokenize the text
    tokens = text.lower().split()

    # Remove stopwords
    stopwords = set(['a', 'an', 'the', 'and', 'but', 'to', 'of', 'at', 'in', 'on', 'with', 'for', 'by', 'from'])
    tokens = [token for token in tokens if token not in stopwords]

    # Join the tokens back into a string
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

def topic_model_nmf(articles, num_topics=1, num_words=1,max_df=0.90, min_df=1):
    """Apply Non-negative Matrix Factorization to the articles and return the topics and weights"""
    vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df,stop_words='english')
    X = vectorizer.fit_transform(articles)
    feature_names = vectorizer.get_feature_names_out()
    nmf = NMF(n_components=num_topics, max_iter=1000, random_state=10).fit(X)
    topic_weights = nmf.transform(X).mean(axis=0)
    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        topic_words = [feature_names[i] for i in topic.argsort()[:-num_words - 1:-1]]
        word_weights = topic / topic.sum()  # compute the weight of each word within the topic
        topics.append((topic_idx, topic_weights[topic_idx], topic_words, word_weights))
    return topics


def main():
    articles = read_csv('Article.csv')
    print(len(articles))
    # Can generate multple topics and multiple words regarding each topic 
    topics = topic_model_nmf(list(preprocess_text(articles[3]).split(" ")), num_topics=5, num_words=5)
    for topic_idx, topic_weight, topic_words, word_weights in topics:
        print(f"Topic {topic_idx} (weight={topic_weight:.2f}): {topic_words}")

if __name__ == '__main__':
    main()