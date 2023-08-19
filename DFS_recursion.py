import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import json
import time

# Streamlit app title
st.title("DFS Visualization on an Undirected Graph (Recursive Implementation)")
# Add credit line
st.markdown("### Created by Gaurav Ojha (VisFac, Applied AI) based on https://www.youtube.com/watch?v=PMMc4VsIacU")

st.write("Upload a text file that contains JSON-like adjacency list format.")
# Upload a text file
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

def dfs_step_by_step(graph, node, parent, visited, pos, visited_order, backtracking_edges):
    visited[node] = True
    graph.nodes[node]['color'] = 'green'  # Change node color to green once visited
    visited_order.append((node, parent))  # Append to visited order list with parent node
    neighbors = graph[node]
    visualize_graph(graph, pos, node, parent)
    time.sleep(1)  # Pause for visualization
    for neighbor in neighbors:
        if not visited[neighbor]:
            graph[node][neighbor]['color'] = 'blue'  # Color edge as traversed
            backtracking_edges.append((node, neighbor))  # Append to backtracking edges
            visualize_graph(graph, pos, node, parent, neighbor)  # Update current node
            time.sleep(1)
            dfs_step_by_step(graph, neighbor, node, visited, pos, visited_order, backtracking_edges)
    if all(visited[neighbor] for neighbor in neighbors):
        if backtracking_edges:
            backtrack_edge = backtracking_edges[-1]
            graph[backtrack_edge[0]][backtrack_edge[1]]['color'] = 'red'  # Color backtracking edge as red
            visualize_graph(graph, pos, node, parent)
            time.sleep(1)
            graph[backtrack_edge[0]][backtrack_edge[1]]['color'] = 'blue'  # Reset edge color
            visualize_graph(graph, pos, node, parent)
            time.sleep(1)
            backtracking_edges.pop()  # Remove backtracking edge from list

def visualize_graph(graph, pos, current_node=None, parent_node=None, neighbor_node=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    node_colors = [graph.nodes[node]['color'] for node in graph.nodes]
    edge_colors = [graph[u][v]['color'] for u, v in graph.edges]
    nx.draw(graph, pos, with_labels=True, node_size=1000, font_size=10, font_color='black', font_weight='bold',
            edgelist=graph.edges, edge_color=edge_colors, edge_cmap=plt.cm.Blues, node_color=node_colors, width=2, ax=ax)
    if current_node is not None:
        ax.annotate(f"Current Node: {current_node}", (0.5, 0.95), xycoords="axes fraction",
                    ha="center", fontsize=12, color="red")
    if parent_node is not None:
        ax.annotate(f"Parent Node: {parent_node}", (0.5, 0.9), xycoords="axes fraction",
                    ha="center", fontsize=12, color="green")
    plt.title("Step-by-Step DFS Visualization")
    st.pyplot(fig)

if uploaded_file is not None:
    # Read the uploaded file and convert it to a string
    file_contents = uploaded_file.read().decode("utf-8")
    
    # Parse the adjacency list from JSON-like format
    adjacency_list = json.loads(file_contents)
    
    # Create an undirected graph using NetworkX
    G = nx.Graph()
    
    # Process the adjacency list and add nodes and edges to the graph
    for node, neighbors in adjacency_list.items():
        G.add_node(node, color='gray')  # Initialize node color
        for neighbor in neighbors:
            G.add_edge(node, neighbor, color='gray')  # Initialize edge color
        
    # Draw the initial graph
    pos = nx.spring_layout(G)
    visualize_graph(G, pos)
    
    # Get user input for the starting node
    start_node = st.text_input("Enter the starting node for DFS:", next(iter(G.nodes)))
    
    if st.button("Start DFS"):
        # Perform DFS step by step and visualize each step
        visited = {node: False for node in G.nodes}
        visited_order = []  # To keep track of visited order
        backtracking_edges = []  # To keep track of backtracking edges
        dfs_step_by_step(G, start_node, None, visited, pos, visited_order, backtracking_edges)
        st.write("DFS traversal completed.")
        
        # Display the order in which nodes were visited along with their parent nodes
        st.subheader("Visited Order")
        for node, parent in visited_order:
            st.write(f"Node: {node}")
