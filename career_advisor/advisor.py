"""Business logic for the career advisor system."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from models import Career, Competency, Profile


@dataclass
class Recommendation:
    """Represents a recommendation result for a profile."""

    profile: Profile
    career: Career
    match_percentage: float
    missing_competencies: Dict[str, float]


class CareerAdvisor:
    """Facade that keeps track of profiles, competencies and careers."""

    def __init__(self) -> None:
        self.profiles: Dict[str, Profile] = {}
        self.careers: Dict[str, Career] = {}

    # -- Profiles -----------------------------------------------------------------
    def add_profile(self, profile: Profile) -> None:
        self.profiles[profile.name.lower()] = profile

    def get_profile(self, name: str) -> Optional[Profile]:
        return self.profiles.get(name.lower())

    # -- Careers ------------------------------------------------------------------
    def add_career(self, career: Career) -> None:
        self.careers[career.name.lower()] = career

    def list_careers(self) -> List[Career]:
        return list(self.careers.values())

    # -- Competencies -------------------------------------------------------------
    def add_competency_to_profile(
        self, profile_name: str, competency: Competency
    ) -> Profile:
        profile = self.profiles.setdefault(profile_name.lower(), Profile(profile_name))
        profile.add_competency(competency)
        return profile

    # -- Analysis -----------------------------------------------------------------
    def analyze_profile(self, profile: Profile) -> List[Recommendation]:
        results: List[Recommendation] = []
        for career in self.careers.values():
            missing: Dict[str, float] = {}
            total = 0
            achieved = 0
            for comp_name, kind, required_score in career.required_items():
                total += required_score
                current_score = profile.get_score(comp_name)
                achieved += min(current_score, required_score)
                if current_score < required_score:
                    missing[comp_name] = required_score - current_score
            match = (achieved / total * 100) if total else 0
            results.append(
                Recommendation(
                    profile=profile,
                    career=career,
                    match_percentage=round(match, 2),
                    missing_competencies=missing,
                )
            )
        results.sort(key=lambda rec: rec.match_percentage, reverse=True)
        return results

    def suggest_improvements(self, recommendation: Recommendation) -> List[str]:
        suggestions: List[str] = []
        for comp_name, missing_value in recommendation.missing_competencies.items():
            suggestions.append(
                f"Aumentar {comp_name} em {missing_value:.1f} pontos para a carreira de {recommendation.career.name}."
            )
        if not suggestions:
            suggestions.append("Perfil já atende aos requisitos dessa carreira!")
        return suggestions


def build_default_advisor() -> CareerAdvisor:
    """Creates an advisor preloaded with common careers."""

    advisor = CareerAdvisor()
    technical_skills = {
        "python": ("tecnica", 9),
        "estatistica aplicada": ("tecnica", 8),
        "machine learning": ("tecnica", 9),
        "deep learning": ("tecnica", 8),
        "sql": ("tecnica", 8),
        "bancos nosql": ("tecnica", 7),
        "data visualization": ("tecnica", 7),
        "power bi": ("tecnica", 6),
        "spark": ("tecnica", 7),
        "hadoop": ("tecnica", 6),
        "big data architecture": ("tecnica", 8),
        "cloud architecture": ("tecnica", 9),
        "kubernetes": ("tecnica", 8),
        "docker": ("tecnica", 8),
        "linux administration": ("tecnica", 7),
        "redes corporativas": ("tecnica", 7),
        "seguranca redes": ("tecnica", 9),
        "criptografia aplicada": ("tecnica", 8),
        "automacao testes": ("tecnica", 7),
        "desenvolvimento backend": ("tecnica", 8),
        "desenvolvimento frontend": ("tecnica", 7),
        "desenvolvimento mobile": ("tecnica", 7),
        "devops": ("tecnica", 9),
        "ci cd": ("tecnica", 8),
        "infraestrutura como codigo": ("tecnica", 8),
        "terraform": ("tecnica", 7),
        "ansible": ("tecnica", 6),
        "monitoramento observabilidade": ("tecnica", 7),
        "testes automatizados api": ("tecnica", 7),
        "sistemas embarcados": ("tecnica", 6),
        "robotica": ("tecnica", 6),
        "iot": ("tecnica", 7),
        "analise de logs": ("tecnica", 6),
        "programacao funcional": ("tecnica", 7),
        "java": ("tecnica", 7),
        "csharp": ("tecnica", 7),
        "go": ("tecnica", 6),
        "rust": ("tecnica", 6),
        "nodejs": ("tecnica", 7),
        "react": ("tecnica", 7),
        "flutter": ("tecnica", 6),
        "swift": ("tecnica", 6),
        "power platform": ("tecnica", 6),
        "integracao sistemas": ("tecnica", 7),
        "arquitetura microservicos": ("tecnica", 8),
        "modelagem dados": ("tecnica", 8),
        "governanca dados": ("tecnica", 7),
        "analise preditiva": ("tecnica", 8),
        "processamento linguagem natural": ("tecnica", 8),
        "visao computacional": ("tecnica", 8),
        "realidade aumentada": ("tecnica", 6),
        "simulacao digital": ("tecnica", 6),
    }
    behavioral_skills = {
        "comunicacao": ("comportamental", 8),
        "storytelling": ("comportamental", 7),
        "pensamento critico": ("comportamental", 8),
        "resolucao de problemas": ("comportamental", 9),
        "colaboracao": ("comportamental", 8),
        "lideranca": ("comportamental", 8),
        "negociacao": ("comportamental", 7),
        "empatia": ("comportamental", 8),
        "adaptabilidade": ("comportamental", 8),
        "criatividade": ("comportamental", 8),
        "proatividade": ("comportamental", 8),
        "gestao do tempo": ("comportamental", 7),
        "gestao de conflitos": ("comportamental", 7),
        "tomada de decisao": ("comportamental", 8),
        "foco no cliente": ("comportamental", 8),
        "orientacao a resultados": ("comportamental", 8),
        "organizacao": ("comportamental", 7),
        "detalhismo": ("comportamental", 7),
        "resiliencia": ("comportamental", 8),
        "inteligencia emocional": ("comportamental", 9),
        "visao estrategica": ("comportamental", 8),
        "mentoria": ("comportamental", 7),
        "aprendizado continuo": ("comportamental", 8),
        "curiosidade": ("comportamental", 7),
        "networking": ("comportamental", 6),
        "responsabilidade": ("comportamental", 8),
        "confiabilidade": ("comportamental", 8),
        "influencia": ("comportamental", 7),
        "coachabilidade": ("comportamental", 7),
        "etica profissional": ("comportamental", 9),
        "diplomacia": ("comportamental", 7),
        "paciencia": ("comportamental", 7),
        "autocontrole": ("comportamental", 8),
        "pensamento sistemico": ("comportamental", 8),
        "planejamento": ("comportamental", 7),
        "capacidade analitica": ("comportamental", 8),
        "iniciativa": ("comportamental", 8),
        "senso de urgencia": ("comportamental", 7),
        "colaboracao remota": ("comportamental", 7),
        "abertura a feedbacks": ("comportamental", 8),
        "comunicacao escrita": ("comportamental", 7),
        "comunicacao visual": ("comportamental", 6),
        "apresentacao": ("comportamental", 7),
        "facilitacao de workshops": ("comportamental", 7),
        "gestao de stakeholders": ("comportamental", 8),
        "mediacao": ("comportamental", 6),
        "escuta ativa": ("comportamental", 8),
        "motivacao de equipes": ("comportamental", 8),
        "foco na qualidade": ("comportamental", 8),
        "orientacao a dados": ("comportamental", 7),
        "gestao de riscos": ("comportamental", 7),
        "pensamento empreendedor": ("comportamental", 7),
    }
    skills_catalog = {**technical_skills, **behavioral_skills}

    careers_data = [
        (
            "Cientista de Dados",
            [
                "python",
                "estatistica aplicada",
                "machine learning",
                "data visualization",
                "pensamento critico",
                "comunicacao",
                "orientacao a dados",
            ],
        ),
        (
            "Arquiteto de Soluções em Nuvem",
            [
                "cloud architecture",
                "arquitetura microservicos",
                "kubernetes",
                "infraestrutura como codigo",
                "lideranca",
                "negociacao",
                "visao estrategica",
            ],
        ),
        (
            "Especialista em Cibersegurança",
            [
                "seguranca redes",
                "criptografia aplicada",
                "linux administration",
                "resolucao de problemas",
                "detalhismo",
                "etica profissional",
            ],
        ),
        (
            "Engenheiro de Machine Learning",
            [
                "python",
                "machine learning",
                "deep learning",
                "analise preditiva",
                "processamento linguagem natural",
                "aprendizado continuo",
                "orientacao a resultados",
            ],
        ),
        (
            "Engenheiro de Dados",
            [
                "sql",
                "modelagem dados",
                "hadoop",
                "spark",
                "governanca dados",
                "comunicacao",
                "planejamento",
            ],
        ),
        (
            "Analista de Business Intelligence",
            [
                "power bi",
                "data visualization",
                "sql",
                "storytelling",
                "comunicacao",
                "foco no cliente",
            ],
        ),
        (
            "Engenheiro DevOps",
            [
                "devops",
                "ci cd",
                "kubernetes",
                "docker",
                "monitoramento observabilidade",
                "colaboracao",
                "proatividade",
                "gestao de riscos",
            ],
        ),
        (
            "Engenheiro de Software Backend",
            [
                "desenvolvimento backend",
                "java",
                "modelagem dados",
                "testes automatizados api",
                "resolucao de problemas",
                "comunicacao escrita",
            ],
        ),
        (
            "Desenvolvedor Full Stack",
            [
                "desenvolvimento frontend",
                "desenvolvimento backend",
                "react",
                "nodejs",
                "comunicacao",
                "adaptabilidade",
                "organizacao",
            ],
        ),
        (
            "Engenheiro Mobile",
            [
                "desenvolvimento mobile",
                "flutter",
                "swift",
                "react",
                "criatividade",
                "senso de urgencia",
                "comunicacao visual",
            ],
        ),
        (
            "Product Manager Digital",
            [
                "data visualization",
                "visao estrategica",
                "gestao de stakeholders",
                "comunicacao",
                "negociacao",
                "orientacao a resultados",
                "planejamento",
            ],
        ),
        (
            "Scrum Master",
            [
                "integracao sistemas",
                "facilitacao de workshops",
                "colaboracao",
                "mediacao",
                "gestao do tempo",
                "adaptabilidade",
                "abertura a feedbacks",
            ],
        ),
        (
            "UX Researcher",
            [
                "data visualization",
                "empatia",
                "escuta ativa",
                "storytelling",
                "curiosidade",
                "pensamento critico",
            ],
        ),
        (
            "UI Designer",
            [
                "desenvolvimento frontend",
                "comunicacao visual",
                "criatividade",
                "detalhismo",
                "colaboracao",
                "orientacao a resultados",
            ],
        ),
        (
            "Analista de Suporte N2",
            [
                "redes corporativas",
                "linux administration",
                "analise de logs",
                "comunicacao",
                "paciencia",
                "responsabilidade",
            ],
        ),
        (
            "Engenheiro de Redes",
            [
                "redes corporativas",
                "seguranca redes",
                "monitoramento observabilidade",
                "infraestrutura como codigo",
                "comunicacao",
                "gestao de riscos",
            ],
        ),
        (
            "Especialista em Observabilidade",
            [
                "monitoramento observabilidade",
                "analise de logs",
                "automacao testes",
                "comunicacao escrita",
                "pensamento sistemico",
                "orientacao a dados",
            ],
        ),
        (
            "Arquiteto de Microserviços",
            [
                "arquitetura microservicos",
                "desenvolvimento backend",
                "nodejs",
                "kubernetes",
                "lideranca",
                "negociacao",
                "planejamento",
            ],
        ),
        (
            "Engenheiro de IoT",
            [
                "iot",
                "redes corporativas",
                "sistemas embarcados",
                "robotica",
                "resolucao de problemas",
                "criatividade",
                "curiosidade",
            ],
        ),
        (
            "Cientista de Visão Computacional",
            [
                "visao computacional",
                "python",
                "deep learning",
                "analise preditiva",
                "comunicacao",
                "pensamento critico",
            ],
        ),
        (
            "Especialista em Processamento de Linguagem Natural",
            [
                "processamento linguagem natural",
                "python",
                "machine learning",
                "storytelling",
                "comunicacao",
                "orientacao a dados",
                "criatividade",
            ],
        ),
        (
            "Consultor de Transformação Digital",
            [
                "cloud architecture",
                "integracao sistemas",
                "power platform",
                "visao estrategica",
                "comunicacao",
                "orientacao a resultados",
                "gestao de stakeholders",
            ],
        ),
        (
            "Analista de Governança de Dados",
            [
                "governanca dados",
                "modelagem dados",
                "data visualization",
                "comunicacao",
                "etica profissional",
                "orientacao a dados",
                "planejamento",
            ],
        ),
        (
            "Especialista em Automação Industrial",
            [
                "automacao testes",
                "sistemas embarcados",
                "robotica",
                "iot",
                "proatividade",
                "responsabilidade",
                "detalhismo",
            ],
        ),
        (
            "Engenheiro de Segurança Aplicada",
            [
                "seguranca redes",
                "criptografia aplicada",
                "desenvolvimento backend",
                "testes automatizados api",
                "resolucao de problemas",
                "orientacao a resultados",
                "etica profissional",
            ],
        ),
        (
            "Agile Coach",
            [
                "devops",
                "facilitacao de workshops",
                "lideranca",
                "mentoria",
                "aprendizado continuo",
                "empatia",
                "planejamento",
                "abertura a feedbacks",
            ],
        ),
        (
            "Engenheiro de Realidade Aumentada",
            [
                "realidade aumentada",
                "visao computacional",
                "desenvolvimento mobile",
                "criatividade",
                "comunicacao visual",
                "resolucao de problemas",
            ],
        ),
        (
            "Especialista em Power Platform",
            [
                "power platform",
                "integracao sistemas",
                "desenvolvimento backend",
                "comunicacao",
                "foco no cliente",
                "orientacao a resultados",
                "planejamento",
            ],
        ),
    ]

    for name, competencies in careers_data:
        advisor.add_career(
            Career(
                name=name,
                required_competencies={skill: skills_catalog[skill] for skill in competencies},
            )
        )
    return advisor
