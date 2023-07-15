import re
import string

import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from wordcloud import WordCloud


def show_used_words():
    """
    Generate word clouds to visualize the most commonly used words in the email content and subjects.

    The function performs data cleaning, including removing stop words, lemmatizing words, and removing punctuation
    and non-alphabetic characters. It then generates word clouds based on the cleaned content and subjects.

    """

    # Function for cleaning text data
    def text_cleaning(txt):
        stop_words = set(stopwords.words('english'))
        stop_words.update(
            ('from', 'to', 'cc', 'http', 're', 'www', 'com', 'subject', 'sent', 'email', 'u', 'ok',
             'thanks', 'please', 'ect', 'dt', 'pm', 'enron'))
        exclude = set(string.punctuation)
        lemma = WordNetLemmatizer()
        txt = txt.rstrip()
        txt = re.sub(r'[^a-zA-Z]', ' ', txt)
        stop_free = " ".join(
            [i for i in txt.lower().split() if ((i not in stop_words) and (not i.isdigit()) and len(i) > 3)])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        return " ".join(lemma.lemmatize(word) for word in punc_free.split())

    filter_df[['Content', 'Subject']] = filter_df[['Content', 'Subject']].fillna('')
    text_clean = []
    for text in filter_df['Content']:
        text_clean.append(text_cleaning(text))
    subject_clean = []
    for sub_text in filter_df['Subject']:
        subject_clean.append(text_cleaning(sub_text))

    filter_df['Clean-Content'] = text_clean
    filter_df['Clean-Subject'] = subject_clean

    clean_content_text = ' '.join(text_clean)
    wordcloud_content = WordCloud(width=800, height=400, background_color='white', max_words=200).generate(
        clean_content_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_content, interpolation='bilinear')
    plt.axis('off')
    plt.title('Common Mail Words', fontsize=20, fontweight='bold')
    st.pyplot(plt)

    # Word cloud for Clean-Subject
    clean_subject_text = ' '.join(subject_clean)
    wordcloud_subject = WordCloud(width=800, height=400, background_color='white', max_words=200).generate(
        clean_subject_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_subject, interpolation='bilinear')
    plt.axis('off')
    plt.title('Common Subject Words', fontsize=20, fontweight='bold')
    st.pyplot(plt)


st.set_page_config(page_title="Enron Emails Dashboard", page_icon="💌", layout='wide')


@st.cache_data
def get_data():
    return pd.read_csv('modified_emails.csv')


df = get_data()
part_df = df.sample(n=2000, random_state=42).reset_index()
part_df[['Content', 'Subject']] = part_df[['Content', 'Subject']].fillna('')

# Adding Some filters on the sidebar for the data
st.sidebar.header("Filter Here:")
reply_options = ["All", True, False]
is_reply = st.sidebar.selectbox("Reply Email:", reply_options)

forward_options = ["All", True, False]
is_forward = st.sidebar.selectbox("Forward Email:", forward_options)

month_dict = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
              "September": 9, "October": 10, "November": 11, "December": 12
              }

day_dict = {"Sunday": 1, "Monday": 2, "Tuesday": 3, "Wednesday": 4, "Thursday": 5, "Friday": 6, "Saturday": 7}

months = df["Month"].unique()
months_sorted = sorted(months, key=lambda x: month_dict.get(x))

days = df["Day"].unique()
days_sorted = sorted(days, key=lambda x: day_dict.get(x))

selected_month = st.sidebar.selectbox("Select Month:", ["All"] + list(months_sorted))
selected_day = st.sidebar.selectbox("Select Day:", ["All"] + list(days_sorted))

senders = df['From'].value_counts().nlargest(10).index.tolist()
selected_sender = st.sidebar.selectbox("Select Sender Mail:", ["All"] + senders)

filter_df = part_df

if selected_month != "All":
    filter_df = filter_df[filter_df["Month"] == selected_month]

if selected_day != "All":
    filter_df = filter_df[filter_df["Day"] == selected_day]

if is_reply != "All":
    filter_df = filter_df[filter_df["Is-Reply"] == is_reply]

if is_forward != "All":
    filter_df = filter_df[filter_df["Is-Forwarded"] == is_forward]

if selected_sender != "All":
    filter_df = filter_df[filter_df["From"] == selected_sender]

st.title(":bar_chart: Words Data")
st.markdown("##")

# Adding Some KPI's
total_emails = filter_df.shape[0]
if total_emails != 0:
    total_senders = filter_df['From'].nunique()
    most_emails = filter_df['From'].value_counts().idxmax()
    emails_amount = filter_df['From'].value_counts().max()

    l_col, m_col, r_col = st.columns(3)
    # Will have 3 KPIs - Total Emails, Total Distinct Senders, Most Prolific Emailer
    with l_col:
        st.subheader("Total Emails: (Filtered Randomly For Speed)")
        st.subheader(total_emails)
    with m_col:
        st.subheader("Total Distinct Senders: ")
        st.subheader(total_senders)
    with r_col:
        st.subheader("Most Prolific Emailer: ")
        st.subheader(f"{most_emails}, {emails_amount}")

    st.markdown("---")
    # Plotting
    show_used_words()
else:
    st.warning("Data Set Is Empty After Filtering")
