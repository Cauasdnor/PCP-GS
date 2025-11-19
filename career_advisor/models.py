"""Core data models for the career advisor application."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Tuple


@dataclass
class Competency:
    """Represents a technical or behavioral competency."""

    name: str
    kind: str  # "tecnica" or "comportamental"
    score: float

    def __post_init__(self) -> None:
        self.kind = self.kind.lower()
        if self.kind not in {"tecnica", "comportamental"}:
            raise ValueError(
                "Tipo de competência deve ser 'tecnica' ou 'comportamental'."
            )
        if not 0 <= self.score <= 10:
            raise ValueError("A nota da competência deve estar entre 0 e 10.")


@dataclass
class Profile:
    """Represents a professional profile with competencies."""

    name: str
    technical_skills: Dict[str, Competency] = field(default_factory=dict)
    behavioral_skills: Dict[str, Competency] = field(default_factory=dict)

    def add_competency(self, competency: Competency) -> None:
        bucket = (
            self.technical_skills if competency.kind == "tecnica" else self.behavioral_skills
        )
        bucket[competency.name.lower()] = competency

    def list_competencies(self) -> List[Competency]:
        return list(self.technical_skills.values()) + list(self.behavioral_skills.values())

    def get_score(self, name: str) -> float:
        key = name.lower()
        if key in self.technical_skills:
            return self.technical_skills[key].score
        if key in self.behavioral_skills:
            return self.behavioral_skills[key].score
        return 0.0


@dataclass
class Career:
    """Represents a possible future career with required competencies."""

    name: str
    required_competencies: Dict[str, Tuple[str, float]]

    def required_items(self) -> Iterable[Tuple[str, str, float]]:
        for comp_name, (kind, score) in self.required_competencies.items():
            yield comp_name, kind, score
