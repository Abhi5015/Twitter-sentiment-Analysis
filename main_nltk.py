import string
from collections import Counter

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.data import find

# Ensure NLTK resources are available
try:
    find('corpora/stopwords.zip')
    find('tokenizers/punkt.zip')
    find('corpora/wordnet.zip')
except:
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

# Read and preprocess text
text = open('read.txt', encoding='utf-8').read()
lower_case = text.lower()
cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

# Using word_tokenize for tokenization
tokenized_words = word_tokenize(cleaned_text, "english")

# Removing Stop Words
stop_words = set(stopwords.words('english'))
final_words = [word for word in tokenized_words if word not in stop_words]

# Lemmatization - Normalize words
lemmatizer = WordNetLemmatizer()
lemma_words = [lemmatizer.lemmatize(word) for word in final_words]

# Load emotions and check
emotion_list = []
with open('emotions.txt', 'r') as file:
    for line in file:
        clear_line = line.strip().replace(",", '').replace("'", '')
        if ':' in clear_line:
            word, emotion = clear_line.split(':', 1)
            word = word.strip()
            emotion = emotion.strip()
            if word in lemma_words:
                emotion_list.append(emotion)

print(emotion_list)
w = Counter(emotion_list)
print(w)

# Sentiment Analysis
def sentiment_analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['neg'] > score['pos']:
        print("Negative Sentiment")
    elif score['neg'] < score['pos']:
        print("Positive Sentiment")
    else:
        print("Neutral Sentiment")

sentiment_analyse(cleaned_text)

# Plotting
fig, ax1 = plt.subplots()
ax1.bar(w.keys(), w.values())
fig.autofmt_xdate()
plt.savefig('graph.png')
plt.show()
