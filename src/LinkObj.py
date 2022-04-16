"""
Template for the link object class
"""


class LinkObj:

    def __init__(self, link_id, source_node, dest_node, bandwidth, edge_delay,
                 edge_cost):
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
        :param edge_delay:
            the delay that this link will add to each request mapped through it
            (float)
        :param edge_cost:
            the cost that this link will add to each request mapped through it
            (integer)
        """
        self.link_id = int(link_id)
        self.source_node = source_node
        self.dest_node = dest_node
        self.bandwidth = int(bandwidth)
        self.edge_delay = float(edge_delay)
        self.edge_cost = int(edge_cost)

    def __str__(self):
        """
        Return string representation of this link. Just here for basic debugging.
        """
        return f"Link ID: {self.link_id}; <SRC: {self.source_node}>; " \
               f"<DEST: {self.dest_node}>; Bandwidth: {self.bandwidth}; " \
               f"Edge delay: {self.edge_delay}; Edge cost: {self.edge_cost}"
