from py2cytoscape.data.cyrest_client import CyRestClient
import networkx as nx

cy = CyRestClient(ip="127.0.0.1", port=1234)
cy.session.delete()

g = nx.Graph()

# authors as nodes
n_authors = 10
authors_nodes = nx.path_graph(n_authors)
g.add_nodes_from(authors_nodes)

# nodes attributes
g.node[0]["keywords"] = "aaa"
g.node[1]["keywords"] = "bbb"
g.node[2]["keywords"] = "ccc"
g.node[3]["keywords"] = "ddd"

# co-authorship as edges
coauthors_list = [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (5, 6), (6, 7),
                  (7, 8), (8, 9)]
g.add_edges_from(coauthors_list)

deg = nx.degree(g)
btw = nx.betweenness_centrality(g)
nx.set_node_attributes(g, "degree", deg)
nx.set_node_attributes(g, "betweenness", btw)

# create network with cytoscape
g_cy = cy.network.create_from_networkx(g, name="coauth")
cy.layout.apply(name="kamada-kawai", network=g_cy)

style = cy.style.create("Minimal")
cy.style.apply(style, network=g_cy)

cy.edgebundling.apply(g_cy)
g_cy.get_svg()

#
# g = nx.scale_free_graph(500)
# deg = nx.degree(g)
# btw = nx.betweenness_centrality(g)
#
# nx.set_node_attributes(g, 'degree', deg)
# nx.set_node_attributes(g, 'betweenness', btw)
#
# g_cy = cy.network.create_from_networkx(g)
# cy.layout.apply(name='kamada-kawai', network=g_cy)
#
# directed = cy.style.create('Directed')
# cy.style.apply(directed, network=g_cy)
#
# result = cy.edgebundling.apply(g_cy)
# network_png = g_cy.get_png()
