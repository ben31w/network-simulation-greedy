
class RequestObj:
    def __init__(self, request_id, source_node, dest_node, requested_resources,
                 requested_bandwidth):
        """
        Create a new request object.
        :param request_id:
            ID of this request (integer)
        :param source_node:
            source node of this request (NodeObj)
        :param dest_node:
            dest node of this request (NodeObj)
        :param requested_resources:
            the resources that will be deducted from each node in this connection
        :param requested_bandwidth:
            the bandwidth that will be deducted from each link in this connection
        """
        self.request_id = request_id
        self.source_node = source_node
        self.dest_node = dest_node
        self.requested_resources = requested_resources  # same for CPU, RAM, and buffer
        self.requested_bandwidth = requested_bandwidth
