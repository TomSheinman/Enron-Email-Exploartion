import ast
import networkx as nx
import numpy as np
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt


def network_plot(graph_to_plot):
    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(graph_to_plot, k=0.5)
    closeness = nx.closeness_centrality(graph_to_plot)
    # Compute edge widths based on 'count' attribute
    edge_widths = [d['count'] for (_, _, d) in graph_to_plot.edges(data=True)]
    max_edge = max(edge_widths)
    edge_widths_normalized = np.power(edge_widths, 0.5) / np.power(max_edge, 0.5) * 4

    nx.draw_networkx_nodes(graph_to_plot, pos, node_size=25, node_color=list(closeness.values()))
    nx.draw_networkx_edges(graph_to_plot, pos, edge_color='black', alpha=0.3, width=edge_widths_normalized)
    nx.draw_networkx_labels(graph_to_plot, pos, font_size=10, font_color='black')

    plt.title("Connections Between Top 100 Most Connected Workers", fontsize=20, fontweight='bold', alpha=1)
    st.pyplot(plt)


def random_network_plot():
    # Select a random subset of 1 percent nodes from sub_df_for_graph
    random_subset = sub_df_for_graph.sample(frac=0.01, random_state=0)
    random_nodes = np.unique(random_subset[['From', 'To']].values)
    sub_df_random = sub_df_for_graph[
        sub_df_for_graph['From'].isin(random_nodes) & sub_df_for_graph['To'].isin(random_nodes)]

    g2 = nx.from_pandas_edgelist(sub_df_random, source='From', target='To', edge_attr='count')
    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(g2, k=0.2)

    # Compute edge widths based on 'count' attribute
    edge_widths = [d['count'] for (_, _, d) in g2.edges(data=True)]
    max_edge = max(edge_widths)
    edge_widths_normalized = np.power(edge_widths, 0.5) / np.power(max_edge, 0.5) * 4

    nx.draw_networkx_nodes(g2, pos, node_size=25, node_color='red', alpha=0.3)
    nx.draw_networkx_edges(g2, pos, edge_color='black', alpha=0.3, width=edge_widths_normalized)
    nx.draw_networkx_labels(g2, pos, font_size=10, font_color='black')

    plt.title("Connections between a random subset of workers", fontsize=20, fontweight='bold')
    st.pyplot(plt)


def in_out_degrees(graph_to_plot):
    in_degree_dict = dict(graph_to_plot.in_degree(weight='count'))
    out_degree_dict = dict(graph_to_plot.out_degree(weight='count'))
    # Extract the values from the dictionaries
    in_degree_values = list(in_degree_dict.values())
    out_degree_values = list(out_degree_dict.values())

    # Create the histogram plot
    plt.figure(figsize=(10, 6))
    plt.hist(in_degree_values, bins=30, density=True, color='blue', alpha=0.5, label='In-degree')
    plt.hist(out_degree_values, bins=30, density=True, color='orange', alpha=0.5, label='Out-degree')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.title('Distribution of In-degree and Out-degree')
    plt.legend()
    plt.show()


st.set_page_config(page_title="Enron Emails Dashboard", page_icon="💌", layout='wide')

@st.cache_data
def get_data():
    return pd.read_csv('modified_emails.csv')


df = get_data()
st.title(":bar_chart: Graph Data")
st.markdown("##")


def prepare_graph():
    df['To'] = df['To'].apply(ast.literal_eval)
    sub_df = df.loc[df['To'].map(len) == 1, ['From', 'To', 'Content']].fillna(0).copy()
    sub_df['To'] = sub_df['To'].map(lambda x: x[0])
    sub_df = sub_df.groupby(['From', 'To']).count().reset_index()
    sub_df.rename(columns={'Content': 'count'}, inplace=True)
    return sub_df.sort_values('count', ascending=False).reset_index()


sub_df_for_graph = prepare_graph()
graph = nx.from_pandas_edgelist(sub_df_for_graph.head(100), source='From', target='To',
                                edge_attr='count')
graph2 = nx.from_pandas_edgelist(sub_df_for_graph.head(100), source='From', target='To',
                                edge_attr='count', create_using=nx.DiGraph)

# Showing Some KPI's
total_nodes = graph.number_of_nodes()
total_edges = graph.number_of_edges()
most_connected_a = sub_df_for_graph.loc[0, 'From']
most_connected_b = sub_df_for_graph.loc[0, 'To']
connection_size = sub_df_for_graph.loc[0, 'count']
max_count = sub_df_for_graph['count'].max()

l_col, m_col, r_col = st.columns(3)
# Will have 3 KPIs - Total Nodes, Total Edges, Most Connected Workers
with l_col:
    st.subheader("Total Nodes: ")
    st.subheader(total_nodes)
with m_col:
    st.subheader("Total Edges: ")
    st.subheader(total_edges)
with r_col:
    st.subheader("Most Connected Workers: ")
    st.subheader(f"{most_connected_a}, {most_connected_b}, {connection_size}")

st.markdown("---")

# Plotting
network_plot(graph2)
random_network_plot()
in_out_degrees(graph2)
