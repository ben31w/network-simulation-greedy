# network-simulation-single-mapping

Simulates a traditional computer network that uses single mapping 
(i.e., each node in the network can map only one function in a given request).


The program takes in several input files to model the network: 
<ol>
  <li>a file that defines a list of nodes, each with an arbitrary ID, resources 
    (CPU, Memory, and Buffer Size), processing delay, and processing cost.</li>
  <li>a file that defines a list of links, each with an arbitrary ID, source and
    destination node, bandwidth, edge delay, and edge cost.
</ol>


The program uses networkx to graph the network.

------------
Eventually, the program will read in a list of requests and output the 
