"""Interfaz Streamlit para editar un grafo y encontrar rutas mínimas."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st

from backend import DEFAULT_EDGES, build_graph, shortest_path


st.set_page_config(page_title="Optimizador de rutas", page_icon="🗺️", layout="wide")
st.title("Optimizador de rutas con grafos")
st.write("Edita los tramos y encuentra el camino de menor distancia entre dos puntos.")

edge_frame = pd.DataFrame(DEFAULT_EDGES, columns=["origen", "destino", "distancia"])
edge_frame["distancia"] = edge_frame["distancia"].astype(float)
st.subheader("Tramos del grafo")
edited_edges = st.data_editor(
    edge_frame,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={"distancia": st.column_config.NumberColumn("distancia", min_value=0.0, step=0.5)},
)

try:
    edges = [
        (str(row.origen), str(row.destino), float(row.distancia))
        for row in edited_edges.dropna().itertuples(index=False)
    ]
    graph = build_graph(edges)
except (ValueError, TypeError) as error:
    st.error(str(error))
    st.stop()

nodes = sorted(graph)
controls = st.columns([1, 1, 2])
start = controls[0].selectbox("Origen", nodes, index=nodes.index("Centro") if "Centro" in nodes else 0)
goal_options = [node for node in nodes if node != start] or nodes
goal_default = "Aeropuerto" if "Aeropuerto" in goal_options else goal_options[-1]
goal = controls[1].selectbox("Destino", goal_options, index=goal_options.index(goal_default))
route_result = shortest_path(graph, start, goal)

if route_result is None:
    st.warning(f"No existe una ruta entre {start} y {goal}.")
    path = []
else:
    path, distance = route_result
    st.success(f"Ruta mínima: {' → '.join(path)}  ·  Distancia total: {distance:g}")

network = nx.Graph()
for origin, neighbors in graph.items():
    for destination, distance in neighbors:
        network.add_edge(origin, destination, weight=distance)
positions = nx.spring_layout(network, seed=17, k=1.2)
route_edges = set(zip(path, path[1:])) | set((b, a) for a, b in zip(path, path[1:]))
fig, axis = plt.subplots(figsize=(10, 6))
nx.draw_networkx_edges(network, positions, ax=axis, edge_color="#aab2bd", width=1.5)
if route_edges:
    nx.draw_networkx_edges(network, positions, edgelist=list(route_edges), ax=axis,
                           edge_color="#e74c3c", width=4)
nx.draw_networkx_nodes(network, positions, ax=axis, node_color="#5dade2", node_size=1500)
if path:
    nx.draw_networkx_nodes(network, positions, nodelist=path, ax=axis,
                           node_color="#f5b041", node_size=1500)
nx.draw_networkx_labels(network, positions, ax=axis, font_size=9)
nx.draw_networkx_edge_labels(
    network, positions, edge_labels=nx.get_edge_attributes(network, "weight"), ax=axis
)
axis.set_title("Ruta resaltada en rojo/naranja")
axis.axis("off")
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

with st.expander("Tramos disponibles"):
    st.dataframe(pd.DataFrame(edges, columns=["origen", "destino", "distancia"]),
                 use_container_width=True, hide_index=True)
