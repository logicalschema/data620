import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


senator_info_url = 'https://raw.githubusercontent.com/logicalschema/data620/main/Project%201/data/Final_senators_social_media.csv'
twitter_relationships_url = 'https://raw.githubusercontent.com/logicalschema/data620/main/Project%201/data/Final_senator_twitter_relationships.csv'

# colnames = ['State', 'Status', 'Name', 'NameLink', 'Party', 'Twitter', 'TwitterLink', 'Instagram', 'InstagramLink', 'Facebook', 'FacebookLink']
data = pd.read_csv(senator_info_url, index_col=0)

# Remove the leading @ character
data['Twitter'] = data['Twitter'].str.strip()
data['Twitter'] = data['Twitter'].str.replace('@','')


# Construct dictionaries to lookup Twitterids. I will use the dataframe index for an index
twitterLookup = {}
twitterReverseLookup = {}

for index, row in data.iterrows():
	twitterLookup[str(row['Twitter'])] = index
	twitterReverseLookup[index] = str(row['Twitter'])


# Constructs the relationships which will be used for Graph edges
# Empty list of relationships
# Dataframe ('Twitter', 'Follower') means User: Twitter is followed by Follower
twitter_relationships = pd.read_csv(twitter_relationships_url, header=None)
twitter_relationships.columns = ['User', 'Follower']


# Create a graph
G = nx.Graph()

# Construct the nodes with some attributes from the dataframe
for index, row in data.iterrows():

	G.add_node(index, 
		State = str(row['State']),
		Name = str(row['Name']),
		Party = str(row['Party']),
		Twitter = str(row['Twitter']),
		)



# Construct the edges using the relationships dataframe
for index, row in twitter_relationships.iterrows():
	User = twitterLookup[row['User']]
	Follower = twitterLookup[row['Follower']]
	G.add_edge(  User , Follower )



# Sorting nodes into Republican, Democrat, and Independent. Only the index is stored.
republicans = data.index[data['Party'] == 'R'].tolist()
democrats = data.index[data['Party'] == 'D'].tolist()
independents = data.index[data['Party'] == 'I'].tolist()
print("Indices for Republicans" + str(republicans))
print("Indices for Democrats" + str(democrats))
print("Indices for Independents" + str(independents))


pos = nx.kamada_kawai_layout(G)
nx.draw_networkx_nodes(G, pos, node_size = 15, nodelist = republicans, node_color = 'red', alpha = 0.75)
nx.draw_networkx_nodes(G, pos, node_size = 15, nodelist = democrats, node_color = 'blue', alpha = 0.75)
nx.draw_networkx_nodes(G, pos, node_size = 15, nodelist = independents, node_color = 'silver')

edges = G.edges()
rep_relationships = []
dem_relationships = []
ind_relationships = []
out_relationships = []

# Determines which edges are between nodes that are not in the same party or same party
for edge in edges:
	if (edge[0] in republicans and edge[1] in republicans):
		rep_relationships.append(edge)
	elif (edge[0] in democrats and edge[1] in democrats):
		dem_relationships.append(edge)
	elif (edge[0] in independents and edge[1] in independents):
		ind_relationships.append(edge)
	else:
		out_relationships.append(edge)

# Lists for nodes that have no or other types of relationships
no_nodes = []
out_nodes = []

# Determines which nodes have no relationships
for node in list(G.nodes):
	if G.degree[node] == 0:
		no_nodes.append(node)

# Determines which nodes (senators) have relationships with those outside their party
out_nodes = [tuples[1] for tuples in out_relationships] 

# Convert the list to a set and back again to remove duplicates
out_nodes = list(set(out_nodes))


# twitterReverseLookup
mapping = {}
for node in out_nodes:
	mapping[node] = twitterReverseLookup[node]

labels = {}
for node in G.nodes():
	if node in mapping:
		labels[node] = twitterReverseLookup[node]


nx.draw_networkx_labels(G,pos,
	labels,
	font_size=5,
	horizontalalignment='right',
	verticalalignment='bottom'
	)


nx.draw_networkx_edges(
    G,
    pos,
    edgelist=rep_relationships,
    width = 1,
    style = "dashed",
    alpha = 0.25,
    edge_color="orange"
)

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=dem_relationships,
    width = 1,
    style = "dashed",
    alpha = 0.25,
    edge_color="skyblue"
)

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=ind_relationships,
    width = 1,
    style = "dashed",    
    alpha = 0.15,
    edge_color="green"
)

nx.draw_networkx_edges(
    G,
    pos,
    edgelist=out_relationships,
    width = 1,
    alpha = 0.15,
    edge_color="black"
)

plt.show()

