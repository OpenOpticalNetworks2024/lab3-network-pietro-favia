import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import sys
# Ensure the parent directory is in sys.path for importing core module
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))
from core.elements import Signal_information, Node, Line, Network

# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'
OUTPUT_FOLDER = ROOT / 'df_output'
OUTPUT_FOLDER.mkdir(exist_ok=True)
csv_output = OUTPUT_FOLDER / 'weighted_path.csv'

# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file

# Initialize the network + Connect nodes and lines
network = Network(file_input)
network.connect()

# Example of a signal to propagate (1 mW initial power)
initial_signal_power = 0.001  # in Watts (1 mW)
signal_info = Signal_information(signal_power=initial_signal_power, path=["A", "B", "F", "E"])
# Propagate signal information through the network starting from path A->B->F->E
modified_signal_info = network.propagate(signal_info)

# Print final signal information properties after propagation
print("Final Signal Power (W):", modified_signal_info.signal_power)
print("Total Noise Power (W):", modified_signal_info.noise_power)
print("Total Latency (s):", modified_signal_info.latency)
print("Remaining Path:", modified_signal_info.path) #if all nodes are crossed is empty!

# Analyze all possible paths and save them in a DataFrame
path_df = network.analyze_paths()
print(path_df.head())  # Display the first few rows for verification

# Save DataFrame to CSV
path_df.to_csv(csv_output, index=False)
print(f"Path data saved to: {csv_output}")

# Visualize the network graph
network.draw()
