import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
#from core.elements import Network
#from core.elements import Signal_information
import sys
# Ensure the parent directory is in sys.path for importing core module
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))
from core.elements import Signal_information
from core.elements import Node

# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'

signal_info = Signal_information(signal_power=1.0, path=["A", "B", "C", "D"])
print(signal_info.signal_power)  # Output: 1.0
signal_info.update_signal_power(0.5)
print(signal_info.signal_power)  # Output: 1.5
print(signal_info.noise_power)  # Output: 0.0
signal_info.update_noise_power(0.05)
print(signal_info.noise_power)  # Output: 0.05
print(signal_info.latency)  # Output: 0.0
signal_info.update_latency(10)
print(signal_info.latency)  # Output: 10.0
print(signal_info.path)  # Output: ["A", "B", "C", "D"]
signal_info.update_path()
print(signal_info.path)  # Output: ["B", "C", "D"] because of the pop function

nodeA_dict={
    "label":"A",
    "position":(0.0,1.0),
    "connected_nodes":["B","C","D"]
}

nodeC_dict={
    "label":"A",
    "position":(0.0,1.0),
    "connected_nodes":["D"]
}

node_dict = {
    "A": Node({
        "label": "A",
        "position": (0.0, 1.0),
        "connected_nodes": ["B", "D", "C"]
    }),
    "B": Node({
        "label": "B",
        "position": (1.5, 2.5),
        "connected_nodes": ["A", "D", "F"]
    }),
    "C": Node({
        "label": "C",
        "position": (0.0, -1.0),
        "connected_nodes": ["A", "D", "E"]
    }),
    "D": Node({
        "label": "D",
        "position": (1.5, 0.5),
        "connected_nodes": ["A", "B", "C", "E", "F"]
    }),
    "E": Node({
        "label": "E",
        "position": (3.0, -0.5),
        "connected_nodes": ["C", "D", "F"]
    }),
    "F": Node({
        "label": "F",
        "position": (3.0, 2.0),
        "connected_nodes": ["B", "E", "D"]
    })
}

node_A=Node(nodeA_dict)
node_C=Node(nodeC_dict)
node_A.propagate(signal_info)

# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file
