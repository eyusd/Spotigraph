import spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import numpy as np


scope =
client_id=
client_secret=
redirect_uri=
username=
token=util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
sp = spotipy.Spotify(auth=token)

def refresh():
    print("Refreshing")
    global scope, client_id, client_scret, redirect_uri, username, token, sp
    token=util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
    sp = spotipy.Spotify(auth=token)

G = nx.Graph()
attente = []
deja_vu = []

def suivant(x):
    try:
        res = sp.artist_related_artists('spotify:artist:'+x)
    except spotipy.client.SpotifyException:
        refresh()
        res = sp.artist_related_artists('spotify:artist:'+x)
    
    results = []
    for item in res['artists']:
        results.append(item['uri'][15:])
    return results

def name(uri):
    try:
        return sp.artist('spotify:artist:'+uri)['name']
    except spotipy.client.SpotifyException:
        refresh()
        return sp.artist('spotify:artist:'+uri)['name']

def draw(g):
    remove = [node for node,degree in dict(g.degree()).items() if degree < 2]
    g.remove_nodes_from(remove)
    nodesize=[g.degree(n)*10 for n in g]
    pos=nx.kamada_kawai_layout(g)
    nx.draw(g,with_labels=False)
    nx.draw_networkx_nodes(g,pos,node_size=nodesize,node_color='r')
    nx.draw_networkx_edges(g,pos)
    plt.show()

def hache(st):
    return hash(st)%1000

attente=['568ZhdwyaiCyOGJRtNYhWf'] #Led Zeppelin uri
deja_vu = [[]]*1000
deja_vu[hache(attente[0])].append(attente[0])
i=0

while not(attente == []):
    print(i)
    if i%5000 == 0:
        nx.write_gexf(G, "spotigraph.gexf")
    
    sommet = attente.pop(0)
    liens = suivant(sommet)
    for link in liens:
        G.add_node(link)
        G.add_edge(sommet,link)
        pos = hache(link)
        if not(link in deja_vu[pos]):
            attente.append(link)
            deja_vu[pos].append(link)
            i+=1


remove = [node for node,degree in dict(G.degree()).items() if degree < 5]
G.remove_nodes_from(remove)

labels = {}
l = list(G.nodes)
degr = [degree for node,degree in dict(G.degree()).items()]
for x in range(len(degr)):
    if degr[x] > 100:
        labels[x] = name(labels[x])
    else:
        labels[x] = l[x]

F = nx.convert_node_labels_to_integers(G)
F = nx.relabel_nodes(G,labels)

# Save graph
nx.write_gml(G, "spotigraph.gml")
nx.write_gexf(G, "spotigraph.gexf")

# Read graph
#G = nx.read_gml('spotigraph.gml')