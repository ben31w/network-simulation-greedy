"""
This project models a computer network running Service Function Chain (SFC)
Mapping. A computer network can be modeled as a graph with nodes (computers/client
terminals) and links (connections between computers). The purpose of SFC mapping
is to process requests from one client terminal to another. Each request has a
source and destination terminal and a list of Virtual Network Functions (VNFs)
to map. These VNFs can be mapped to/processed by any node between (and including)
the source and destination, provided the node has enough resources and the links
(between the source and mapping node) have enough bandwidth. Each VNF has a given
resource cost and each request has a given bandwidth cost.

This particular implementation of SFC mapping receives requests comprised of 1+
VNFs, and each VNF is mapped to one and only one node between the request's src
and dest (single mapping).

SUPPORTING CLASSES/OBJECTS
==========================
Nodes are objects with the following fields:
    n = <id, status, cpu, memory, buffer, processing_delay, processing_cost>
        cpu, memory, and buffer are the computer's resources.

Links are objects with the following fields:
    l = <id, src, dest, bandwidth, edge_delay, edge_cost>

Requests are objects with the following fields:
    r = <id, src, dest, [requested_resources], requested_bandwidth>
        requested_resources is a list of integers indicating the resources that
        each VNF in this request needs
"""
import ast
import csv
# Need these for path finding and graphing
import networkx as nx   # K-shortest paths library
import matplotlib.pyplot as plt  # Create the graph

from LinkObj import LinkObj
from NodeObj import NodeObj
from RequestObj import RequestObj

def get_nodes_from_file(filepath):
    """
    Receive a csv file of nodes, return a list of node objects.
    The csv file contains many columns but not all of them are used.
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


def get_requests_from_file(filepath, nodes):
    """
    Receive a csv file of requests, return a list of request objects.
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
            requested_resources = [int(function[1:]) for function in functions]

            new_request = RequestObj(request_id, source_node, dest_node,
                                     requested_resources, requested_bandwidth)
            requests.append(new_request)
    return requests


def process_requests(request_objects, node_objects, link_objects):
    """
    Process requests through the network.
    :param request_objects: [RequestObj(s)]
    :param node_objects:    [NodeObj(s)] of the network
    :param link_objects:    [LinkObj(s)] of the network
    :return:                number of successful requests
    """
    num_successes = 0
    for request in request_objects:
        if process_one_request(request, node_objects, link_objects):
            num_successes += 1
    return num_successes


def process_one_request(request, node_objects, link_objects):
    """
    Process one request through the network.

    (1) Create a pruned version of the network that can support this request.
        The pruned version removes nodes and links with inadequate resources or bandwidth.
        Pruned graph: G'(N', L')
    (2) Compute K shortest paths over G'(N', L') between the request's source and
        destination. These paths are given by a set of path vectors, P = {p},
        each containing vectors of path nodes and links, i.e., p = {{n}, {l}}.
    (3) The K path routes are then sorted/searched to find VNF mappings for a
        single mapping strategy.
    :param request:         RequestObj
    :param node_objects:    [NodeObj(s)] of the network
    :param link_objects:    [LinkObj(s)] of the network
    :return:                True if the request was processed successfully
    """
    # (1)
    pruned_nodes, pruned_links = prune_network(request, node_objects, link_objects)
    pruned_graph = nx.Graph()
    new_links = [(link.source_node.node_id, link.dest_node.node_id) for link in pruned_links]
    pruned_graph.add_edges_from(new_links)

    # (2) Note if there are no valid paths (empty list), then this request can't be processed
    full_paths = get_path_vectors(pruned_graph, request)
    if not full_paths:
        return False

    # (3)
    # Is sorting the paths necessary? Each link has the same processing delay

    return False


def prune_network(request, node_objects, link_objects):
    """
    Given a request and a network of nodes and links, prune out nodes and
    links that don't have enough resources or bandwidth for the request.
    :param request:         RequestObj
    :param node_objects:    initial NodeObj(s)
    :param link_objects:    initial LinkObj(s)
    :return:                [nodes with enough resources], [links with enough bandwidth]
    """
    pruned_nodes = node_objects.copy()
    pruned_links = link_objects.copy()

    # The request contains a list of functions to map; find the minimum resource
    # cost among this request's functions.
    min_resources = min(request.requested_resources)

    # Prune nodes that don't have enough resources to process this request.
    for node in node_objects:
        if node.cpu < min_resources:
            pruned_nodes.remove(node)
    # Prune links that are connected to pruned nodes.
    for link in link_objects:
        if link.source_node not in pruned_nodes or link.dest_node not in pruned_nodes:
            pruned_links.remove(link)
    # Prune links that don't have enough bandwidth to process this request.
    for link in pruned_links:
        if link.bandwidth < request.requested_bandwidth:
            pruned_links.remove(link)

    return pruned_nodes, pruned_links


def get_path_vectors(graph, request):
    """
    Using the given network/graph, return the k shortest paths for this request.
    More specifically, this method returns path vectors, which are tuples in the
    form: ([path], [path_links])
        path has the nodes of the shortest path, e.g., [19, 5, 2, 16]
        path_links has the links of the shortest path, e.g, [(19,5), (5,2), (2,16)]
    :param graph:   graph representing the network processing this request
    :param request: RequestObj to process
    :return:        [path vectors]
    """
    paths = [p for p in nx.all_shortest_paths(graph,
                                              source=request.source_node.node_id,
                                              target=request.dest_node.node_id)]
    # There are no shortest paths (should be impossible) or the shortest path is
    # too short to process this request; return an empty path list.
    if len(paths) == 0 or len(request.requested_resources) > len(paths[0]):
        return []

    path_links_list = []
    for path in paths:
        path_links = []
        for i in range(0, len(path) - 1):
            ls = path[i], path[i + 1]
            path_links.append(ls)
        path_links_list.append(path_links)

    return zip(paths, path_links_list)


if __name__ == '__main__':
    # Read input files and get the nodes and links
    node_filepath = "../data/NodeInputData.csv"
    nodes = get_nodes_from_file(node_filepath)
    link_filepath = "../data/LinkInputData.csv"
    links = get_links_from_file(link_filepath, nodes)

    # Graph the nodes and links (we just need the IDs, not the objects)
    GRAPH = nx.Graph()
    graph_links = [(link.source_node.node_id, link.dest_node.node_id) for link in links]
    GRAPH.add_edges_from(graph_links)
    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show()

    # Read input file and get the requests
    requests_filepath = "../data/RequestInputData.txt"
    requests = get_requests_from_file(requests_filepath, nodes)

    process_requests(requests, nodes, links)


