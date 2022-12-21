"""

"""
import ast
import csv
# Need these for path finding and graphing
import networkx as nx   # K-shortest paths library
import matplotlib.pyplot as plt  # Create the graph

from LinkObj import LinkObj
from NodeObj import NodeObj
from RequestObj import RequestObj


def get_links_from_file(filepath, nodes):
    """
    Receive a csv file of links, return a list of link objects.
    :param filepath:    csv file to process
    :param nodes:       list of node objects in the network. Needed to set src
                            and dest of each link.
    :return:            list of link objects
    """
    links = []
    sorted_nodes = sorted(nodes)
    with open(filepath) as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)  # skip the first line
        for line in reader:
            link_id = line[0]
            bandwidth = line[3]
            edge_delay = float(line[4])
            edge_cost = int(line[5])

            # Input file gives the node IDs of src and destination, which is off
            # by 1 from the indices in sorted nodes list.
            source_node_index = int(line[1]) - 1
            source_node = sorted_nodes[source_node_index]
            dest_node_index = int(line[2]) - 1
            dest_node = sorted_nodes[dest_node_index]

            new_link = LinkObj(link_id, source_node, dest_node, bandwidth,
                               edge_delay, edge_cost)
            links.append(new_link)
    return links


def get_nodes_from_file(filepath):
    """
    Receive a csv file of nodes, return a list of node objects.
    :param filepath:    csv file to process
    :return:            list of node objects
    """
    nodes = []
    with open(filepath) as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)  # skip the first line
        for line in reader:
            node_id = int(line[0])
            processing_delay = int(line[5])
            processing_cost = int(line[6])

            # 'A' means the node is active
            if line[3] == 'A':
                status = True
            else:
                status = False

            resources = ast.literal_eval(line[4])
            cpu = int(resources[0])
            memory = int(resources[1])
            buffer = int(resources[2])

            new_node = NodeObj(node_id, status, cpu, memory, buffer,
                               processing_delay, processing_cost)
            nodes.append(new_node)
    return nodes


def get_requests_from_file(filepath, nodes):
    """
    Receive a csv file of requests, return a list of request objects.
    Requests are objects with the following fields:
        r = <id, src, dest, [requested_resources], requested_bandwidth>
        requested_resources is a list of integers indicating the resources that
        each function in this request needs
    :param filepath:    csv file to process
    :param nodes:       list of node objects in the network. Needed to set src
                            and dest of each request.
    :return:            list of request objects
    """
    requests = []
    sorted_nodes = sorted(nodes)  # sort nodes by index
    with open(filepath) as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)  # skip the first line
        for line in reader:
            request_id = int(line[0])
            requested_bandwidth = int(line[4])

            # Input file gives the node IDs of src and destination, which is off
            # by 1 from the indices in sorted nodes list.
            source_node_index = int(line[1]) - 1
            source_node = sorted_nodes[source_node_index]
            dest_node_index = int(line[2]) - 1
            dest_node = sorted_nodes[dest_node_index]

            # Turn "['F4', 'F1', 'F3']" into a list using ast.literal_eval
            # Then convert the list of functions ['F4', 'F1', ... ]
            # into a list of resources being requested by each function [4, 1, ..]
            # Requested resources indicates the CPU, Memory, and Buffer that
            # will be allocated from the node that processes this function.
            functions = ast.literal_eval(line[3])
            requested_resources = [int(function[1]) for function in functions]

            new_request = RequestObj(request_id, source_node, dest_node,
                                     requested_resources, requested_bandwidth)
            requests.append(new_request)
    return requests


def process_requests(graph, requests):
    """
    Process the list of requests. Map one function in each request to a node.
    :param graph: a networkx graph with nodes and edges. Simulates a computer
                network that processes requests
    :param requests: a list of request objects
    :return: the number of successful requests
    """
    num_successes = 0

    # TODO Prune the network by removing nodes and edges that aren't feasible (not enough resources or bandwidth).


    for request in requests:
        src = request.source_node
        dest = request.dest_node
        requested_resources = request.requested_resources  # [1,2,6]
        requested_bandwidth = request.requested_bandwidth  # 5

        # Need to find a path from src to dest.
        # Because this is a single mapping network,
        # len(path) must be at least len(requested_resources)

        # If this request has three functions to map, then the path must have at
        # least three nodes.

        # Some nodes may map a function and some may not. Each node that maps a
        # function will subtract a requested resource.
        # cost of 1 means subtract 1 from (CPU, RAM, and buffer)

        # Each link in the path will have the requested bandwidth subtracted.
    return num_successes

if __name__ == '__main__':
    # Read input files and get the nodes and links
    node_filepath = "../data/NodeInputData.csv"
    nodes = get_nodes_from_file(node_filepath)
    link_filepath = "../data/LinkInputData.csv"
    links = get_links_from_file(link_filepath, nodes)
    # for node in nodes:
    #     print(node)
    # for link in links:
    #     print(link)

    # Graph the nodes and links (we just need the IDs, not the objects)
    GRAPH = nx.Graph()
    graph_links = [(link.source_node.node_id, link.dest_node.node_id) for link in links]
    GRAPH.add_edges_from(graph_links)
    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show()

    print(GRAPH)
    print(GRAPH.nodes)
    print(GRAPH.edges)

    # Read input file and get the requests
    requests_filepath = "../data/RequestInputData.txt"
    requests = get_requests_from_file(requests_filepath, nodes)
    # for request in requests:
    #     print(request)


