"""Simple CLI to interact with the career advisor system."""

from __future__ import annotations

import argparse
from textwrap import dedent

from advisor import CareerAdvisor, Recommendation, build_default_advisor
from models import Competency, Profile


class CareerCLI:
    """Command-line interface for the advisor."""

    def __init__(self, advisor: CareerAdvisor) -> None:
        self.advisor = advisor

    def run(self) -> None:
        print("=== Sistema Inteligente de Orientação de Carreiras ===")
        while True:
            option = self._menu()
            if option == "1":
                self._create_profile()
            elif option == "2":
                self._add_competency()
            elif option == "3":
                self._analyze_profile()
            elif option == "4":
                self._list_careers()
            elif option == "0":
                print("Até logo!")
                break
            else:
                print("Opção inválida. Tente novamente.\n")

    def _menu(self) -> str:
        print(
            dedent(
                """
                Escolha uma opção:
                [1] Cadastrar perfil
                [2] Adicionar competência ao perfil
                [3] Analisar perfil e recomendar carreiras
                [4] Mostrar carreiras disponíveis
                [0] Sair
                """
            )
        )
        return input("Opção: ").strip()

    def _create_profile(self) -> None:
        name = input("Nome do perfil: ").strip()
        if not name:
            print("Nome inválido.")
            return
        profile = Profile(name)
        self.advisor.add_profile(profile)
        print(f"Perfil '{name}' cadastrado com sucesso!")

    def _add_competency(self) -> None:
        profile_name = input("Nome do perfil: ").strip()
        if not profile_name:
            print("Informe um nome de perfil.")
            return
        name = input("Nome da competência: ").strip()
        kind = input("Tipo (tecnica/comportamental): ").strip().lower()
        score_raw = input("Nota (0-10): ").strip()
        try:
            score = float(score_raw)
            competency = Competency(name=name, kind=kind, score=score)
        except ValueError as exc:
            print(f"Erro ao cadastrar competência: {exc}")
            return
        profile = self.advisor.add_competency_to_profile(profile_name, competency)
        print(f"Competência adicionada ao perfil '{profile.name}'.")

    def _analyze_profile(self) -> None:
        profile_name = input("Nome do perfil a analisar: ").strip()
        profile = self.advisor.get_profile(profile_name)
        if not profile:
            print("Perfil não encontrado. Cadastre-o primeiro.")
            return
        recommendations = self.advisor.analyze_profile(profile)
        if not recommendations:
            print("Nenhuma carreira cadastrada para comparação.")
            return
        self._print_recommendations(recommendations)

    def _print_recommendations(self, recommendations: list[Recommendation]) -> None:
        print("\nRecomendações:")
        for rec in recommendations:
            print(
                f"- {rec.career.name}: compatibilidade de {rec.match_percentage:.2f}%"
            )
            suggestions = self.advisor.suggest_improvements(rec)
            for suggestion in suggestions:
                print(f"  * {suggestion}")
        print()

    def _list_careers(self) -> None:
        print("Carreiras cadastradas:")
        for career in self.advisor.list_careers():
            requirements = ", ".join(
                f"{name} ({kind} {score})" for name, (kind, score) in career.required_competencies.items()
            )
            print(f"- {career.name}: {requirements}")
        print()


def demo() -> None:
    """Runs a demonstration of the CLI with mock data."""

    advisor = build_default_advisor()
    cli = CareerCLI(advisor)

    # Simulated data for demonstration
    demo_profile = Profile("Marina")
    demo_profile.add_competency(Competency("Python", "tecnica", 7.5))
    demo_profile.add_competency(Competency("Estatistica", "tecnica", 6))
    demo_profile.add_competency(Competency("Comunicacao", "comportamental", 6.5))
    advisor.add_profile(demo_profile)

    print(
        dedent(
            """
            ========================= DEMONSTRAÇÃO =========================
            Perfil exemplo: Marina
            Competências: Python 7.5, Estatística 6, Comunicação 6.5
            A seguir estão as recomendações geradas automaticamente.
            =================================================================
            """
        )
    )

    recommendations = advisor.analyze_profile(demo_profile)
    cli._print_recommendations(recommendations)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sistema de orientação de carreiras")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Executa uma simulação automática de cadastro e análise",
    )
    args = parser.parse_args()

    advisor = build_default_advisor()
    if args.demo:
        demo()
    else:
        CareerCLI(advisor).run()


if __name__ == "__main__":
    main()
