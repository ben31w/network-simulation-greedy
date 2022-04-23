# network-simulation-single-mapping

Simulates a traditional computer network that uses single mapping 
(i.e., each node in the network can map only one function in a given request).


The program takes in several input files to model the network: 
<ol>
  <li>a file that defines a list of nodes, each with an arbitrary ID, resources 
    (CPU, Memory, and Buffer Size), processing delay, and processing cost.</li>
  <li>a file that defines a list of links, each with an arbitrary ID, source and
    destination node, bandwidth, edge delay, and edge cost.</li>
  <li>a file that defines a list of requests, each with an arbitrary ID, source node,
    destination node, requested resources (the CPU, Memory, and Buffer that will be 
    allocated from a node between [source, destination]), and requested bandwidth (which
    will be allocated from every link between source and destination).</li>
</ol>


The program uses networkx to graph the network.

------------
Eventually, the program will read in a list of requests and output the requests that pass.
