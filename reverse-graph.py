import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


nodata = '-'
merging_col = 'street_name'


def union_and_delete(graph):
    edge_to_remove = list()

    for source, target, attr in graph.edges(data=True):
        attr['node_id'] = {source, target}
        attr['cross_streets'] = set()

    for source, target, attributes in graph.edges(data=True):
        for id1, id2, attr in graph.edges(data=True):
            if source == id1 and target == id2:
                continue
            if (attributes[merging_col] == attr[merging_col] and attributes[merging_col] != nodata) \
                    and len(attributes['node_id'].intersection(attr['node_id'])):
                attributes['node_id'] = attributes['node_id'].union(attr['node_id'])
                attr['node_id'].clear()
                edge_to_remove.append((id1, id2))
            elif (attributes[merging_col] != attr[merging_col] or attributes[merging_col] == nodata) \
                    and len(attributes['node_id'].intersection({id1, id2})):
                if attr[merging_col] != nodata:
                    attributes['cross_streets'].add(attr[merging_col])
                else:
                    attributes['cross_streets'].add(str(id1) + str(nodata) + str(id2))

    graph.remove_edges_from(edge_to_remove)


def reverse_graph(graph):
    new_graph = nx.Graph()

    new_graph.add_nodes_from([(attr[merging_col], attr) if attr[merging_col] != nodata
                              else (str(source) + str(nodata) + str(target), attr)
                              for source, target, attr in graph.edges(data=True)])

    for node_id, attributes in new_graph.nodes(data=True):
        for id, attr in new_graph.nodes(data=True):
            if id in attributes['cross_streets']:
                new_graph.add_edge(node_id, id)

    return new_graph


def draw_graph(graph):
    nx.draw(graph, with_labels=True)
    plt.show()


def convert_to_df(graph, source='source', target='target'):
    edges_df = nx.to_pandas_edgelist(graph, source=source, target=target)
    nodes_df = pd.DataFrame.from_dict(graph.nodes, orient='index')

    return edges_df, nodes_df


def get_reversed_graph(graph, source='source', target='target', merging_column='street_id', empty_cell_sign='-',
                       edge_attr=list['street_id']):
    global nodata
    global merging_col
    nodata = empty_cell_sign
    merging_col = merging_column

    nx_graph = nx.from_pandas_edgelist(graph, source=source, target=target, edge_attr=edge_attr)
    
    adjacency_df = nx.to_pandas_adjacency(nx_graph, weight=merging_column)
    
    union_and_delete(nx_graph)

    new_graph = reverse_graph(nx_graph)
    edges_ds, nodes_df = convert_to_df(new_graph, source=source, target=target)
    return edges_ds, nodes_df, adjacency_df


def main():
    global nodata
    global merging_col
    nodata = '-'
    merging_col = 'street_id'

    graph = pd.read_csv("data/graph1.csv")
    nx_graph = nx.from_pandas_edgelist(graph, source='source', target='target', edge_attr=['street_id', 'street_name'])

    adjacency_df = nx.to_pandas_adjacency(nx_graph, weight='street_id')
    print('\nadjacency_df:\n', adjacency_df.head(7))
    
    union_and_delete(nx_graph)

    new_graph = reverse_graph(nx_graph)
    draw_graph(new_graph)
    
    edges_df, nodes_df = convert_to_df(new_graph, source='source', target='target')
    print('\nedges_df:\n', edges_df.head(7))
    print('\nnodes_df:\n', nodes_df.head(7))


if __name__ == '__main__':
    main()
