import matplotlib.pyplot as plt
import networkx as nx


class Visualizer:
    @staticmethod
    def plot_graph(graph, tsp_path=None, title="Network Graph"):
        pos = nx.get_node_attributes(graph, 'pos')
        plt.figure(figsize=(12, 10))
        nx.draw(graph, pos, with_labels=True, node_size=700, font_size=9, edge_color='gray')

        if tsp_path:
            tsp_edges = list(zip(tsp_path, tsp_path[1:]))
            for i, edge in enumerate(tsp_edges):
                nx.draw_networkx_edges(graph, pos, edgelist=[edge], edge_color='blue', width=2)
                mid_point = ((pos[edge[0]][0] + pos[edge[1]][0]) / 2, (pos[edge[0]][1] + pos[edge[1]][1]) / 2)
                plt.text(mid_point[0], mid_point[1], graph[edge[0]][edge[1]].get("mode", ""), color='red', fontsize=10)

        plt.title(title)
        plt.show()
