import json


class Signal_information(object):
    def __init__(self, signal_power: float, path: list):
        self._signal_power = signal_power
        self._noise_power = 0.0
        self._latency = 0.0
        self._path = path  # Initialize the path with the given list of node labels

    @property
    def signal_power(self):
        return self._signal_power

    def update_signal_power(self, increment: float):
        self._signal_power += increment

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, value: float):
        self._noise_power = value

    def update_noise_power(self, increment: float):
        self._noise_power += increment

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, value: float):
        self._latency = value

    def update_latency(self, increment: float):
        self._latency += increment

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path: list[str]):
        if isinstance(new_path, list) and all(isinstance(node, str) for node in new_path):
            self._path = new_path
        else:
            raise ValueError("Path must be a list of strings")

    def update_path(self):
        if self._path:  # Remove the first node in the path
            self._path.pop(0)


class Node(object):
    def __init__(self, node_dict: dict):
        """
        the dictionary node_dict should have 'label', 'position', and 'connected_nodes' keys.
        """
        self._label = node_dict['label']  # (string)
        self._position = tuple(node_dict['position'])  # (tuple of floats) = (x,y) :2D Cartesian Spatial Coordinates of a node in the network
        self._connected_nodes = node_dict['connected_nodes']  # (list of strings)
        self._successive = {}  # Initialize successive as an empty dictionary

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, value: dict):
        self._successive = value

    def propagate(self,signal_information):
        """
         Propagate the signal information by updating its path and
         calling the propagate method of the next element in the successive dict.
         """
        # Update the signal's path by removing the first node (this node)
        signal_information.update_path()

        # Get the next node in the path
        if signal_information.path:
            next_node_label = signal_information.path[0]  # The next node label is the first in the updated path
            if next_node_label in self._successive:
                # Call the propagate method of the next line in the successive dictionary
                next_line = self._successive[next_node_label]
                next_line.propagate(signal_information)  # Assume that Line class has a propagate method
            else:
                print(f"Error: No successive node found for {next_node_label}")
        else:
            print("End of path reached.")


class Line(object):
    def __init__(self):
        pass

    @property
    def label(self):
        pass

    @property
    def length(self):
        pass

    @property
    def successive(self):
        pass

    @successive.setter
    def successive(self):
        pass

    def latency_generation(self):
        pass

    def noise_generation(self):
        pass

    def propagate(self):
        pass


class Network(object):
    def __init__(self):
        pass

    @property
    def nodes(self):
        pass

    @property
    def lines(self):
        pass

    def draw(self):
        pass

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2):
        pass

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        pass