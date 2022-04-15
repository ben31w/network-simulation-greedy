"""
Template for the link object class
"""


class LinkObj:

    def __init__(self, link_id, source_node, dest_node, bandwidth):
        """
        Construct a new link object.
        :param link_id:
            the ID of this link (integer)
        :param source_node:
            the source node of this link (NodeObj)
        :param dest_node:
            the destination node of this link (NodeObj)
        :param bandwidth:
            the bandwidth of this link (integer)
        """
        self.link_id = link_id
        self.source_node = source_node
        self.dest_node = dest_node
        self.bandwidth = bandwidth

    def __str__(self):
        """
        Return string representation of this link. Just here for basic debugging.
        """
        return f"Link ID:{self.link_id}; Source Node:{self.source_node}; " \
               f"Destination Node: {self.dest_node}; Bandwidth: {self.bandwidth}"
