"""
Template for the node object class
"""


class NodeObj:

    def __init__(self, node_id, status, cpu, memory, buffer, cost):
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
        :param cost:
            the cost that this node will add to each request mapped through it
            (integer)
        """
        self.node_id = node_id
        self.status = status
        self.cpu = cpu
        self.memory = memory
        self.buffer = buffer
        self.cost = cost

    def __str__(self):
        """
        Return string representation of this node. Just here for basic debugging.
        """
        return f"Node ID: {self.node_id}; Status: {self.status}; CPU: {self.cpu}; " \
               f"Memory: {self.memory}; Buffer: {self.buffer}; Cost: {self.cost}"
