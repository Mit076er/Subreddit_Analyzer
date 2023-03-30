import praw
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id="JnZeKfKqP62GP3CzptSLRg",
    client_secret="ykOlgXsGgI05joj4cMtyx4Ms7ZhIvg",
  ##add username and password 
    user_agent="Godzone_YT",
)

# Define a function to fetch Reddit posts and extract the relevant data
def fetch_posts(subreddit, num_posts):
    posts = []
    for post in reddit.subreddit(subreddit).new(limit=num_posts):
        posts.append({
            "title": post.title,
            "score": post.score,
            "id": post.id,
            "url": post.url,
            "num_comments": post.num_comments,
            "created_utc": post.created_utc,
            "selftext": post.selftext
        })
    return pd.DataFrame(posts)

# Instantiate the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Define function to plot the sentiment distribution
def plot_distribution(df):
    # Create a bar chart of the sentiment distribution
    sentiment_counts = df["sentiment"].value_counts()
    fig, ax = plt.subplots()
    ax.bar(sentiment_counts.index, sentiment_counts.values)
    ax.set_title("Distribution of Scores by Sentiment")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# Define function to plot the top words
def plot_top_words(df):
    # Combine all the comments into a single string
    comments = " ".join(df["selftext"].tolist())

    # Generate a word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(comments)

    # Display the word cloud
    st.image(wordcloud.to_array())

# Define function to perform sentiment analysis on a post
def plot_post_sentiment(post_text):
    # Perform sentiment analysis on the post
    scores = analyzer.polarity_scores(post_text)

    # Create a bar chart of the sentiment scores
    fig, ax = plt.subplots()
    ax.bar(scores.keys(), scores.values())
    ax.set_title("Sentiment Analysis")
    ax.set_ylabel("Score")
    st.pyplot(fig)

# Define a function to fetch trending topics in a subreddit
def fetch_trending_topics(subreddit):
    subreddit = reddit.subreddit(subreddit)
    return [topic.title for topic in subreddit.hot(limit=10)]

# Define function to plot the sentiment distribution as a pie chart
def plot_sentiment_pie(df):
    # Count the number of positive, negative, and neutral posts
    positive_count = (df["sentiment"] > 0).sum()
    negative_count = (df["sentiment"] < 0).sum()
    neutral_count = (df["sentiment"] == 0).sum()

    # Create a pie chart of the sentiment distribution
    fig, ax = plt.subplots()
    ax.pie([positive_count, negative_count, neutral_count], labels=["Positive", "Negative", "Neutral"], autopct="%1.1f%%")
    ax.set_title("Sentiment Distribution")
    st.pyplot(fig)

# Create a dictionary of menu items and their corresponding function calls
menu = {
"Distribution of Scores by Sentiment": plot_distribution,
"Top Words": plot_top_words,
"Post Sentiment Analysis": plot_post_sentiment,
"Trending Topics": fetch_trending_topics,
"Sentiment Pie Chart": plot_sentiment_pie
}

def main():
# Add a title to the app
    st.title("Reddit Post Sentiment Analysis")

    # Get user input for the subreddit and number of posts to fetch
    subreddit = st.text_input("Enter a subreddit:", "all")
    num_posts = st.number_input("Number of posts to fetch:", value=100, min_value=1, max_value=1000)

# Fetch the Reddit posts and perform sentiment analysis
    df = fetch_posts(subreddit, num_posts)
    df["sentiment"] = df["selftext"].apply(lambda x: analyzer.polarity_scores(x)["compound"])

# Create a vertical menu with the options.
    menu_choice = st.sidebar.radio("Select an option", tuple(menu.keys()))

    # Call the function corresponding to the selected option.
    if menu_choice == "Post Sentiment Analysis":
        st.write("Enter the text of the post:")
        post_text = st.text_area("", height=200)
        if st.button("Analyze Sentiment"):
            plot_post_sentiment(post_text)
    elif menu_choice == "Trending Topics":
        st.write(f"Trending topics in r/{subreddit}:")
        trending_topics = fetch_trending_topics(subreddit)
        for i, topic in enumerate(trending_topics):
            st.write(f"{i+1}. {topic}")
    else:
        menu[menu_choice](df)


if __name__ == "__main__":
    main()


