import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button, Slider
import random
import copy
import inspect

# Define core model structure
class Model:
    """Represents a disease or state transition model with states and transitions."""
    def __init__(self, name="Generic Model"):
        self.name = name
        self.states = []
        self.transitions = []
        self.default_state = None

    def add_state(self, name, color, number=0, default=False):
        # Create a new state and add it to the model's states list
        state = State(name, color, number)
        self.states.append(state)
        # Set this state as the default state if specified
        if default:
            self.default_state = state.name
        return state

    def add_transition(self, from_state, to_state, probability,
                       requires_proximity=False, contact_with=None):
        # Add a transition rule from one state to another with given conditions
        # requires_proximity and contact_with define if transition depends on neighbor states
        t = Transition(from_state, to_state, probability,
                       requires_proximity, contact_with)
        self.transitions.append(t)

class State:
    """Represents a single state in the model with a name, color, and optional number."""
    def __init__(self, name, color, number=0):
        self.name = name
        self.color = color  # RGB tuple (0–255)
        self.number = number


class Transition:
    """Represents a state transition rule with conditions and probability."""
    def __init__(self, from_state, to_state, probability,
                 requires_proximity=False, contact_with=None):
        self.from_state = from_state
        self.to_state = to_state
        self.probability = probability
        self.requires_proximity = requires_proximity
        self.contact_with = contact_with


# === Network abstraction ===
class Network:
    """Wraps a NetworkX graph with model state management for nodes."""
    def __init__(self, model):
        self.model = model
        self.graph = nx.Graph()

    def add_node(self, node_id, state_name=None):
        self.graph.add_node(node_id)
        if state_name is None:
            state_name = self.model.default_state
        self.graph.nodes[node_id]['state'] = state_name

    def add_nodes(self, count, state_name=None, start_id=1):
        for i in range(start_id, start_id + count):
            self.add_node(i, state_name if state_name is not None else self.model.default_state)

    def add_edges(self, *edges):
        new_edges = []
        for edge in edges:
            new_edges.append((edge[0], edge[1]))
        self.graph.add_edges_from(new_edges)

    def set_state(self, node_ids, state_name):
        if isinstance(node_ids, list):
            for node_id in node_ids:
                self.graph.nodes[node_id]['state'] = state_name
        else:
            self.graph.nodes[node_ids]['state'] = state_name

    def get_state(self, node_id):
        return self.graph.nodes[node_id]['state']

    def get_nx_graph(self):
        return self.graph
    
    def random_node(self, state_name=None):
        """Returns a random node from the graph, optionally filtering by state."""
        if state_name is None:
            return random.choice(list(self.graph.nodes))
        else:
            filtered_nodes = [n for n in self.graph.nodes if self.graph.nodes[n]['state'] == state_name]
            return random.choice(filtered_nodes) if filtered_nodes else None
    
    def __getattr__(self, name):
        try:
            return getattr(self.graph, name)
        except AttributeError:
            if hasattr(nx, name):
                def wrapper(*args, **kwargs):
                    return getattr(nx, name)(self.graph, *args, **kwargs)
                return wrapper
            raise

def plot_graph_stats(graph, hist_ax, stats_ax, text_ax):
    # Clear the axis before plotting
    hist_ax.clear()

    # Plot histogram of degrees
    degrees = [d for _, d in graph.degree()]
    degree_hist = {deg: degrees.count(deg) for deg in sorted(set(degrees))}
    hist_ax.bar(degree_hist.keys(), degree_hist.values(), color='skyblue')
    hist_ax.set_title("Degree Histogram")
    hist_ax.set_xlabel("Degree")
    hist_ax.set_ylabel("Number of Nodes")

    # Plot clustering coefficient by degree as a separate subplot
    stats_ax.clear()
    from collections import defaultdict
    clustering_by_degree = defaultdict(list)
    clustering_dict = nx.clustering(graph)
    for node, c in clustering_dict.items():
        d = graph.degree[node]
        clustering_by_degree[d].append(c)
    avg_clustering_by_degree = {
        d: sum(c_list) / len(c_list) for d, c_list in clustering_by_degree.items()
    }
    # Plot average clustering coefficient for nodes grouped by their degree
    stats_ax.plot(sorted(avg_clustering_by_degree.keys()),
                  [avg_clustering_by_degree[d] for d in sorted(avg_clustering_by_degree.keys())],
                  marker='o', color='orange')
    stats_ax.set_title("Avg Clustering Coefficient by Degree")
    stats_ax.set_xlabel("Degree")
    stats_ax.set_ylabel("Avg Clustering Coefficient")

    text_ax.clear()
    text_ax.axis('off')
    stats = []
    degrees = [d for _, d in graph.degree()]
    avg_degree = sum(degrees) / len(degrees)
    avg_squared_degree = sum(d**2 for d in degrees) / len(degrees)
    avg_neighbor_degree = avg_squared_degree / avg_degree
    stats.append(f"Nodes: {graph.number_of_nodes()}")
    stats.append(f"Edges: {graph.number_of_edges()}")
    stats.append(f"Min degree: {min(degrees)}")
    stats.append(f"Max degree: {max(degrees)}")
    stats.append(f"Avg degree: {avg_degree:.2f}")
    stats.append(f"Avg squared degree: {avg_squared_degree:.2f}")
    stats.append(f"Avg neighbor degree: {avg_neighbor_degree:.2f}")
    stats.append(f"Avg clustering coeff: {nx.average_clustering(graph):.4f}")

    if nx.is_connected(graph):
        stats.append("Connected: Yes")
        stats.append(f"Diameter: {nx.diameter(graph)}")
        stats.append(f"Radius: {nx.radius(graph)}")
        stats.append(f"Avg shortest path: {nx.average_shortest_path_length(graph):.4f}")
    else:
        components = list(nx.connected_components(graph))
        stats.append("Connected: No")
        stats.append(f"Components: {len(components)}")
        stats.append(f"Largest component size: {max(len(c) for c in components)}")

    
    
    text_ax.text(-0.2, 1, "\n".join(stats), va='top', fontsize=10, family='monospace')

class Simulation:
    """Handles the simulation of state transitions over a network graph and visualizes the results."""
    def __init__(self, model, graph, num_frames=20, layout="spring", layout_seed=None, display_stats=True, show_labels=None):
        self.model = model
        self.graph = graph
        self.num_frames = num_frames
        self.frames = []  # List of dicts mapping node -> state for each frame
        self.layout = layout
        self.layout_seed = layout_seed
        self.display_stats = display_stats
        if show_labels is None:
            self.show_labels = self.graph.number_of_nodes() < 100
        else:
            self.show_labels = show_labels
        self.generate_frames()

    def generate_frames(self):
        current_graph = copy.deepcopy(self.graph)
        for _ in range(self.num_frames):
            # Snapshot of current states
            frame_state = {node: current_graph.nodes[node]['state'] for node in current_graph.nodes}
            self.frames.append(frame_state)

            # Apply transitions
            new_states = {}
            for node in current_graph.nodes:
                state = current_graph.nodes[node]['state']
                neighbors = list(current_graph.neighbors(node))
                neighbor_states = [current_graph.nodes[n]['state'] for n in neighbors]
                new_state = self.model.apply_transitions_network(state, neighbor_states)
                new_states[node] = new_state

            # Update all at once (synchronous update)
            for node in current_graph.nodes:
                current_graph.nodes[node]['state'] = new_states[node]

    def run(self):
        # === Setup plot and axes ===
        if self.display_stats:
            import matplotlib.gridspec as gridspec
            fig = plt.figure(figsize=(14, 8))
            gs = gridspec.GridSpec(1, 3, width_ratios=[2, 1, 1])
            # Only two rows in the middle column (charts), text in right column
            inner_gs = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[0, 2], hspace=0.6)
            ax = fig.add_subplot(gs[0, 0])
            hist_ax = fig.add_subplot(inner_gs[0])
            stats_ax = fig.add_subplot(inner_gs[1])
            text_ax = fig.add_subplot(gs[0, 1])
            text_ax.axis('off')
        else:
            fig, ax = plt.subplots(figsize=(8, 8))
        plt.subplots_adjust(bottom=0.3, wspace=0.3)

        # === Layout selection ===
        if self.layout_seed is None:
            self.layout_seed = 8675309

        layout_map = {
            "spring": nx.spring_layout,
            "circular": nx.circular_layout,
            "kamada_kawai": nx.kamada_kawai_layout,
            "shell": nx.shell_layout,
            "spectral": nx.spectral_layout,
            "random": nx.random_layout
        }
        layout_func = layout_map.get(self.layout, nx.spring_layout)

        # Only pass seed if the layout function accepts it
        layout_args = {}
        if 'seed' in inspect.signature(layout_func).parameters:
            layout_args['seed'] = self.layout_seed

        pos = layout_func(self.graph, **layout_args)

        self.frame_idx = [0]  # Mutable container

        # === Draw initial graph ===
        nodes = nx.draw_networkx_nodes(
            self.graph, pos, ax=ax,
            node_color=[self.model.state_colors[self.frames[0][n]] for n in self.graph.nodes],
            node_size=300 if self.show_labels else max(10000 // self.graph.number_of_nodes(), 20)
        )
        nx.draw_networkx_edges(self.graph, pos, ax=ax)
        if self.show_labels:
            nx.draw_networkx_labels(
                self.graph,
                pos,
                ax=ax,
                labels={n: str(n) for n in self.graph.nodes},
                font_color='white',
                font_weight='bold'
            )

        if self.display_stats:
            plot_graph_stats(self.graph, hist_ax, stats_ax, text_ax)

        # === Update function to refresh node colors and slider label ===
        def update():
            new_colors = [self.model.state_colors[self.frames[self.frame_idx[0]][n]] for n in self.graph.nodes]
            nodes.set_color(new_colors)
            frame_slider.valtext.set_text(f"{self.frame_idx[0] + 1}/{self.num_frames}")
            # --- Dynamic state counts appended to stats ---
            if self.display_stats:
                # Compute current state counts
                current_state_counts = {state.name: 0 for state in self.model.states}
                for n in self.graph.nodes:
                    current_state_counts[self.frames[self.frame_idx[0]][n]] += 1
                count_lines = [f"{state}: {count}" for state, count in current_state_counts.items()]
                # Use a persistent text object for stats
                if not hasattr(self, "_stats_text"):
                    self._stats_text = text_ax.text(0, 0.4, "", va='top', fontsize=10, family='monospace')

                existing_text = self._stats_text.get_text()
                split_index = existing_text.find("\n\nCurrent States:\n")
                base_text = existing_text if split_index == -1 else existing_text[:split_index]
                state_block = "Current States:\n" + "\n".join(count_lines)
                self._stats_text.set_text(base_text + "\n\n" + state_block)
            fig.canvas.draw_idle()

        # === Slider and Buttons positioning ===
        if self.display_stats:
            slider_ax = fig.add_axes([0.2, 0.18, 0.6, 0.03])
            play_ax = fig.add_axes([0.1, 0.08, 0.2, 0.05])
            stop_ax = fig.add_axes([0.35, 0.08, 0.2, 0.05])
            reset_ax = fig.add_axes([0.6, 0.08, 0.2, 0.05])
        else:
            slider_ax = plt.axes([0.2, 0.15, 0.6, 0.03])
            play_ax = plt.axes([0.1, 0.05, 0.2, 0.05])
            stop_ax = plt.axes([0.35, 0.05, 0.2, 0.05])
            reset_ax = plt.axes([0.6, 0.05, 0.2, 0.05])

        frame_slider = Slider(
            ax=slider_ax,
            label='Frame',
            valmin=0,
            valmax=self.num_frames - 1,
            valinit=0,
            valstep=1
        )

        play_button = Button(play_ax, 'Play')
        stop_button = Button(stop_ax, 'Stop')
        reset_button = Button(reset_ax, 'Reset')

        # === Timer for animation ===
        timer = fig.canvas.new_timer(interval=1000)
        is_playing = [False]  # mutable container so inner functions can modify

        # Advance frame during playback
        def advance_frame(*args):
            if self.frame_idx[0] < self.num_frames - 1:
                self.frame_idx[0] += 1
                frame_slider.set_val(self.frame_idx[0])  # triggers update
            else:
                # Stop playback when last frame is reached
                is_playing[0] = False
                timer.stop()

        # Update frame when slider is moved
        def on_slider_change(val):
            self.frame_idx[0] = int(val)
            update()

        # Start playback
        def on_play(event):
            if not is_playing[0]:
                is_playing[0] = True
                timer.start()

        # Reset simulation to first frame and stop playback
        def on_reset(event):
            timer.stop()
            is_playing[0] = False
            self.frame_idx[0] = 0
            frame_slider.set_val(0)  # triggers update

        # Stop playback without resetting
        def on_stop(event):
            timer.stop()
            is_playing[0] = False

        timer.add_callback(advance_frame)
        frame_slider.on_changed(on_slider_change)
        play_button.on_clicked(on_play)
        stop_button.on_clicked(on_stop)
        reset_button.on_clicked(on_reset)

        update()
        plt.show()

def run_simulation(model, network, num_frames=100, layout="spring", layout_seed=None, display_stats=False, show_labels=None):
    # Extract networkx graph and preserve node states if using custom Network object
    if isinstance(network, Network):
        raw_graph = network.graph
    else:
        raw_graph = network

    # Assign initial states and create color mapping for visualization
    model.state_colors = {state.name: tuple(c/255 for c in state.color) for state in model.states}

    # Ensure every node has a 'state' attribute; default to "Susceptible"
    for node in raw_graph.nodes:
        if 'state' not in raw_graph.nodes[node]:
            raw_graph.nodes[node]['state'] = "Susceptible"

    # Add method to apply transitions in network mode
    def apply_transitions_network(state_name, neighbor_state_names):
        # Iterate over all transitions to find applicable rules for current state
        for t in model.transitions:
            if t.from_state.name != state_name:
                continue
            if t.requires_proximity:
                # Transition only applies if any neighbor has the required contact state
                if any(ns == t.contact_with.name for ns in neighbor_state_names):
                    if random.random() <= t.probability:
                        return t.to_state.name
            else:
                # Transition applies without proximity requirement based on probability
                if random.random() <= t.probability:
                    return t.to_state.name
        # No transition applied; remain in current state
        return state_name

    model.apply_transitions_network = apply_transitions_network
    sim = Simulation(model, raw_graph, num_frames, layout, layout_seed, display_stats=display_stats, show_labels=show_labels)
    if display_stats:
        # The stats panel is drawn inside Simulation.run(), no additional call needed here
        pass
    sim.run()