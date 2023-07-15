import numpy as np
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Enron Emails Dashboard", page_icon="💌", layout='wide')

# Read An already grouped data set based on Reply count emails sent amount and average word count
grouped_df = pd.read_csv('grouped_emails.csv')
st.title(":bar_chart: Additional Summarizing Plots")
st.markdown("##")

# Calculate the difference between number of emails sent and number of replies
grouped_df['Email_Reply_Ratio'] = np.where(grouped_df['Reply_Count'] == 0, grouped_df['Emails_Sent'],
                                           grouped_df['Emails_Sent'] / grouped_df['Reply_Count'])
# Sort the DataFrame by the difference in descending order
grouped_df = grouped_df.sort_values('Email_Reply_Ratio', ascending=False)
# Create a bar plot of the difference between emails sent and replies
fig, ax = plt.subplots(figsize=(10, 9))
sns.barplot(data=grouped_df.head(30), x='From', y='Email_Reply_Ratio', palette=sns.color_palette("magma", 30),
            ax=ax)
ax.set_xlabel('Sender', fontweight='bold', fontsize=18)
ax.set_ylabel('Email/Reply Ratio', fontweight='bold', fontsize=18)
ax.set_title('Possible Spammers: Email to Reply Ratio (Top 30)', fontsize=18)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontweight='bold', fontsize=12)
plt.tight_layout()
st.pyplot(plt)

# Sort the DataFrame by number of emails sent in descending order
grouped_df = grouped_df.sort_values('Emails_Sent', ascending=False)
# Scatter plot of number of emails sent vs word count
plt.figure(figsize=(10, 6))
sns.scatterplot(data=grouped_df.head(30), x='Emails_Sent', y='Average_Word_Count', hue='From', palette='Paired')
plt.xlabel('Number of Emails Sent')
plt.ylabel('Average Word Count')
plt.title('Number of Emails Sent vs Word Count (Top 30 Senders)', fontsize=18)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)  # Place legend outside the plot
st.pyplot(plt)

# Sort the DataFrame by number of replies in descending order
grouped_df = grouped_df.sort_values('Reply_Count', ascending=False)
# Scatter plot of number of replies vs word count
plt.figure(figsize=(10, 6))
sns.scatterplot(data=grouped_df.head(30), x='Reply_Count', y='Average_Word_Count', hue='From', palette='Paired')
plt.xlabel('Number of Replies')
plt.ylabel('Word Count')
plt.title('Number of Replies vs Word Count (Top 30 Repliers)', fontsize=18)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)  # Place legend outside the plot
plt.tight_layout()
st.pyplot(plt)
