
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
            each request contains function(s). Each function requires a specific
            amount of resources to process. This parameter stores a list of
            integers representing the required resources for each function in
            this request. So if a request has a function that requires four
            resources and a function that requires one resource, this parameter
            will store [4, 1].
        :param requested_bandwidth:
            the bandwidth that will be deducted from each link in this connection
        """
        self.request_id = int(request_id)
        self.source_node = source_node
        self.dest_node = dest_node
        self.requested_resources = list(requested_resources)  # same for CPU, RAM, and buffer
        self.requested_bandwidth = int(requested_bandwidth)
