import praw
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import base64
from streamlit import components
from PIL import Image




# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id="JnZeKfKqP62GP3CzptSLRg",
    client_secret="ykOlgXsGgI05joj4cMtyx4Ms7ZhIvg",
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

def social_links():
    # Define the social links as a dictionary with keys as the name of the social media platform and values as the URLs
    social_media = {
        "Twitter": "https://twitter.com/MitPandya4",
        "LinkedIn": "https://www.linkedin.com/in/mit-pandya-15930621a/",
        "Github": "https://github.com/Mit076er"
    }

  # Define the logos for each social media platform as a dictionary with keys as the names of the social media platform and values as the URLs of the logos
    social_media_logos = {
        "Twitter": "https://upload.wikimedia.org/wikipedia/sco/9/9f/Twitter_bird_logo_2012.svg",
        "LinkedIn": "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png",
        "Github":   "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg"
    }

    social_links_html = ""
    for name, url in social_media.items():
        social_links_html += f'<a href="{url}" target="_blank" rel="noopener noreferrer"><img src="{social_media_logos[name]}" alt="{name}" width="50" height="50"></a>'



    st.markdown(social_links_html, unsafe_allow_html=True)
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

    fig, ax = plt.subplots()
    ax.pie([positive_count, negative_count, neutral_count], labels=["Positive", "Negative", "Neutral"], autopct="%1.1f%%")
    ax.set_title("Sentiment Distribution")
    st.pyplot(fig)

def download_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="reddit_posts.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

def home():
    st.title("Mit Pandya's Subreddit Analyzer")
    st.write("Welcome to the Mit Pandya's Subreddit Analyzer. This app is designed to analyze the sentiment of subreddits posts in the Reddit community. Please select an option from the menu on the left to get started. Use the features in navigation menu to explore the subreddit data.To Download the csv dataset file navigate to download csv file option to access the file. To Use the sentiment analyzer enter a valid subreddit name and the number of posts to fetch from range 1-1000 as the range has been set is till max 1000 to fetch.")
    image = Image.open("reddit.png")
    st.image(image, caption="", use_column_width=True)


def about_me():
    st.title("About Me")
    st.write("This app was created by Mit Yogeshkumar Pandya under the guidance of Prof. Nita Jadav, with the goal of analyzing the sentiment of posts in the Reddit community. I hope that this app is helpful and insightful for users who are interested in understanding the sentiment of Reddit posts.")
    st.write("If you have any questions or feedback, feel free to contact me at mitpanh@gmail.com")
    st.write("Thank you for using my app!!!")
    st.write("Follow me on social media:")
    social_links()
      # Add an image to the page
    image = Image.open("aws mit.jpg")
    st.image(image, caption="Hey its me Mit Pandya", use_column_width=True)


menu = {
    "Home": home,
    "Distribution of Scores by Sentiment": plot_distribution,
    "Top Words": plot_top_words,
    "Post Sentiment Analysis": plot_post_sentiment,
    "Trending Topics": fetch_trending_topics,
    "Sentiment Pie Chart": plot_sentiment_pie,
    "Download Data": download_csv,
    "About Me": about_me
}



def main():
    # Add a title to the app


    # Create a vertical menu with the options.
    menu_choice = st.sidebar.radio("Select an option", tuple(menu.keys()))
     
    if menu_choice == "Home":
        home()

    # Call the function corresponding to the selected option.
    elif menu_choice == "Post Sentiment Analysis":
        subreddit = st.text_input("Enter a subreddit:", "all")
        num_posts = st.number_input("Number of posts to fetch:", value=100, min_value=1, max_value=1000)
        st.write("Enter the text of the post:")
        post_text = st.text_area("", height=200)
        if st.button("Analyze Sentiment"):
            plot_post_sentiment(post_text)
    elif menu_choice == "Trending Topics":
        subreddit = st.text_input("Enter a subreddit:", "all")
        st.write(f"Trending topics in r/{subreddit}:")
        trending_topics = fetch_trending_topics(subreddit)
        for i, topic in enumerate(trending_topics):
            st.write(f"{i+1}. {topic}")
    elif menu_choice == "About Me":
        about_me()
   
    else:
        subreddit = st.text_input("Enter a subreddit:", "all")
        num_posts = st.number_input("Number of posts to fetch:", value=100, min_value=1, max_value=1000)
        df = fetch_posts(subreddit, num_posts)
        df["sentiment"] = df["selftext"].apply(lambda x: analyzer.polarity_scores(x)["compound"])
        menu[menu_choice](df)


if __name__ == "__main__":
    main()
