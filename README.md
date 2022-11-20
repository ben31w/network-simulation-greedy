# network-simulation-single-mapping

Simulates a computer network that uses single mapping. 
This network processes a list of requests, with each request composed of one or more functions to be run. 
As a single mapping network, each node maps one function in a given request.

This program has several components:
<ol>
  <li>
    First, it models a computer network using the given input files LinkInputData and NodeInputData.
    Each node is a computer and each link is a connection between two computers.
    The network is graphed and displayed with NetworkX.
  </li>
  <li>
    <b>TODO</b>: Then, it processes the file RequestsInputData. 
    It runs the requests and outputs the requests that pass.
  </li>
</ol>

The eventual goal of this program is to compare single mapping networks to other algorithms.

---------

In this network, each node represents a computer with an ID, list of resources [CPU, Memory, Buffer Size], processing delay, and processing cost.

Each link represents a connection with an ID, list of computers [source, destination node], bandwidth, edge delay, and edge cost.

Each request has an ID, source node, destination node, list of requested resources to be allocated from some node between source and destination [CPU, Memory, Buffer cost], and requested bandwidth (which will be allocated from every link between source and destination).
