from typing import Annotated

from fastapi import Depends
import polars as pl
from graphviz import Digraph
import networkx as nx


def get_data() -> pl.DataFrame:
    return pl.read_csv("static/digimon_tree.csv")


def get_identities(data: Annotated[pl.DataFrame, Depends(get_data)]) -> pl.DataFrame:
    return data.filter(data["名前"].is_not_null())


def get_evolutions(data: Annotated[pl.DataFrame, Depends(get_data)]) -> pl.DataFrame:
    return (
        data.lazy()
        .with_columns(
            pl.col("名前").fill_null(strategy="forward"),
            pl.col("進化").fill_null(strategy="forward"),
        )
        .filter(pl.col("進化").is_not_null())
        .filter(pl.col("進化") != "-")
        .select(["名前", "進化"])
        .collect()
    )


def render(
    identities: Annotated[pl.DataFrame, Depends(get_identities)],
    evolutions: Annotated[pl.DataFrame, Depends(get_evolutions)],
) -> Digraph:
    dot = Digraph()
    for identity in identities.select(["名前"]).iter_rows():
        dot.node(identity[0])
    for evolution in evolutions.iter_rows():
        dot.edge(evolution[0], evolution[1])
    dot.render("static/all_tree", format="png", cleanup=True)
    return "/static/all_tree.png"


def render_selected(
    start: str,
    dest: str,
    evolutions: Annotated[pl.DataFrame, Depends(get_evolutions)],
) -> str:
    G = nx.Graph()
    G.add_edges_from([(row[0], row[1]) for row in evolutions.iter_rows()])

    nodes = nx.shortest_path(G, source=start, target=dest)

    dot = Digraph()
    for node in nodes:
        dot.node(node)
    for i in range(len(nodes) - 1):
        dot.edge(nodes[i], nodes[i + 1])

    dot.render("static/selected_tree", format="png", cleanup=True)
    return "static/selected_tree.png"
