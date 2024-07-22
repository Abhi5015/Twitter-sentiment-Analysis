import string
from collections import Counter
import tweepy
import matplotlib.pyplot as plt

# Replace with your actual Bearer Token
bearer_token = 'AAAAAAAAAAAAAAAAAAAAALbRuwEAAAAAAWq%2FBSbVpPA2GZtt9d3l0kzDxpA%3DbnJlw6ta4SUqkeXTyXxLyfrCEJr2WiNBukNuugUudxbWk76uVo'

# Set up the Twitter API client
client = tweepy.Client(bearer_token=bearer_token)


def get_tweets(query, start_date, end_date, max_results):
    try:
        response = client.search_recent_tweets(query=query,
                                               start_time=start_date,
                                               end_time=end_date,
                                               max_results=max_results,
                                               tweet_fields=['text'])

        # Print the raw response for debugging
        print("API Response:", response.json())  # Use response.json() to view the actual response content

        if response.data:
            tweets = response.data
            text_tweets = [[tweet.text] for tweet in tweets]
            return text_tweets
        else:
            print("No tweets found.")
            return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


# Get tweets
text_tweets = get_tweets('Coronavirus', '2020-01-01T00:00:00Z', '2021-04-01T00:00:00Z', 1000)

# Reading and processing tweets
text = ""
length = len(text_tweets)

for i in range(length):
    text = text_tweets[i][0] + " " + text

# Converting to lowercase
lower_case = text.lower()

# Removing punctuations
cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

# Splitting text into words
tokenized_words = cleaned_text.split()

# Define stop words
stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

# Removing stop words
final_words = [word for word in tokenized_words if word not in stop_words]

# Print final words for debugging
print("Final Words:", final_words)

# Get emotions from file
emotion_list = []
with open('emotions.txt', 'r') as file:
    for line in file:
        clear_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
        word, emotion = clear_line.split(':')
        if word in final_words:
            emotion_list.append(emotion)

# Print emotion list for debugging
print("Emotion List:", emotion_list)

# Count emotions and plot results
w = Counter(emotion_list)
print(w)

fig, ax1 = plt.subplots()
ax1.bar(w.keys(), w.values())
fig.autofmt_xdate()
plt.savefig('graph.png')
plt.show()
