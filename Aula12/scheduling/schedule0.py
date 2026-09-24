"""Naive backtracking search without any heuristics or inference."""

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


def backtrack(assignment):
    """Runs backtracking search to find a complete assignment."""

    # TODO 1: reconheça o caso-base de uma atribuição completa.
    # TODO 2: selecione uma variável ainda não atribuída.
    # TODO 3: tente cada dia disponível em uma cópia da atribuição.
    # TODO 4: continue recursivamente apenas se a cópia for consistente.
    # TODO 5: retorne None quando nenhuma escolha produzir uma solução.
    raise NotImplementedError("Implemente a busca por backtracking.")


def select_unassigned_variable(assignment):
    """Chooses the first variable not yet assigned."""

    # TODO: percorra VARIABLES em ordem e retorne a primeira variável que não
    # aparece em `assignment`. Retorne None se todas já estiverem atribuídas.
    raise NotImplementedError("Implemente a seleção de variável.")


def consistent(assignment):
    """Checks whether a complete or partial assignment is consistent."""

    # TODO: para cada restrição, compare os dias somente quando suas duas
    # variáveis já estiverem na atribuição.
    raise NotImplementedError("Implemente a verificação das restrições.")


def main():
    solution = backtrack({})
    print(solution)


if __name__ == "__main__":
    main()
