"""Construcción de grafos y búsqueda de caminos mínimos."""

from __future__ import annotations

import heapq
import math


DEFAULT_EDGES = [
    ("Centro", "Norte", 4.0),
    ("Centro", "Sur", 3.0),
    ("Centro", "Este", 6.0),
    ("Norte", "Oeste", 5.0),
    ("Norte", "Este", 2.0),
    ("Sur", "Oeste", 4.0),
    ("Sur", "Puerto", 7.0),
    ("Oeste", "Puerto", 3.0),
    ("Este", "Puerto", 5.0),
    ("Este", "Aeropuerto", 4.0),
    ("Puerto", "Aeropuerto", 6.0),
]


def build_graph(edges: list[tuple[str, str, float]]) -> dict[str, list[tuple[str, float]]]:
    graph: dict[str, list[tuple[str, float]]] = {}
    seen_edges: set[frozenset[str]] = set()
    for origin, destination, distance in edges:
        origin, destination = origin.strip(), destination.strip()
        distance = float(distance)
        if not origin or not destination:
            raise ValueError("Cada tramo debe tener origen y destino.")
        if origin == destination:
            raise ValueError("Un tramo no puede conectar un nodo consigo mismo.")
        if not math.isfinite(distance) or distance < 0:
            raise ValueError("Las distancias no pueden ser negativas.")
        edge_key = frozenset((origin, destination))
        if edge_key in seen_edges:
            raise ValueError(f"El tramo {origin} ↔ {destination} está repetido.")
        seen_edges.add(edge_key)
        graph.setdefault(origin, []).append((destination, distance))
        graph.setdefault(destination, []).append((origin, distance))
    if not graph:
        raise ValueError("Agrega al menos un tramo al grafo.")
    return graph


def shortest_path(
    graph: dict[str, list[tuple[str, float]]], start: str, goal: str
) -> tuple[list[str], float] | None:
    """Devuelve la ruta y distancia mínima usando Dijkstra."""
    if start not in graph or goal not in graph:
        raise ValueError("El origen y el destino deben existir en el grafo.")
    distances = {node: float("inf") for node in graph}
    previous: dict[str, str] = {}
    distances[start] = 0.0
    queue = [(0.0, start)]
    while queue:
        distance, node = heapq.heappop(queue)
        if distance > distances[node]:
            continue
        if node == goal:
            break
        for neighbor, weight in graph[node]:
            candidate = distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = node
                heapq.heappush(queue, (candidate, neighbor))
    if distances[goal] == float("inf"):
        return None
    path = [goal]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return path, distances[goal]
