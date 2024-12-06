import random
import time
import streamlit as st
import matplotlib.pyplot as plt

# SensorNode class
class SensorNode:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.energy = 100
        self.cluster_head = False
        self.cluster = None

    def distance_to(self, other_node):
        return ((self.x - other_node.x) ** 2 + (self.y - other_node.y) ** 2) ** 0.5

# WirelessSensorNetwork class
class WirelessSensorNetwork:
    def __init__(self, num_nodes, network_size):
        self.nodes = []
        self.network_size = network_size
        for i in range(num_nodes):
            x = random.uniform(0, network_size)
            y = random.uniform(0, network_size)
            self.nodes.append(SensorNode(i, x, y))

    def form_clusters(self, num_clusters):
        cluster_heads = random.sample(self.nodes, num_clusters)
        for node in self.nodes:
            closest_ch = min(cluster_heads, key=lambda ch: node.distance_to(ch))
            node.cluster_head = (node == closest_ch)
            node.cluster = closest_ch.id

    def energy_efficient_routing(self):
        for node in self.nodes:
            if not node.cluster_head:
                node.energy = max(0, node.energy - 0.5)
            else:
                node.energy = max(0, node.energy - 0.2)

    def display_network(self):
        fig, ax = plt.subplots()
        for node in self.nodes:
            if node.cluster_head:
                ax.plot(node.x, node.y, 'ro', label=f'Cluster Head {node.id}' if f'Cluster Head {node.id}' not in ax.get_legend_handles_labels()[1] else "")
            else:
                ax.plot(node.x, node.y, 'bo')
                if node.cluster is not None:
                    ch = next(n for n in self.nodes if n.id == node.cluster)
                    ax.plot([node.x, ch.x], [node.y, ch.y], 'g--')
        ax.set_title("Wireless Sensor Network")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.legend()
        return fig

# Streamlit UI
st.title("Energy-Efficient Routing in IoT Networks")

# Simulation parameters
num_nodes = st.sidebar.slider("Number of Nodes", 5, 50, 10)
network_size = st.sidebar.slider("Network Size", 50, 200, 100)
num_clusters = st.sidebar.slider("Number of Clusters", 2, num_nodes // 2, 3)
simulate_steps = st.sidebar.slider("Simulation Steps", 1, 10, 5)

# Initialize network
if "network" not in st.session_state:
    st.session_state.network = WirelessSensorNetwork(num_nodes, network_size)
    st.session_state.network.form_clusters(num_clusters)

# Display network
st.subheader("Sensor Network Visualization")
fig = st.session_state.network.display_network()
st.pyplot(fig)

# Simulate energy-efficient routing
st.subheader("Simulation")
if st.button("Run Simulation"):
    for step in range(simulate_steps):
        st.session_state.network.energy_efficient_routing()
        st.write(f"Step {step + 1} completed.")
        time.sleep(0.5)

    st.write("Simulation finished.")
    fig = st.session_state.network.display_network()
    st.pyplot(fig)

# Node details
st.subheader("Node Details")
for node in st.session_state.network.nodes:
    st.write(
        f"Node {node.id}: Energy = {node.energy:.2f} mAh, "
        f"Cluster Head = {node.cluster_head}, Cluster = {node.cluster}"
    )
