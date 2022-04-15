"""

"""
import csv
# Need these for path finding and graphing
import networkx as nx   # K-shortest paths library
import matplotlib.pyplot as plt  # Create the graph

from LinkObj import LinkObj
from NodeObj import NodeObj
from RequestObj import RequestObj


def get_links_from_file(filepath, nodes):
    """
    Return a list of links from the input file. Pass in a list of nodes so the
    links source and destination fields can be defined.
    :param filepath:
    :param nodes:
    :return:
    """
    links = []
    with open(filepath) as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)  # skip the first line
        for line in reader:
            link_id = line[0]
            bandwidth = line[3]

            source_node_id = int(line[1])
            source_node = nodes[source_node_id]
            dest_node_id = int(line[2])
            dest_node = nodes[dest_node_id]

            new_link = LinkObj(link_id, source_node, dest_node, bandwidth)
            links.append(new_link)
    return links


def get_nodes_from_file(filepath):
    """
    Return a list of nodes from the input file.
    """
    nodes = []
    with open(filepath) as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)  # skip the first line
        for line in reader:
            # # (self, node_id, status, cpu, memory, buffer, cost):
            node_id = line[0]
            cost = line[6]

            # 'A' means the node is active
            if line[3] == 'A':
                status = True
            else:
                status = False

            # Turn "[100, 100, 100]" into "100, 100, 100", then split the
            # string into a list using the commas
            resources_string = line[4][1: len(line[4]) - 1]
            resources_list = resources_string.split(',')
            cpu = int(resources_list[0])
            memory = int(resources_list[1])
            buffer = int(resources_list[2])

            new_node = NodeObj(node_id, status, cpu, memory, buffer, cost)
            nodes.append(new_node)

    return nodes


if __name__ == '__main__':
    node_filepath = "../data/NodeInputData.csv"
    nodes = get_nodes_from_file(node_filepath)

    for node in nodes:
        print(node)

    link_filepath = "../data/LinkInputData.csv"
    links = get_links_from_file(link_filepath, nodes)

    for link in links:
        print(link)

    GRAPH = nx.Graph()
