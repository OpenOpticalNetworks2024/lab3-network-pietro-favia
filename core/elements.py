import json
import math
import pandas as pd
import matplotlib.pyplot as plt

class Signal_information(object):
    def __init__(self, signal_power: float, path: list):
        self._signal_power = signal_power
        self._noise_power = 0.0
        self._latency = 0.0 # Total Time Delay due to signal propagation along the whole path
        self._path = path  # Initialize the path with the given list of node labels (through which the signal must travel)

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
    def path(self, new_path: list[str]): #to check that the new path value is a list of strings
        if isinstance(new_path, list) and all(isinstance(node, str) for node in new_path):
            self._path = new_path #if yes, we can set the new path
        else:
            raise ValueError("Path must be a list of strings") #otherwise, it raises an error!

    def update_path(self):
        if self._path:  # Remove the first node in the path
            self._path.pop(0)
        else:
            print("Path is empty. No further nodes to propagate through.")


class Node(object):
    def __init__(self, node_dict: dict):
        """
        the dictionary node_dict should have 'label', 'position', and 'connected_nodes' keys
        """
        self._label = node_dict['label']  # (string)
        self._position = tuple(node_dict['position'])  # (tuple of floats) = (x,y) :2D Cartesian Spatial Coordinates of a node in the Network
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
         propagate the signal information by updating its path and
         calling the propagate method of the next element in the successive dict
         """
        # Update the signal's path by removing the first node (the starting node)
        signal_information.update_path()

        # Get the next node in the path
        if signal_information.path:
            next_node_label = signal_information.path[0]  # The next node label is the first in the updated path
            print(f"Propagating to next node: {next_node_label}")
            if next_node_label in self._successive: # Check if the next node in the path is present in successive dict
                # of the current node
                next_line = self._successive[next_node_label] # Get next line (successive element) and propagate further
                next_line.propagate(signal_information)  # Propagate the signal through the next line (which is the
                # link between the current and the next node)
            else: # this branch runs when there's no connection to that node
                print(f"Error: No successive node found for {next_node_label}")
        else: # this branch runs when path(=list of nodes) is empty
            print("End of path reached.")


class Line(object):
    def __init__(self, label, length):
        self._label = label # (string)
        self._length = length # (float)
        self._successive = {}  # Initialize as empty dict -> successive nodes are stored here (as a dict)

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, value: dict):
        self._successive = value

    def latency_generation(self):
        """Calculate and return the latency through this line"""
        speed_of_light = 3 * 10**8  # Speed of light in vacuum 3e8(m/s)
        light_speed_in_fiber = (2/3) * speed_of_light  # Speed in the fiber
        latency = self._length / light_speed_in_fiber  # Latency formula
        return latency

    def noise_generation(self, signal_power):
        """Calculate and return the noise power for the given signal power"""
        noise = 1e-9 * signal_power * self._length  # Noise formula
        return noise

    def propagate(self, signal_information):
        """
        Update the signal information by adding the noise and latency,
        and then propagate to the next node in the successive dictionary
        """
        # Update latency
        latency = self.latency_generation()
        signal_information.update_latency(latency)  # Add the calculated latency

        # Update noise power
        noise = self.noise_generation(signal_information.signal_power)
        signal_information.update_noise_power(noise)  # Add the calculated noise

        # Get the next node in the path (if any)
        signal_information.update_path()
        if signal_information.path:
            next_node_label = signal_information.path[0]
            if next_node_label in self.successive:
                # Propagate the signal to the next element (node)
                next_node = self.successive[next_node_label]
                next_node.propagate(signal_information)
            else:
                print(f"Error: No successive node found for {next_node_label}")
        else:
            print("End of path reached.")


class Network(object):
    def __init__(self, nodes_file='nodes.json'):
        self._nodes = {}  # Dictionary to store nodes, key = node label
        self._lines = {}  # Dictionary to store lines, key = concatenated node labels

        # Load nodes from JSON file and create node and line instances
        self._load_nodes(nodes_file)
        self._create_lines() #to ensure a bidirectional link for each couple of nodes

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def _load_nodes(self, nodes_file):
        """Load nodes from a JSON file and create Node instances"""
        with open(nodes_file, 'r') as file:
            nodes_data = json.load(file) # returns the corresponding df where keys are node labels

        for node_label, node_value in nodes_data.items():
            node_value['label'] = node_label
            value = Node(node_value)
            self._nodes[node_label] = value # e.g. dict "A": obj of Node class with attributes values from js file

        for node_label, node in self.nodes.items(): # Loop over each node in the nodes dict
            for connected_node_label in node.connected_nodes: # Loop over each node connected to the current node
                if connected_node_label in self.nodes: # Check if the connected node exists
                    # Calculate the distance between the current node and its connected node
                    length = self._calculate_distance(node.position, self.nodes[connected_node_label].position)
                    # Create a label for the line as a combination of the two node labels e.g. "AB"
                    line_label = f"{node_label}{connected_node_label}"
                    if line_label not in self.lines: # Check if this line label does not already exist in self.lines
                        line = Line(line_label, length) # Create a new Line instance with determined length and label
                        self.lines[line_label] = line # Add this new line to the network's lines dictionary

    def _create_lines(self):
        """Create line instances connecting all nodes in the network"""
        for node in self._nodes.values():
            for connected_label in node.connected_nodes:
                # Ensure each line is created only once in each direction e.g."BA" already exists in lines dict?
                if node.label + connected_label not in self._lines:
                    length = self._calculate_distance(node, self._nodes[connected_label])
                    line = Line(node.label + connected_label, length)
                    self._lines[node.label + connected_label] = line

    def _calculate_distance(self, pos1, pos2):
        """Euclidean distance between two 2D positions"""
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


    def draw(self):
        """Visualize the network sketch using matplotlib"""
        plt.figure(figsize=(10, 10))
        for line in self._lines.values():
            start_label, end_label = line.label[0], line.label[1]
            start_node, end_node = self._nodes[start_label], self._nodes[end_label]
            x_values = [start_node.position[0], end_node.position[0]]
            y_values = [start_node.position[1], end_node.position[1]]
            plt.plot(x_values, y_values, 'g-')  # Plot line between 2 nodes

        for node in self._nodes.values():
            plt.plot(node.position[0], node.position[1], 'bo', markersize=12)
            plt.text(node.position[0]+22500, node.position[1]+22500, node.label, fontsize=30, ha='right')
        plt.xlabel('X position')
        plt.ylabel('Y position')
        plt.title('Network Graph')
        plt.grid(True)
        plt.ylim(-3.8e5,5e5)
        plt.show()

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, start_label, end_label):
        """Return all unique paths from start_label to end_label"""

        def dfs(current_label, end_label, visited, path):
            visited.add(current_label)
            path.append(current_label)
            if current_label == end_label:
                paths.append(list(path))
            else:
                for neighbor in self._nodes[current_label].connected_nodes:
                    if neighbor not in visited:
                        dfs(neighbor, end_label, visited, path) #recursive call
            path.pop() #needed backtrack
            visited.remove(current_label)

        paths = [] # here I store all valid paths from start_ to end_ label
        dfs(start_label, end_label, set(), []) # Depth-First Search execution
        return paths

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        """Set successive attributes for each node and line."""
        for line in self._lines.values():
            # Assign the line's successive node
            start_label, end_label = line.label[0], line.label[1]
            line.successive[end_label] = self._nodes[end_label]
            # Assign each node's successive line
            self._nodes[start_label].successive[end_label] = line

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        """Propagate signal information through the path defined in signal_information"""

        """start_node = self._nodes[signal_information.path[0]]
        start_node.propagate(signal_information)
        #v = 2/3*3e8 #signal speed inside the fiber is at around 2/3 of the speed of light
        #"""

        while signal_information.path:
            current_node_label = signal_information.path[0]
            signal_information.update_path()  # Remove current node from path

            if signal_information.path:# Continue propagation until path is empty
                next_node_label = signal_information.path[0]  # Get the next node label (after pop out)
                line_key = current_node_label + next_node_label
                if next_node_label in self._nodes[current_node_label].connected_nodes: #and line_key in self._lines:
                    next_line=self._lines[line_key]
                    #signal_information.update_latency(next_line.length/v) # update delay in local (not needed)
                    latency = next_line.latency_generation()
                    noise = next_line.noise_generation(signal_information.signal_power)
                    signal_information.update_latency(latency) #update latency
                    signal_information.update_noise_power(noise) #update noise power
                    #signal_information.update_signal_power() #update signal power ?
                    #next_line.propagate(signal_information)#i don't think is necessary
                    print(f" Crossed node {next_node_label} from {current_node_label}")
                else:
                    print(f"Error: No successive line found for {next_node_label} from {current_node_label}")
                    break # Stop propagation if no line connects the nodes

        print("End of path reached.")
        return signal_information

    def analyze_paths(self):
        """Create a DataFrame for each possible path, by updating latency, noise and SNR"""
        data = []
        for start_label in self._nodes.keys():
            for end_label in self._nodes.keys():
                if start_label != end_label:
                    paths = self.find_paths(start_label, end_label)
                    for path in paths:
                        path_str = '->'.join(path)
                        # Create a signal information object with initial power of 1 mW (0.001 W)
                        signal_info = Signal_information(0.001, path)
                        # Propagate signal through the path
                        signal_info = self.propagate(signal_info)
                        # Calculate the SNR in dB
                        snr_db = 10 * math.log10(signal_info.signal_power / signal_info.noise_power)
                        # Append data for DataFrame
                        data.append({
                            'Path': path_str,
                            'Latency (s)': signal_info.latency,
                            'Noise Power (W)': signal_info.noise_power,
                            'SNR (dB)': snr_db
                        })
        # Create DataFrame
        df = pd.DataFrame(data)
        return df