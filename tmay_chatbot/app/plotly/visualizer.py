import logging

import numpy as np
import plotly.graph_objects as go
from sklearn.manifold import TSNE

from tmay_chatbot.app.base import PlotlyApp
from tmay_chatbot.core.context_repository.factory import get_context_repository
from tmay_chatbot.core.context_repository.repository import ContextRepository
from tmay_chatbot.core.knowledge_base import get_repository
from tmay_chatbot.core.knowledge_base.repository import KnowledgeBaseRepository

logger = logging.getLogger(__name__)

DOC_TYPE_COLOR_PALETTE = [
    "royalblue",
    "chocolate",
    "mediumseagreen",
    "goldenrod",
    "palevioletred",
    "green",
    "slateblue",
    "indianred",
    "gray",
    "brown",
]


class DataVisualizerApp(PlotlyApp):
    def __init__(
        self,
        context_repository: ContextRepository,
        knowledge_base_repository: KnowledgeBaseRepository,
    ):
        self.context_repository = context_repository
        self.knowledge_base_repository = knowledge_base_repository

    def _load_vectors(self):
        documents = self.context_repository.fetch_all()

        self.vectors = np.array([document.embedding for document in documents])
        self.documents = np.array([document.content for document in documents])
        self.doc_types = np.array([document.metadata["doc_type"] for document in documents])

        doc_type_names = self.knowledge_base_repository.fetch_doc_types()
        self.doc_type_colors = {
            doc_type: DOC_TYPE_COLOR_PALETTE[i % len(DOC_TYPE_COLOR_PALETTE)]
            for i, doc_type in enumerate(doc_type_names)
        }
        logger.info(f"Doc type colors: {self.doc_type_colors}")

    def _run_tsne(self, n_components: int):
        logger.info(f"Running t-SNE ({n_components}D)")
        tsne = TSNE(n_components=n_components, random_state=42)
        return tsne.fit_transform(self.vectors)

    def _build_figure(self, reduced_vectors, dimensions: int):
        scatter_cls = go.Scatter3d if dimensions == 3 else go.Scatter
        fig = go.Figure()
        for doc_type in sorted(set(self.doc_types)):
            mask = self.doc_types == doc_type
            coords = {axis: reduced_vectors[mask, i] for i, axis in enumerate("xyz"[:dimensions])}
            fig.add_trace(
                scatter_cls(
                    **coords,
                    mode="markers",
                    name=doc_type,
                    marker={"size": 5, "color": self.doc_type_colors[doc_type], "opacity": 0.8},
                    text=[f"Type: {doc_type}<br>Text: {d[:100]}..." for d in self.documents[mask]],
                    hoverinfo="text",
                )
            )
        return fig

    def display_2d(self):
        reduced_vectors = self._run_tsne(2)
        fig = self._build_figure(reduced_vectors, dimensions=2)
        fig.update_layout(
            title="2D Chroma Vector Store Visualization",
            xaxis_title="x",
            yaxis_title="y",
            width=800,
            height=600,
            margin={"r": 20, "b": 10, "l": 10, "t": 40},
        )
        logger.info("Rendering 2D figure")
        fig.show()

    def display_3d(self):
        reduced_vectors = self._run_tsne(3)
        fig = self._build_figure(reduced_vectors, dimensions=3)
        fig.update_layout(
            title="3D Chroma Vector Store Visualization",
            scene={"xaxis_title": "x", "yaxis_title": "y", "zaxis_title": "z"},
            width=900,
            height=700,
            margin={"r": 10, "b": 10, "l": 10, "t": 40},
        )
        logger.info("Rendering 3D figure")
        fig.show()

    def run_hook(self, *args, **kwargs) -> None:
        self._load_vectors()
        self.display_2d()
        self.display_3d()


if __name__ == "__main__":
    DataVisualizerApp(
        context_repository=get_context_repository(),
        knowledge_base_repository=get_repository(),
    ).run()
