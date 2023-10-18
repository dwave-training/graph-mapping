# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Import networkx for graph tools
import networkx as nx

# Import dwave_networkx for d-wave graph tools/functions
import dwave_networkx as dnx

# Import dwave.system packages for the QPU
from dwave.system import DWaveSampler, EmbeddingComposite

# Import matplotlib.pyplot to draw graphs on screen
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt


# Set the solver we're going to use
def set_sampler():
    '''Returns a dimod sampler'''

    sampler = EmbeddingComposite(DWaveSampler())

    return sampler

def create_graph():
    # Create empty graph
    G = nx.Graph()

    # Add edges to graph - this also adds the nodes
    G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (3, 5), 
                        (4, 5), (4, 6), (5, 6), (6, 7)])

    return G

def solve_problem(G, sampler):
    '''Returns a solution to to the minimum vertex cover on graph G using 
    the D-Wave QPU.

    Args:
        G(networkx.Graph): a graph representing a problem
        sampler(dimod.Sampler): sampler used to find solutions

    Returns:
        A list of nodes
    '''

    # Find the maximum independent set, S
    S = dnx.maximum_independent_set(G, sampler=sampler, num_reads=10)

    return S

## ------- Main program -------
if __name__ == "__main__":

    G = create_graph()

    sampler = set_sampler()

    S = solve_problem(G, sampler)

    # Print the solution for the user
    print('Maximum independent set size found is', len(S))
    print(S)

    # Visualize the results
    subset_1 = G.subgraph(S)
    notS = list(set(G.nodes()) - set(S))
    subset_0 = G.subgraph(notS)
    pos = nx.spring_layout(G)
    plt.figure()

    # Save original problem graph
    original_name = "antenna_plot_original.png"
    nx.draw_networkx(G, pos=pos, with_labels=True)
    plt.savefig(original_name, bbox_inches='tight')

    # Save solution graph
    # Note: red nodes are in the set, blue nodes are not
    solution_name = "antenna_plot_solution.png"
    nx.draw_networkx(subset_1, pos=pos, with_labels=True, node_color='r', font_color='k')
    nx.draw_networkx(subset_0, pos=pos, with_labels=True, node_color='b', font_color='w')
    plt.savefig(solution_name, bbox_inches='tight')

    print("Your plots are saved to {} and {}".format(original_name, solution_name))
