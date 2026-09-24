"""Solves the scheduling problem with the python-constraint library."""

from constraint import Problem


VARIABLES = ["A", "B", "C", "D", "E", "F", "G"]
DAYS = ["Monday", "Tuesday", "Wednesday"]
CONSTRAINTS = [
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "D"),
    ("B", "E"),
    ("C", "E"),
    ("C", "F"),
    ("D", "E"),
    ("E", "F"),
    ("E", "G"),
    ("F", "G"),
]


def build_problem():
    """Builds and returns the constraint satisfaction problem."""
    problem = Problem()

    # TODO 1: adicione todas as variáveis e use DAYS como domínio.
    # TODO 2: adicione, para cada par em CONSTRAINTS, uma restrição que exija
    # valores diferentes.
    # TODO 3: retorne o problema configurado.
    raise NotImplementedError("Configure o problema de restrições.")


def main():
    problem = build_problem()

    # TODO: obtenha e exiba todas as soluções encontradas pela biblioteca.
    raise NotImplementedError("Resolva e exiba as soluções.")


if __name__ == "__main__":
    main()
