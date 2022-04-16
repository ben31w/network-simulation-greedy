"""
Template for the node object class
"""


class NodeObj:

    def __init__(self, node_id, status, cpu, memory, buffer, processing_delay,
                 processing_cost):
        """
        Construct a new Node object.
        :param node_id:
            ID of this node (integer)
        :param status:
            True if this node has enough resources for a connection (boolean)
        :param cpu:
            one of this node's resources (integer)
        :param memory:
            one of this node's resources (integer)
        :param buffer:
            one of this node's resources (integer)
        :param processing_delay:
            the delay that this node will add to each request mapped through it
            (integer)
        :param processing_cost:
            the cost that this node will add to each request mapped through it
            (integer)
        """
        self.node_id = int(node_id)
        self.status = status
        self.cpu = int(cpu)
        self.memory = int(memory)
        self.buffer = int(buffer)
        self.processing_delay = int(processing_delay)
        self.processing_cost = int(processing_cost)

    def __lt__(self, other):
        """
        Compare two node objects by comparing their IDs.
        :param other: the other node being compared to this node.
        :return: 1 if this node's ID < other node's ID
        """
        return self.node_id < other.node_id

    def __str__(self):
        """
        Return string representation of this node. Just here for basic debugging.
        """
        return f"Node ID: {self.node_id}; Status: {self.status}; CPU: {self.cpu}; " \
               f"Memory: {self.memory}; Buffer: {self.buffer}; Processing Delay: " \
               f"{self.processing_delay}; Processing Cost: {self.processing_cost}"
