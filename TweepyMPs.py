"""
Politweets Python Project
Using Twitter API to scrape tweets then sentiment analysis with Textblob, finally present using Streamlit
This is the streamlit and analysis section
"""

from textblob import TextBlob
import nltk
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import re



politweets = pd.read_csv(r'politweets.csv')
politweets = politweets.drop(columns=['Unnamed: 0'])


# sentiment analysis functions
def polarity(tweet):
    """returns tweet polarity using textblob -1 - 1"""
    tweet = TextBlob(tweet)
    return tweet.sentiment.polarity


def subjectivity(tweet):
    """returns tweet subjectivity via textblob 0 - 1"""
    tweet = TextBlob(tweet)
    return tweet.sentiment.subjectivity


# extracting hashtags function
def hashtag_extract(tweet):
    """extract hashtag topics from tweets"""
    ht = re.findall(r"#(\w+)", tweet)
    return ht


# applying functions to dataframe to create: sentiment, polarity, hashtag columns
def create_additional_columns(politweets, polarity, subjectivity):
    """Creating additional columns from """
    politweets['polarity'] = politweets['tweet'].map(polarity).round(2)
    politweets['subjectivity'] = politweets['tweet'].map(subjectivity).round(2)
    politweets['hashtag'] = politweets['tweet'].map(hashtag_extract)
    politweets['hashtag'] = politweets['hashtag'].str.join(',')
    return politweets


def hashtags_list():
    """ creates a list of hastags from politweets column by mp"""
    hashtags = []
    for ht in politweets['hashtag']:
        if ht == '':
            pass
        else:
            hashtags.append(ht)
    return hashtags


def hashtags_df(hashtags):
    """create a dataframe from the hashtags selected"""
    freq_dist = nltk.FreqDist(hashtags)
    hashtags_data = pd.DataFrame({'Hashtag': list(freq_dist.keys()),
                                  'Count': list(freq_dist.values())})
    return hashtags_data


def plot_hashtags_data():
    """a plot to show top 10 hashtags """
    st.subheader('Top 10 Hashtags Bar Chart')
    fig = plt.figure(figsize=(16, 5))
    ax = sns.barplot(data=hashtags_count, x="Hashtag", y="Count")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    ax.set(ylabel='Count')
    return st.pyplot(fig)

def color_red(val):
    if val == 'Labour':
        color = '#DC241f'
    elif val == 'Conservative':
        color = '#0087DC'
    elif val == 'Liberal Democrat':
        color = '#FDBB30'
    elif val == 'Scottish National Party':
        color = '#FFFF00'
    elif val == 'Green Party':
        color = '#78b943'
    else:
        color = None
    return 'background-color: %s' % color


# create additional columns for sentiment analysis
politweets = create_additional_columns(politweets, polarity, subjectivity)
politweets.index += 1

# grouped politicans
politican_group = politweets.groupby('name').agg({'party': 'first',
                                                  'favourite_count': 'sum',
                                                  'retweet_count': 'sum',
                                                  'polarity': 'sum',
                                                  'subjectivity': 'sum',
                                                  })

# hastags list into dataframe
hashtags_data = hashtags_df(hashtags_list())
# selecting top 10 most frequent hashtags
hashtags_count = hashtags_data.nlargest(columns="Count", n=10)
hashtags_count.set_index('Hashtag')

data = hashtags_count
fig10 = px.bar(data, x=data.Hashtag, y=data.Count, color='Hashtag',
              labels={"index": "Hashtag",
                     "retweet_count": "Retweet Count"},
             title="Top 10 Hashtags Bar Chart")
fig10.update_xaxes(categoryorder="total descending")
fig10.update_layout(showlegend=False)
fig10.update_layout(autosize=False, width=1200,height=700,)

# grouped by party
party_groups = politweets[['party', 'favourite_count']].groupby('party').sum()
party_groups_2 = politweets[['party', 'retweet_count']].groupby('party').sum()

st.set_page_config(layout="wide")

st.title(' Politweets ')
st.text('A project looking at UK political tweet data. \n'
        'Data obtained from Twitter, using the API and Tweepy library \n'
        'simple NLP sentiment analysis using Textblob')

if st.checkbox('See Politweets Data'):
    st.subheader('Dataset of tweets from UK mps')
    st.text('A sample of 20 tweets from each mp that is represented on twitter')
    st.dataframe(politweets.style.applymap(color_red))


# Top 10 tweets favourite count
top_10_fav = politweets[['name', 'party','favourite_count']] \
    .sort_values(by='favourite_count', ascending=False) \
    .head(10) \
    .set_index("name")

# print(top_10_fav)
# dat = top_10_fav
# print(dat)
# fig, ax = plt.subplots()
# ax.bar(x=top_10_fav.index, height=dat)
# ax.set(ylabel='favourite_count')
# ax.set_title('Top 10 Favourite Tweets')
# labels = ax.get_xticklabels()
# plt.setp(labels, rotation=45, horizontalalignment='right')
# st.pyplot(fig)


data = top_10_fav
fig1 = px.bar(data, x=data.index, y=data.favourite_count, color=data.party,
             labels={"name": "MP Name",
                     "favourite_count": "Favourite Count",
                     "party":"Party"},
             color_discrete_map={"Labour": "#DC241f",
                                 "Conservative": "#0087DC",
                                 "Liberal Democrat": "#FDBB30",
                                 "Scottish National Party": "#FFFF00",
                                 "Green Party": "#78b943",
                                 "Independent": "#bf4080"},
             title="Top 10 Tweets Sorted by Favourite Count")
fig1.update_xaxes(categoryorder="total descending")

# top 10 retweets count
top_10_rt = politweets[['name','party','retweet_count']] \
    .sort_values(by='retweet_count', ascending=False) \
    .head(10) \
    .set_index('name')

data = top_10_rt
fig4 = px.bar(data, x=data.index, y=data.retweet_count, color=data.party,
             labels={"name": "MP Name",
                     "retweet_count": "Retweet Count",
                     "party":"Party"},
             color_discrete_map={"Labour": "#DC241f",
                                 "Conservative": "#0087DC",
                                 "Liberal Democrat": "#FDBB30",
                                 "Scottish National Party": "#FFFF00",
                                 "Green Party": "#78b943",
                                 "Independent": "#bf4080"},
             title="Top 10 Tweets sorted by Retweet Count")
fig4.update_xaxes(categoryorder="total descending")

# top 10 parties by Favourite Count Sum
top_10_party = party_groups.sort_values(by='favourite_count', ascending=False)

data = party_groups
fig3 = px.bar(data, x=data.index, y=data.favourite_count, color=data.index,
             labels={"favourite_count": "Favourite Count",
                     "party":"Party"},
             color_discrete_map={"Labour": "#DC241f",
                                 "Conservative": "#0087DC",
                                 "Liberal Democrat": "#FDBB30",
                                 "Scottish National Party": "#FFFF00",
                                 "Green Party": "#78b943",
                                 "Independent": "#bf4080"},
             title="Top 10 Parties Sorted by Favourite Count Sum")
fig3.update_xaxes(categoryorder="total descending")
fig3.update_layout(showlegend=False)

# top 10 retweets count sum
top_10_rts = party_groups_2.sort_values(by='retweet_count', ascending=False)

data = top_10_rts
fig6 = px.bar(data, x=data.index, y=data.retweet_count, color=data.index,
             labels={"name": "MP Name",
                     "retweet_count": "Retweet Count",
                     "party":"Party"},
             color_discrete_map={"Labour": "#DC241f",
                                 "Conservative": "#0087DC",
                                 "Liberal Democrat": "#FDBB30",
                                 "Scottish National Party": "#FFFF00",
                                 "Green Party": "#78b943",
                                 "Independent": "#bf4080"},
             title="Top 10 Parties Sorted by Retweet Count Total Sum")
fig6.update_xaxes(categoryorder="total descending")
fig6.update_layout(showlegend=False)

# top 10 mps sorted by favourite count sum
top_10_fcs = politican_group[['party', 'favourite_count']] \
    .sort_values(by='favourite_count', ascending=False) \
    .head(10)

data = top_10_fcs
fig2 = px.bar(data, x=data.index, y=data.favourite_count, color=data.party,
             labels={"name": "MP Name",
                     "favourite_count": "Favourite Count",
                     "party":"Party"},
             color_discrete_map={"Labour": "#DC241f",
                                 "Conservative": "#0087DC",
                                 "Liberal Democrat": "#FDBB30",
                                 "Scottish National Party": "#FFFF00",
                                 "Green Party": "#78b943",
                                 "Independent": "#bf4080"},
             title="Top 10 MPs Sorted by Favourite Count Sum")
fig2.update_xaxes(categoryorder="total descending")

# top 10 mps sorted by retweet count sum
top_10_rtcs = politican_group[['party', 'retweet_count']] \
    .sort_values(by='retweet_count', ascending=False) \
    .head(10)

data = top_10_rtcs
fig5 = px.bar(data, x=data.index, y=data.retweet_count, color=data.party,
             labels={"name": "MP Name",
                     "retweet_count": "Retweet Count",
                     "party":"Party"},
             color_discrete_map={"Labour": "#DC241f",
                                 "Conservative": "#0087DC",
                                 "Liberal Democrat": "#FDBB30",
                                 "Scottish National Party": "#FFFF00",
                                 "Green Party": "#78b943",
                                 "Independent": "#bf4080"},
             title="Top 10 MPs sorted by Retweet Count Total Sum")
fig5.update_xaxes(categoryorder="total descending")


# top 10 mps sorted by polarity sum
party_pol = politican_group[['party', 'polarity']]\
            .sort_values(by='polarity', ascending=False)\
            .head(10)

data = party_pol
fig7 = px.bar(data, x=data.index, y=data.polarity, color=data.party,
             labels={"name": "MP Name",
                     "retweet_count": "Retweet Count",
                     "party":"Party"},
             color_discrete_map={"Labour": "#DC241f",
                                 "Conservative": "#0087DC",
                                 "Liberal Democrat": "#FDBB30",
                                 "Scottish National Party": "#FFFF00",
                                 "Green Party": "#78b943",
                                 "Independent": "#bf4080"},
             title="Top 10 MPs Sorted by Polarity Sum")
fig7.update_xaxes(categoryorder="total descending")


# top 10 mps sorted by subjectivity sum
party_subj = politican_group[['party', 'subjectivity']]\
                            .sort_values(by='subjectivity', ascending=False)\
                            .head(10)

data = party_subj
fig8 = px.bar(data, x=data.index, y=data.subjectivity, color=data.party,
             labels={"name": "MP Name",
                     "retweet_count": "Retweet Count",
                     "party":"Party"},
             color_discrete_map={"Labour": "#DC241f",
                                 "Conservative": "#0087DC",
                                 "Liberal Democrat": "#FDBB30",
                                 "Scottish National Party": "#FFFF00",
                                 "Green Party": "#78b943",
                                 "Independent": "#bf4080"},
             title="Top 10 MPs Sorted by Subjectivity Sum")
fig8.update_xaxes(categoryorder="total descending")

# top 10 parties by polarity sum
party_groups = politweets[['party', 'polarity']].groupby('party').sum()
# parties by tweet polarity
party_polsum = party_groups.sort_values(by='polarity', ascending=False).head(10)

data = party_polsum
fig9 = px.bar(data, x=data.index, y=data.polarity, color=data.index,
             labels={"name": "MP Name",
                     "retweet_count": "Retweet Count",
                     "party":"Party"},
             color_discrete_map={"Labour": "#DC241f",
                                 "Conservative": "#0087DC",
                                 "Liberal Democrat": "#FDBB30",
                                 "Scottish National Party": "#FFFF00",
                                 "Green Party": "#78b943",
                                 "Independent": "#bf4080"},
             title="Top 10 Parties by Tweet Polarity Sum")
fig9.update_xaxes(categoryorder="total descending")
fig9.update_layout(showlegend=False)

#Sidebar for data selection


add_selectbox = st.sidebar.selectbox(
    "Select an insight",
    ("Top 10 Favourites", "Top 10 Retweets", "Top 10 Hashtags", "Sentiment Analysis")
)

if add_selectbox == 'Top 10 Favourites':
    favourites = st.beta_container()
    with favourites:
        st.subheader('Favourite Tweets Analysis')
        st.text('Some analysis on the favourite tweet data and groupings')
        col1, col2, = st.beta_columns([1, 1.25])
        col1.subheader('Top 10 Tweets Sorted by Favourite Count')
        col1.dataframe(top_10_fav.reset_index(drop=False).style.applymap(color_red))
        col2.plotly_chart(fig1)
        col1.subheader('Top 10 MPs sorted by Favourite Count Sum')
        col1.text('The total of all favourites across all tweets, per MP')
        col1.write(top_10_fcs.reset_index(drop=False).style.applymap(color_red))
        col2.plotly_chart(fig2)
        col1.subheader('Top 10 Parties Sorted by Favourite Count Sum')
        col1.text('The total of all favourites, of all mps within a party,\n'
                  'grouped by party')
        col1.write(top_10_party)
        col2.plotly_chart(fig3)

elif add_selectbox == 'Top 10 Retweets':
    retweets = st.beta_container()
    with retweets:
        col1, col2, = st.beta_columns([1, 1.25])
        col1.subheader('Retweets Analysis')
        col1.subheader('Top 10 Tweets Sorted by Retweet Count')
        col2.plotly_chart(fig4)
        col1.write(top_10_rt.reset_index(drop=False).style.applymap(color_red))
        col1.subheader('Top 10 MPs Sorted by Retweet Count Total Sum')
        col2.plotly_chart(fig5)
        col1.write(top_10_rtcs.reset_index(drop=False).style.applymap(color_red))
        col2.plotly_chart(fig6)
        col1.subheader('Top 10 Parties Sorted by Retweet Count Total Sum')
        col1.write(top_10_rts)

elif add_selectbox == 'Top 10 Hashtags':
    hashtags = st.beta_container()
    with hashtags:
        col1, col2, = st.beta_columns([1, 1.25])
        col1.subheader('Hashtags Analysis')
        col1.subheader('Top 10 Hashtags used by MPs in Tweets')
        col1.write(hashtags_count.set_index('Hashtag'))
        st.plotly_chart(fig10)

elif add_selectbox == 'Sentiment Analysis':
    col1, col2, = st.beta_columns([1, 1.25])
    if col1.checkbox('Sentiment Definitions'):
        col1.subheader('Polarity')
        col1.text('The polarity score is a float within the range [-1.0, 1.0]. \n'
                  'Negative words correspond to negative polarity values. \n'
                  'Positive words correspond to positive polartiy values. \n'
                  'The more negative the closer to -1 and the opposite for positive.')
        col1.subheader('Subjectivity')
        col1.text("The subjectivity is a float within the range [0.0, 1.0] \n"
                  "where 0.0 is very objective and 1.0 is very subjective.")
    col1.subheader('Sentiment Analysis')
    col1.subheader('Top 10 MPs Sorted by Polarity Sum')
    col1.write(party_pol.reset_index(drop=False).style.applymap(color_red))
    col2.plotly_chart(fig7)
    col1.subheader('Top 10 MPs Sorted by Subjectivity Sum')
    col1.write(party_subj.reset_index(drop=False).style.applymap(color_red))
    col2.plotly_chart(fig8)
    col1.subheader('Top 10 Parties by Tweet Polarity Sum')
    col1.write(party_polsum)
    col2.plotly_chart(fig9)

else:
    pass

