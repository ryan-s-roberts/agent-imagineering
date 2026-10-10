"""Judge schema for the explicit, user-supplied contextual-party assumption."""

from typing import Literal

from .citation_catalog import MaterializedJudgment, SelectedJudgment, materialize


class ContextSelectedJudgment(SelectedJudgment):
    version: Literal["soft-judge-v3"]
    benchmark_context_used: bool


class ContextMaterializedJudgment(MaterializedJudgment):
    version: Literal["soft-judge-v3"]
    benchmark_context_used: bool


class ContextSelectionValidator:
    def __init__(self, catalog):
        self.catalog = catalog

    def model_validate(self, data):
        selected = ContextSelectedJudgment.model_validate(data)
        try:
            materialize(selected.model_dump(), self.catalog, ContextMaterializedJudgment)
        except KeyError as error:
            raise ValueError(f"Select only allowed citation span IDs: {error}") from error
        return selected
