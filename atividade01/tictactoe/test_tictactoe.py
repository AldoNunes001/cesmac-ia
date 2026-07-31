"""
Script de verificacao das funcoes de tictactoe.py

Este script NAO usa o modulo unittest de proposito: a ideia e que qualquer
aluno consiga rodar `python test_tictactoe.py` e entender imediatamente,
em portugues, o que foi testado, o que era esperado e o que o codigo
realmente retornou.

Como rodar:
    cd tictactoe
    python test_tictactoe.py
(ou usando o venv do projeto: ../venv/bin/python test_tictactoe.py)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tictactoe import (  # noqa: E402
    X, O, EMPTY,
    initial_state,
    player,
    actions,
    result,
    winner,
    terminal,
    utility,
    minimax,
)


class Reporter:
    """Coleta e imprime os resultados dos testes de forma explicativa."""

    def __init__(self):
        self.section_name = None
        self.sections_order = []
        self.sections = {}  # nome -> [passou, total]
        self.failures = []  # (secao, descricao, esperado, obtido, dica)

    def section(self, name):
        self.section_name = name
        self.sections_order.append(name)
        self.sections[name] = [0, 0]
        print()
        print("=" * 72)
        print(f" Testando: {name}")
        print("=" * 72)

    def _register(self, ok, description, expected, actual, hint):
        self.sections[self.section_name][1] += 1
        if ok:
            self.sections[self.section_name][0] += 1
            print(f"  [OK]     {description}")
        else:
            self.failures.append((self.section_name, description, expected, actual, hint))
            print(f"  [FALHOU] {description}")
            print(f"           esperado: {expected}")
            print(f"           obtido:   {actual}")
            if hint:
                print(f"           dica: {hint}")

    def check(self, description, actual_fn, expected, hint=None):
        """Executa actual_fn() e compara o resultado com `expected`."""
        try:
            actual = actual_fn()
            ok = actual == expected
        except Exception as e:
            actual = f"{type(e).__name__}: {e}"
            ok = False
        self._register(ok, description, expected, actual, hint)

    def check_raises(self, description, func, hint=None):
        """Espera que func() lance uma excecao (ex.: jogada invalida)."""
        try:
            func()
        except NotImplementedError:
            self._register(
                False, description, "uma excecao (por jogada invalida)",
                "NotImplementedError: a funcao ainda nao foi implementada", hint,
            )
        except Exception as e:
            self._register(True, description, "uma excecao", f"{type(e).__name__}: {e}", hint)
        else:
            self._register(False, description, "uma excecao (Exception)", "nenhuma excecao foi lancada", hint)

    def summary(self):
        print()
        print("=" * 72)
        print(" RESUMO POR FUNCAO")
        print("=" * 72)
        total_passed = 0
        total_all = 0
        for name in self.sections_order:
            passed, total = self.sections[name]
            total_passed += passed
            total_all += total
            status = "OK" if passed == total else "COM FALHAS"
            print(f"  {name:<15} {passed}/{total} testes passaram  [{status}]")

        print()
        print("-" * 72)
        print(f" TOTAL GERAL: {total_passed}/{total_all} testes passaram")
        print("-" * 72)

        if self.failures:
            print()
            print(f" {len(self.failures)} teste(s) falharam. Detalhe:")
            for section, desc, _expected, _actual, _hint in self.failures:
                print(f"  - [{section}] {desc}")
            print()
            print(" Revise as funcoes listadas acima. Role para cima para ver")
            print(" o motivo detalhado de cada falha (esperado x obtido).")
            return False
        else:
            print()
            print(" Parabens! Todas as funcoes passaram em todos os testes.")
            return True


r = Reporter()


# ---------------------------------------------------------------------------
# player()
# ---------------------------------------------------------------------------
r.section("player")

r.check(
    "Tabuleiro inicial (vazio): quem joga primeiro deve ser X",
    lambda: player(initial_state()),
    X,
    hint="No jogo da velha, X sempre comeca.",
)

board = [[X, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "Depois de 1 jogada de X, deve ser a vez de O",
    lambda: player(board),
    O,
    hint="Os jogadores se alternam: X, O, X, O, ...",
)

board = [[X, O, X],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "Depois de X, O, X (2 X e 1 O), deve ser a vez de O",
    lambda: player(board),
    O,
)

board = [[X, O, X],
         [X, O, O],
         [O, X, EMPTY]]
r.check(
    "Tabuleiro quase cheio (4 X e 4 O), deve ser a vez de X",
    lambda: player(board),
    X,
)


# ---------------------------------------------------------------------------
# actions()
# ---------------------------------------------------------------------------
r.section("actions")

r.check(
    "Tabuleiro inicial deve ter as 9 posicoes como jogadas possiveis",
    lambda: actions(initial_state()),
    {(i, j) for i in range(3) for j in range(3)},
)

board = [[X, EMPTY, EMPTY],
         [EMPTY, O, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "Tabuleiro parcialmente preenchido deve retornar so as posicoes vazias",
    lambda: actions(board),
    {(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)},
)

board = [[X, O, X],
         [X, O, O],
         [O, X, X]]
r.check(
    "Tabuleiro cheio nao deve ter nenhuma jogada possivel",
    lambda: actions(board),
    set(),
)


# ---------------------------------------------------------------------------
# result()
# ---------------------------------------------------------------------------
r.section("result")

r.check(
    "result() deve colocar o simbolo do jogador certo na posicao jogada",
    lambda: result(initial_state(), (0, 0))[0][0],
    X,
)

board = initial_state()
r.check(
    "result() nao deve alterar o tabuleiro original (deve copiar, nao mutar)",
    lambda: (result(board, (1, 1)), board)[1],
    initial_state(),
    hint="Use copy.deepcopy (ou equivalente) antes de modificar o tabuleiro.",
)

board = [[X, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "Apos a jogada de X, a proxima marcada deve ser O (jogadores alternam)",
    lambda: result(board, (1, 1))[1][1],
    O,
)

board = [[X, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check_raises(
    "Jogar em uma posicao ja ocupada deve lancar uma excecao",
    lambda: result(board, (0, 0)),
    hint="Verifique se a acao esta em actions(board) antes de aplicar a jogada.",
)


# ---------------------------------------------------------------------------
# winner()
# ---------------------------------------------------------------------------
r.section("winner")

r.check(
    "Tabuleiro inicial nao deve ter vencedor",
    lambda: winner(initial_state()),
    None,
)

board = [[X, X, X],
         [O, O, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "3 X em linha (linha 0) deve dar vitoria para X",
    lambda: winner(board),
    X,
)

board = [[O, X, EMPTY],
         [O, X, EMPTY],
         [O, EMPTY, EMPTY]]
r.check(
    "3 O em coluna (coluna 0) deve dar vitoria para O",
    lambda: winner(board),
    O,
)

board = [[X, O, EMPTY],
         [O, X, EMPTY],
         [EMPTY, EMPTY, X]]
r.check(
    "3 X na diagonal principal deve dar vitoria para X",
    lambda: winner(board),
    X,
)

board = [[EMPTY, O, X],
         [O, X, EMPTY],
         [X, EMPTY, EMPTY]]
r.check(
    "3 X na diagonal secundaria (anti-diagonal) deve dar vitoria para X",
    lambda: winner(board),
    X,
)

board = [[X, O, X],
         [X, O, O],
         [O, X, X]]
r.check(
    "Tabuleiro cheio empatado nao deve ter vencedor",
    lambda: winner(board),
    None,
)


# ---------------------------------------------------------------------------
# terminal()
# ---------------------------------------------------------------------------
r.section("terminal")

r.check(
    "Tabuleiro inicial nao deve ser terminal (jogo comecando)",
    lambda: terminal(initial_state()),
    False,
)

board = [[X, EMPTY, EMPTY],
         [EMPTY, O, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "Jogo em andamento (sem vencedor e com casas vazias) nao deve ser terminal",
    lambda: terminal(board),
    False,
)

board = [[X, X, X],
         [O, O, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "Jogo com um vencedor deve ser terminal, mesmo com casas vazias",
    lambda: terminal(board),
    True,
)

board = [[X, O, X],
         [X, O, O],
         [O, X, X]]
r.check(
    "Tabuleiro cheio (empate) deve ser terminal",
    lambda: terminal(board),
    True,
)


# ---------------------------------------------------------------------------
# utility()
# ---------------------------------------------------------------------------
r.section("utility")

board = [[X, X, X],
         [O, O, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "Vitoria de X deve ter utilidade 1",
    lambda: utility(board),
    1,
)

board = [[O, X, X],
         [O, X, EMPTY],
         [O, EMPTY, EMPTY]]
r.check(
    "Vitoria de O deve ter utilidade -1",
    lambda: utility(board),
    -1,
)

board = [[X, O, X],
         [X, O, O],
         [O, X, X]]
r.check(
    "Empate deve ter utilidade 0",
    lambda: utility(board),
    0,
)


# ---------------------------------------------------------------------------
# minimax()
# ---------------------------------------------------------------------------
r.section("minimax")

board = [[X, X, X],
         [O, O, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "Em um tabuleiro terminal, minimax() deve retornar None",
    lambda: minimax(board),
    None,
)

board = [[X, X, EMPTY],
         [O, O, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "Se X pode vencer jogando em (0, 2), minimax() deve escolher essa jogada",
    lambda: minimax(board),
    (0, 2),
    hint="Verifique se max_value()/min_value() estao retornando a melhor jogada, nao so o melhor valor.",
)

board = [[O, O, EMPTY],
         [X, X, EMPTY],
         [X, EMPTY, EMPTY]]
r.check(
    "Se O pode vencer jogando em (0, 2), minimax() deve escolher essa jogada",
    lambda: minimax(board),
    (0, 2),
)

board = [[O, X, EMPTY],
         [O, EMPTY, X],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "Se O ameaca vencer na coluna 0, X deve bloquear jogando em (2, 0)",
    lambda: minimax(board),
    (2, 0),
    hint="minimax() deve escolher a jogada que impede a derrota, nao so procurar uma vitoria propria.",
)

board = [[X, X, EMPTY],
         [O, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
r.check(
    "Se X ameaca vencer na linha 0, O deve bloquear jogando em (0, 2)",
    lambda: minimax(board),
    (0, 2),
)


def simulate_optimal_game():
    """Simula uma partida completa com ambos os lados jogando via minimax."""
    board = initial_state()
    for _ in range(9):
        if terminal(board):
            break
        move = minimax(board)
        if move is None:
            raise Exception("minimax() retornou None antes do jogo terminar")
        board = result(board, move)
    if not terminal(board):
        raise Exception("o jogo nao terminou apos 9 jogadas (verifique terminal/actions/result)")
    return utility(board)


r.check(
    "Se X e O jogarem sempre a jogada otima (minimax), o jogo deve empatar",
    simulate_optimal_game,
    0,
    hint="Isso e uma propriedade classica da velha: com jogo perfeito dos dois lados, ninguem vence.",
)


if __name__ == "__main__":
    ok = r.summary()
    sys.exit(0 if ok else 1)
