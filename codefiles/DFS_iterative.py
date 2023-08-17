import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import json
import time

# Streamlit app title
st.title("DFS Visualization on an Undirected Graph (Iterative/Stack Implementation)")

# Add credit line
st.markdown("### Created by Gaurav Ojha (VisFac, Applied AI) based on https://www.youtube.com/watch?v=PMMc4VsIacU")

# Define the visualize_graph function
def visualize_graph(graph, pos, visited, current_node=None, parent=None, highlight_node=None, stack=None):
    plt.figure(figsize=(10, 6))
    node_colors = ["green" if node == current_node else "blue" if node in visited else "gray" for node in graph.nodes]
    edge_colors = ["blue" if (node, neighbor) == (parent, current_node) else "gray" for node, neighbor in graph.edges]
    
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        edge_color=edge_colors,
        font_color='black',
        font_weight='bold',
        node_size=1000,
    )

    if stack:
        stack_text = "\n".join(f"{node} ({parent})" for node, parent in stack)
        plt.text(1.1, 0.5, f"Stack:\n{stack_text}", fontsize=10, ha="left", va="center")

    plt.title("DFS Visualization")
    st.pyplot(plt)
    plt.close()

# Rest of your Streamlit app code
st.write("Upload a text file that contains JSON-like adjacency list format.")
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

def dfs_stack(graph, start_node):
    stack = [(start_node, None)]
    visited = set()  # Initialize the 'visited' set
    traversal_order = []

    while stack:
        current_node, parent = stack.pop()

        if current_node not in visited:
            visited.add(current_node)
            traversal_order.append((current_node, parent))
            neighbors = graph[current_node]
            visualize_graph(graph, pos, visited, current_node, parent, current_node, stack)
            time.sleep(1)

            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, current_node))
        else:
            visualize_graph(graph, pos, visited, current_node, parent, current_node, stack)
            time.sleep(1)

    return traversal_order

if uploaded_file is not None:
    file_contents = uploaded_file.read().decode("utf-8")
    adjacency_list = json.loads(file_contents)
    G = nx.Graph()

    # Process the adjacency list and add nodes and edges to the graph
    for node, neighbors in adjacency_list.items():
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
        
    # Draw the initial graph
    pos = nx.spring_layout(G)
    visualize_graph(G, pos, set())

    start_node = st.selectbox("Enter the starting node for DFS:", list(G.nodes) if G.nodes else "")

    if st.button("Start DFS"):
        traversal_order = dfs_stack(G, start_node)
        st.write("DFS traversal completed.")
        
        st.subheader("Visited Order")
        for node in traversal_order:
            st.write(f"Node: {node}")


