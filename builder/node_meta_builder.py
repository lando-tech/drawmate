from graph_objects.node import NodeMetaData
from builder.doc_builder import generate_id


class NodeMetaBuilder:

    def init_node_meta(
        self, node_attributes: dict, col_index: int, row_index: int, side: str
    ) -> NodeMetaData:
        """
        Initializes and returns a NodeMetaData object with the specified attributes.
        This method assigns metadata to a node object based on the provided node
        attributes and positional indices.

        Args:
            node_attributes (dict): A dictionary containing specific node attributes
                like 'input-labels', 'output-labels', 'connection-indexes-left', and
                'connection-indexes-right'.
            col_index (int): The column index indicating the node's position in a grid
                structure.
            row_index (int): The row index indicating the node's position in a grid
                structure.
            side (str): The specific side or orientation information related to the
                central node on the graph, such as a matrix/switch.

        Returns:
            NodeMetaData: An object containing the initialized metadata for the node.
        """

        _id = str(generate_id())
        node_meta = NodeMetaData(__SIDE__=side, __ID__=_id)
        node_meta.__LABEL__ = node_attributes["label"]
        node_meta.__ROW_INDEX__ = row_index
        node_meta.__COLUMN_INDEX__ = col_index

        if isinstance(node_attributes["input-labels"], str):
            node_attributes["input-labels"] = node_meta.__INPUT_LABEL__
        elif isinstance(node_attributes["output-labels"], str):
            node_attributes["output-labels"] = node_meta.__OUTPUT_LABEL__
        else:
            node_meta.__INPUT_LABEL_ARRAY__ = node_attributes["input-labels"]
            node_meta.__OUTPUT_LABEL_ARRAY__ = node_attributes["output-labels"]
            self.verify_label_indexes(node_meta)

        node_meta.__CONNECTION_INDEXES_LEFT__ = node_attributes[
            "connection-indexes-left"
        ]
        node_meta.__CONNECTION_INDEXES_RIGHT__ = node_attributes[
            "connection-indexes-right"
        ]

        self.verify_spanning_node(node_meta)
        self.verify_multi_connection_node(node_meta)

        return node_meta

    def verify_spanning_node(self, node_meta: NodeMetaData) -> None:
        """
        Determines if a node should be marked as a spanning node based on its label and
        updates the node's metadata accordingly.

        Args:
            node_meta (NodeMetaData): The metadata associated with a node, which will
            be checked and possibly modified.

        Returns:
            None
        """
        if node_meta.__LABEL__ == "__SPAN__" or node_meta.__LABEL__ == "":
            node_meta.__SPANNING_NODE__ = True

    def verify_label_indexes(self, node_meta: NodeMetaData) -> None:
        """
        Verifies and updates label indexes for the given node metadata.

        This method ensures that each label in the input label array of the provided
        NodeMetaData object is assigned a corresponding index and updates the label
        indexes list accordingly. It calculates the indexes using the current row
        index of the node and the index of each label within the label array.

        Parameters:
        node_meta (NodeMetaData): The metadata of the node containing label and index
        information to be processed.

        Returns:
        None
        """
        if len(node_meta.__INPUT_LABEL_ARRAY__) > 0:
            for index, label in enumerate(node_meta.__INPUT_LABEL_ARRAY__):
                node_meta.__LABEL_INDEXES__.append(node_meta.__ROW_INDEX__ + index)

    def verify_multi_connection_node(self, node_meta: NodeMetaData) -> None:
        """
        Verifies the multi-connection state of a node based on its connection metadata.
        The method determines whether a node has multiple connections on the left
        and/or right sides by analyzing the connection metadata and computing the
        connection counts. The node's multi-connection status is then updated accordingly.

        Args:
            node_meta (NodeMetaData): Metadata object for the node, containing connection
            indexes and related attributes.

        Returns:
            None
        """
        connection_length_left = len(node_meta.__CONNECTION_INDEXES_LEFT__)
        connection_length_right = len(node_meta.__CONNECTION_INDEXES_RIGHT__)

        if connection_length_left <= 1 and connection_length_right <= 1:
            node_meta.__MULTI_CONNECTION_LEFT__ = False
            node_meta.__MULTI_CONNECTION_RIGHT__ = False
            return

        connection_count_left = self.get_connection_count(
            node_meta.__CONNECTION_INDEXES_LEFT__
        )
        connection_count_right = self.get_connection_count(
            node_meta.__CONNECTION_INDEXES_RIGHT__
        )

        if connection_count_left > 1:
            node_meta.__MULTI_CONNECTION_LEFT__ = True
        if connection_count_right > 1:
            node_meta.__MULTI_CONNECTION_RIGHT__ = True

    @staticmethod
    def get_connection_count(connection_indexes: list) -> int:
        """
        Calculates the total count of valid connections from a given list of connection indexes.

        This method iterates through a list of connection indexes and determines the number
        of valid connections by excluding those marked as "NONE". It returns the total count
        of valid connections as an integer.

        Args:
            connection_indexes (list): A list containing connection indexes. Non-valid connections
                are represented as the string "NONE".

        Returns:
            int: The count of valid connections in the provided list.
        """
        connection_count = 0
        for connection in connection_indexes:
            if connection != "NONE":
                connection_count += 1

        return connection_count
