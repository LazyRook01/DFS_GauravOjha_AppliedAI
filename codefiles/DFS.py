import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import json
import time

# Page 1: Recursive Implementation
def page_recursive():
    st.title("DFS Visualization (Recursive Implementation)")

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

# Page 2: Iterative/Stack Implementation
def page_iterative():
    st.title("DFS Visualization (Iterative/Stack Implementation)")

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
            for node, parent in traversal_order:
                st.write(f"Node: {node}, Parent: {parent}")


# Main App
def main():
    st.sidebar.title("DFS Visualization App")
    page = st.sidebar.radio("Select a page:", ("Recursive Implementation", "Iterative/Stack Implementation"))

    if page == "Recursive Implementation":
        page_recursive()
    elif page == "Iterative/Stack Implementation":
        page_iterative()

if __name__ == "__main__":
    main()
