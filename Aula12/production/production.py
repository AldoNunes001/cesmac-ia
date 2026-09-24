import scipy.optimize


def solve_production_problem():
    """Modela e resolve o problema de produção descrito em instrucoes.md."""

    # TODO 1: represente os coeficientes da função objetivo.
    # TODO 2: represente os coeficientes do lado esquerdo das restrições.
    # TODO 3: represente os limites do lado direito das restrições.
    # TODO 4: chame scipy.optimize.linprog e retorne o resultado.
    #
    # Atenção: linprog trabalha com restrições no formato A_ub @ x <= b_ub.
    raise NotImplementedError("Implemente o modelo de programação linear.")


def main():
    result = solve_production_problem()

    if result.success:
        print(f"X1: {result.x[0]:.2f} hours")
        print(f"X2: {result.x[1]:.2f} hours")
        print(f"Minimum cost: {result.fun:.2f}")
    else:
        print("No solution")


if __name__ == "__main__":
    main()
