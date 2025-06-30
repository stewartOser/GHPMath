import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button, Slider
import random
import copy

# Define core model structure
class Model:
    def __init__(self, name="Generic Model"):
        self.name = name
        self.states = []
        self.transitions = []

    def add_state(self, name, color, number=0):
        state = State(name, color, number)
        self.states.append(state)
        return state

    def add_transition(self, from_state, to_state, probability,
                       requires_proximity=False, contact_with=None):
        t = Transition(from_state, to_state, probability,
                       requires_proximity, contact_with)
        self.transitions.append(t)

class State:
    def __init__(self, name, color, number=0):
        self.name = name
        self.color = color  # RGB tuple (0–255)
        self.number = number


class Transition:
    def __init__(self, from_state, to_state, probability,
                 requires_proximity=False, contact_with=None):
        self.from_state = from_state
        self.to_state = to_state
        self.probability = probability
        self.requires_proximity = requires_proximity
        self.contact_with = contact_with


# === Network abstraction ===
class Network:
    def __init__(self, model):
        self.model = model
        self.graph = nx.Graph()

    def add_node(self, node_id, state_name):
        self.graph.add_node(node_id)
        self.graph.nodes[node_id]['state'] = state_name

    def add_nodes(self, count, state_name, start_id=0):
        for i in range(start_id, start_id + count):
            self.add_node(i, state_name)

    def add_edges(self, *edges):
        self.graph.add_edges_from(edges)

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

class Simulation:
    def __init__(self, model, graph, num_frames=20):
        self.model = model
        self.graph = graph
        self.num_frames = num_frames
        self.frames = []  # List of dicts mapping node -> state for each frame
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
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3)

        pos = nx.circular_layout(self.graph)
        self.frame_idx = [0]  # Mutable container

        nodes = nx.draw_networkx_nodes(
            self.graph, pos, ax=ax,
            node_color=[self.model.state_colors[self.frames[0][n]] for n in self.graph.nodes]
        )
        nx.draw_networkx_edges(self.graph, pos, ax=ax)
        nx.draw_networkx_labels(
            self.graph,
            pos,
            ax=ax,
            labels={n: str(n) for n in self.graph.nodes},
            font_color='white',
            font_weight='bold'
        )

        def update():
            new_colors = [self.model.state_colors[self.frames[self.frame_idx[0]][n]] for n in self.graph.nodes]
            nodes.set_color(new_colors)
            frame_slider.valtext.set_text(f"{self.frame_idx[0] + 1}/{self.num_frames}")
            fig.canvas.draw_idle()

        # === Slider ===
        slider_ax = plt.axes([0.2, 0.15, 0.6, 0.03])
        frame_slider = Slider(
            ax=slider_ax,
            label='Frame',
            valmin=0,
            valmax=self.num_frames - 1,
            valinit=0,
            valstep=1
        )

        # === Buttons ===
        play_ax = plt.axes([0.1, 0.05, 0.2, 0.05])
        stop_ax = plt.axes([0.35, 0.05, 0.2, 0.05])
        reset_ax = plt.axes([0.6, 0.05, 0.2, 0.05])
        play_button = Button(play_ax, 'Play')
        stop_button = Button(stop_ax, 'Stop')
        reset_button = Button(reset_ax, 'Reset')

        # === Timer ===
        timer = fig.canvas.new_timer(interval=1000)
        is_playing = [False]  # mutable container so inner functions can modify

        def advance_frame(*args):
            if self.frame_idx[0] < self.num_frames - 1:
                self.frame_idx[0] += 1
                frame_slider.set_val(self.frame_idx[0])  # triggers update
            else:
                is_playing[0] = False
                timer.stop()

        def on_slider_change(val):
            self.frame_idx[0] = int(val)
            update()

        def on_play(event):
            if not is_playing[0]:
                is_playing[0] = True
                timer.start()

        def on_reset(event):
            timer.stop()
            is_playing[0] = False
            self.frame_idx[0] = 0
            frame_slider.set_val(0)  # triggers update

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

def run_simulation(model, network, num_frames=100):
    network = network.get_nx_graph()
    # Assign initial states
    model.state_colors = {state.name: tuple(c/255 for c in state.color) for state in model.states}

    # Add method to apply transitions in network mode
    def apply_transitions_network(state_name, neighbor_state_names):
        for t in model.transitions:
            if t.from_state.name != state_name:
                continue
            if t.requires_proximity:
                if any(ns == t.contact_with.name for ns in neighbor_state_names):
                    if random.random() <= t.probability:
                        return t.to_state.name
            else:
                if random.random() <= t.probability:
                    return t.to_state.name
        return state_name

    model.apply_transitions_network = apply_transitions_network

    sim = Simulation(model, network, num_frames)
    sim.run()