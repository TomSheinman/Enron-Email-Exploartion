import ast
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
import seaborn as sns


def time_dist(col_to_plot):
    """
       Generate a bar chart showing the distribution of email sending times during the day.
    """

    # Create a new DataFrame for visualization
    time_df = filter_df.groupby(filter_df['Hour']).size().reset_index(name='count')
    time_df.columns = ['hour', 'count']
    # Assign colors based on rank
    ranks = time_df['count'].rank(method='min', ascending=False)
    c_map = sns.color_palette("mako", n_colors=len(time_df))
    colors = [c_map[int(rank) - 1] for rank in ranks]

    fig, ax = plt.subplots()
    sns.barplot(data=time_df, x='hour', y='count', palette=colors, ax=ax)
    ax.set_xlabel('Hour of the day', fontweight='bold', fontsize=12)
    ax.set_ylabel('Number of emails', fontweight='bold', fontsize=12)
    ax.set_title('Distribution of Email Sending Times')
    col_to_plot.pyplot(fig)


def emails_senders(col_to_plot):
    """
    Create a bar chart displaying the top 15 email senders and the number of emails they have sent.
    """

    grouped_df = filter_df.groupby('From').size().reset_index(name='Emails_Sent')
    grouped_df = grouped_df.sort_values('Emails_Sent', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 9))
    color_palette = sns.color_palette("crest", 20)
    sns.barplot(data=grouped_df.head(20), x='From', y='Emails_Sent', palette=color_palette, ax=ax)
    ax.set_xlabel('Sender', fontweight='bold', fontsize=14)
    ax.set_ylabel('Number of Emails Sent', fontweight='bold', fontsize=14)
    ax.set_title('Most Emails Per User (Top 20 Senders)', fontsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontweight='bold', fontsize=12)
    plt.tight_layout()
    col_to_plot.pyplot(fig)


def outsource_senders(col_to_plot):
    """
    Generate a bar chart illustrating the top 20 outsource email senders and the number of emails they have sent.
    """

    grouped_df = filter_df.groupby('From').size().reset_index(name='Emails_Sent')
    outsources = grouped_df[~grouped_df['From'].str.contains('enron', case=False)]
    outsources = outsources.sort_values('Emails_Sent', ascending=False)

    # Bar plot of number of emails sent by outsource senders
    fig, ax = plt.subplots(figsize=(10, 9))
    color_palette = sns.color_palette("rocket", 20)
    sns.barplot(data=outsources.head(20), x='From', y='Emails_Sent', palette=color_palette, ax=ax)
    ax.set_xlabel('Sender', fontweight='bold', fontsize=14)
    ax.set_ylabel('Number of Emails Sent', fontweight='bold', fontsize=14)
    ax.set_title('Biggest Outsource Senders (Top 20)', fontsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontweight='bold', fontsize=12)
    plt.tight_layout()
    col_to_plot.pyplot(fig)


def day_dist(col_to_plot):
    """
    Generate a pie chart showcasing the distribution of email sending days.
    """

    day_df = filter_df.groupby(filter_df['Day']).size().reset_index(name='count')

    # Combine Friday and Saturday into a single slice
    weekend_count = day_df.loc[day_df['Day'].isin(['Saturday', 'Sunday']), 'count'].sum()
    day_df = day_df.loc[~day_df['Day'].isin(['Saturday', 'Sunday'])]

    # Create a new DataFrame for the weekend data
    weekend_df = pd.DataFrame({'Day': ['Weekend'], 'count': [weekend_count]})

    # Concatenate the original DataFrame with the weekend DataFrame
    day_df = pd.concat([day_df, weekend_df], ignore_index=True)

    # Set the explode parameter to make the "Weekend" slice stand out
    explode = [0.0] * (len(day_df) - 1) + [0.2]

    # Plot the distribution of email sending days using a pie chart
    fig, ax = plt.subplots()
    ax.pie(day_df['count'], labels=day_df['Day'], autopct='%1.1f%%', colors=sns.color_palette('Set2'),
           explode=explode, textprops={'fontsize': 12})
    ax.set_title('Distribution of Email Sending Days', fontsize=12)
    col_to_plot.pyplot(fig)


def biggest_repliers(col_to_plot):
    """
    Generate a bar chart showing the top 15 email repliers and the number of emails they have sent.
    """

    grouped_df = filter_df.groupby('Is-Reply').size().reset_index(name='Reply_Count')
    grouped_df = grouped_df.sort_values('Reply_Count', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 9))
    sns.barplot(data=grouped_df.head(15), x='From', y='Emails_Sent', palette=sns.color_palette("crest", 15), ax=ax)
    ax.set_xlabel('Replier Email', fontweight='bold', fontsize=18)
    ax.set_ylabel('Number of Emails Sent', fontweight='bold', fontsize=18)
    ax.set_title('Biggest Email Repliers (Top 15 Senders)', fontsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontweight='bold', fontsize=12)
    plt.tight_layout()
    col_to_plot.pyplot(fig)


def find_connected_users(col_to_plot):
    filter_df['To'] = filter_df['To'].apply(ast.literal_eval)
    explode_df = filter_df.explode('To', ignore_index=True)
    helper_df = explode_df.groupby('To').size().reset_index(name='count')
    helper_df = helper_df.sort_values('count', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 9))
    num_to_show = min(15, helper_df.shape[0])
    sns.barplot(data=helper_df.head(num_to_show), x='To', y='count', palette=sns.color_palette("flare", num_to_show),
                ax=ax)
    ax.set_xlabel('Email Recipient', fontweight='bold', fontsize=18)
    ax.set_ylabel('Number of Emails Sent', fontweight='bold', fontsize=18)
    ax.set_title('Most Sent Emails To', fontsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontweight='bold', fontsize=12)
    plt.tight_layout()
    col_to_plot.pyplot(fig)


st.set_page_config(page_title="Enron Emails Dashboard", page_icon="💌", layout='wide')


@st.cache_data
def get_data():
    return pd.read_csv('modified_emails.csv')


df = get_data()
# Some data filtering...
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

filter_df = df
if selected_sender != "All":
    filter_df = filter_df[filter_df["From"] == selected_sender]

if selected_month != "All":
    filter_df = filter_df[filter_df["Month"] == selected_month]

if selected_day != "All":
    filter_df = filter_df[filter_df["Day"] == selected_day]

if is_reply != "All":
    filter_df = filter_df[filter_df["Is-Reply"] == is_reply]

if is_forward != "All":
    filter_df = filter_df[filter_df["Is-Forwarded"] == is_forward]

# Adding Some KPI's
st.title(":bar_chart: Emails Data")
st.markdown("##")
total_emails = filter_df.shape[0]
if total_emails != 0:
    total_senders = filter_df['From'].nunique()
    most_emails = filter_df['From'].value_counts().idxmax()
    emails_amount = filter_df['From'].value_counts().max()

    l_col, m_col, r_col = st.columns(3)
    # Will have 3 KPIs - Total Emails, Total Distinct Senders, Most Prolific Emailer
    with l_col:
        st.subheader("Total Emails: ")
        st.subheader(total_emails)
    with m_col:
        st.subheader("Total Distinct Senders: ")
        st.subheader(total_senders)
    with r_col:
        st.subheader("Most Prolific Emailer: ")
        st.subheader(f"{most_emails}, {emails_amount}")

    st.markdown("---")
    # Plotting
    l_col, r_col = st.columns(2)
    time_dist(l_col)
    if selected_day == "All":
        day_dist(l_col)
    if selected_sender == "All":
        emails_senders(r_col)
        outsource_senders(r_col)
    else:
        find_connected_users(r_col)
else:
    st.warning("Data Set Is Empty After Filtering")
