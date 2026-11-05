"""
Testes de progresso para Nim, com resultados e dicas em português.

Referência de apresentação: test_tictactoe.py da atividade de jogo da velha.
Não requer pytest, unittest ou pacotes externos.

Como executar nesta pasta:
    python test_nim.py
    python test_nim.py --modulo nim_gabarito

Os testes individuais isolam as dependências de cada função usando funções
de apoio; os testes de integração usam a implementação real, sem substituições.
Empates não exigem uma ação específica. Os testes de aleatoriedade restauram
o estado do gerador e usam sementes fixas, com tolerâncias amplas.

Este script auxilia o aprendizado; não substitui a especificação ou o check50.
Código de testes disponibilizado sob CC BY-NC-SA 4.0, como a atividade.
"""

import argparse
from collections import Counter
from contextlib import contextmanager, redirect_stdout
import importlib
import io
import math
from pathlib import Path
import random
import sys


class Reporter:
    """Exibe o esperado, o obtido e um resumo por função, sem parar nas falhas."""

    def __init__(self):
        self.section_name = None
        self.sections = {}
        self.failures = []

    def section(self, name):
        self.section_name = name
        self.sections[name] = [0, 0]
        print()
        print("=" * 72)
        print(f" Testando: {name}")
        print("=" * 72)

    def check_condition(self, description, actual_fn, condition, expected,
                        hint=None):
        try:
            actual = actual_fn()
            ok = bool(condition(actual))
        except NotImplementedError:
            actual = "NotImplementedError: a função ainda não foi implementada"
            ok = False
        except Exception as error:
            actual = f"{type(error).__name__}: {error}"
            ok = False

        self.sections[self.section_name][1] += 1
        if ok:
            self.sections[self.section_name][0] += 1
            print(f"  [OK]     {description}")
        else:
            self.failures.append((self.section_name, description))
            print(f"  [FALHOU] {description}")
            print(f"           esperado: {expected}")
            print(f"           obtido:   {actual}")
            if hint:
                print(f"           dica: {hint}")

    def check(self, description, actual_fn, expected, hint=None):
        self.check_condition(
            description, actual_fn, lambda actual: actual == expected,
            expected, hint,
        )

    def check_close(self, description, actual_fn, expected, hint=None):
        self.check_condition(
            description, actual_fn,
            lambda actual: math.isclose(actual, expected, abs_tol=1e-9),
            expected, hint,
        )

    def summary(self):
        print()
        print("=" * 72)
        print(" RESUMO POR FUNÇÃO")
        print("=" * 72)
        total_passed = 0
        total_all = 0
        for name, (passed, total) in self.sections.items():
            total_passed += passed
            total_all += total
            status = "OK" if passed == total else "COM FALHAS"
            print(f"  {name:<24} {passed}/{total} testes passaram  [{status}]")
        print()
        print("-" * 72)
        print(f" TOTAL GERAL: {total_passed}/{total_all} testes passaram")
        print("-" * 72)
        if self.failures:
            print("\n Revise as funções abaixo; os detalhes estão acima:")
            for section, description in self.failures:
                print(f"  - [{section}] {description}")
            return False
        print("\n Parabéns! Todos os testes passaram.")
        return True


@contextmanager
def fixed_seed(seed):
    """Torna os sorteios reproduzíveis sem alterar o gerador após o teste."""
    previous = random.getstate()
    random.seed(seed)
    try:
        yield
    finally:
        random.setstate(previous)


def supported_ai(module, q=None, alpha=0.5, epsilon=0.1):
    """Isola uma função das outras que o aluno ainda pode estar escrevendo."""
    ai = module.NimAI(alpha=alpha, epsilon=epsilon)
    ai.q = dict(q or {})
    ai.get_q_value = lambda state, action: ai.q.get((tuple(state), action), 0)
    ai.best_future_reward = lambda state: max(
        (ai.q.get((tuple(state), action), 0)
         for action in module.Nim.available_actions(state)),
        default=0,
    )
    return ai


def check_get_q_value(r, module):
    r.section("get_q_value")
    state = [1, 3, 0, 0]
    entries = {
        ((1, 3, 0, 0), (1, 2)): 0.75,
        ((1, 3, 0, 0), (0, 1)): -0.4,
        ((1, 3, 0, 0), (1, 3)): 0,
        ((3, 1, 0, 0), (1, 1)): 0.2,
    }

    def lookup(query_state, action, values=None):
        ai = module.NimAI()
        ai.q = dict(entries if values is None else values)
        return ai.get_q_value(query_state, action)

    r.check("Dicionário vazio: um par desconhecido deve valer 0",
            lambda: lookup(state, (1, 2), {}), 0,
            hint="A ausência de uma chave não deve causar KeyError.")
    r.check_close("Recupera um valor positivo usando um estado em lista",
                  lambda: lookup(state, (1, 2)), 0.75,
                  hint="Na chave do dicionário, o estado deve ser uma tupla.")
    r.check_close("Preserva valores Q negativos",
                  lambda: lookup(state, (0, 1)), -0.4)
    r.check("Preserva um valor Q armazenado como zero",
            lambda: lookup(state, (1, 3)), 0)
    r.check("Outra ação no mesmo estado não deve herdar um valor conhecido",
            lambda: lookup(state, (1, 1)), 0)
    r.check_close("A ordem das pilhas faz parte do estado",
                  lambda: lookup([3, 1, 0, 0], (1, 1)), 0.2,
                  hint="Não ordene as pilhas ao construir a chave.")
    r.check("Outro estado com a mesma ação deve ser consultado separadamente",
            lambda: lookup([1, 2, 0, 0], (1, 2)), 0)

    def unchanged():
        ai = module.NimAI()
        ai.q = dict(entries)
        original_state = list(state)
        ai.get_q_value(original_state, (1, 2))
        return original_state, ai.q

    r.check("Consultar um valor conhecido mantém o estado e os valores Q",
            unchanged, (state, entries))


def check_update_q_value(r, module):
    r.section("update_q_value")
    # alpha, old_q, reward, future_rewards, resultado esperado
    cases = [
        ("Vitória: aprende com recompensa +1", 0.5, 0, 1, 0, 0.5),
        ("Derrota: aprende com recompensa -1", 0.5, 0, -1, 0, -0.5),
        ("Sem recompensa imediata: considera a recompensa futura",
         0.5, 0.2, 0, 0.8, 0.5),
        ("Soma recompensa imediata e futura antes da atualização",
         0.5, -0.4, 1, 0.6, 0.6),
        ("Uma experiência ruim pode reduzir um valor positivo",
         0.5, 0.8, -1, 0.3, 0.05),
        ("Respeita uma taxa de aprendizado diferente de 0,5",
         0.2, 0.4, 1, 0.5, 0.62),
        ("alpha = 0 preserva o valor antigo", 0, -0.6, 1, 1, -0.6),
        ("alpha = 1 adota integralmente a nova estimativa",
         1, 0.7, -1, 0.25, -0.75),
        ("Uma recompensa futura negativa também deve ser considerada",
         0.5, 0.2, 0, -0.8, -0.3),
    ]

    def updated(alpha, old_q, reward, future):
        ai = module.NimAI(alpha=alpha)
        ai.update_q_value([0, 2], (1, 1), old_q, reward, future)
        return ai.q[((0, 2), (1, 1))]

    for description, alpha, old_q, reward, future, expected in cases:
        r.check_close(
            description,
            lambda a=alpha, o=old_q, v=reward, f=future: updated(a, o, v, f),
            expected,
            hint="Use old_q e self.alpha; a nova estimativa é reward + future_rewards.",
        )

    def respects_argument():
        ai = module.NimAI()
        ai.q[((0, 2), (1, 1))] = 0.9
        ai.update_q_value([0, 2], (1, 1), 0.2, 0, 0.8)
        return ai.q[((0, 2), (1, 1))]

    r.check_close("Usa o argumento old_q como estimativa antiga",
                  respects_argument, 0.5)

    def preserves_others():
        ai = module.NimAI()
        ai.q[((2, 0), (0, 1))] = -0.7
        state = [0, 2]
        ai.update_q_value(state, (1, 1), 0, 1, 0)
        return state, ai.q

    r.check("Atualiza a chave correta sem alterar outras entradas ou o estado",
            preserves_others,
            ([0, 2], {((2, 0), (0, 1)): -0.7, ((0, 2), (1, 1)): 0.5}))

    def repeated_updates():
        ai = module.NimAI()
        ai.update_q_value([1], (0, 1), 0, -1, 0)
        old_q = ai.q[((1,), (0, 1))]
        ai.update_q_value([1], (0, 1), old_q, -1, 0)
        return ai.q[((1,), (0, 1))]

    r.check_close("Atualizações repetidas aproximam o valor da recompensa",
                  repeated_updates, -0.75)


def check_best_future_reward(r, module):
    r.section("best_future_reward")

    def best(state, entries):
        ai = supported_ai(module, entries)
        # Restaura apenas a função que está sendo avaliada nesta seção.
        del ai.best_future_reward
        return ai.best_future_reward(state)

    cases = [
        ("Sem ações disponíveis, retorna 0", [0, 0], {}, 0),
        ("Com ações desconhecidas, retorna 0", [1, 2], {}, 0),
        ("Retorna o maior valor, e não a soma ou a média", [1, 2],
         {((1, 2), (0, 1)): 0.3, ((1, 2), (1, 1)): 0.8,
          ((1, 2), (1, 2)): 0.4}, 0.8),
        ("Se todas as ações forem negativas, retorna a menos negativa", [2],
         {((2,), (0, 1)): -0.7, ((2,), (0, 2)): -0.2}, -0.2),
        ("Uma ação desconhecida vale 0 e supera uma ação negativa", [2],
         {((2,), (0, 1)): -0.4}, 0),
        ("Considera ações em pilhas posteriores a uma pilha vazia", [0, 2],
         {((0, 2), (1, 1)): 0.6}, 0.6),
        ("Ignora valores de estados diferentes", [1],
         {((2,), (0, 1)): 100, ((1,), (0, 1)): -0.3}, -0.3),
        ("Ignora ações inválidas mesmo que tenham um valor Q alto", [1],
         {((1,), (0, 1)): -0.4, ((1,), (0, 2)): 100}, -0.4),
        ("Estado final retorna 0 mesmo com uma chave de ação inválida", [0],
         {((0,), (0, 1)): 100}, 0),
    ]
    for description, state, entries, expected in cases:
        r.check_close(
            description,
            lambda s=state, q=entries: best(s, q), expected,
            hint="Examine todas as ações válidas; 0 é o padrão das desconhecidas.",
        )


def draw_actions(module, state, entries, rate, flag=True, count=2000):
    """Amostra ações e explica imediatamente uma escolha inválida."""
    ai = supported_ai(module, entries, epsilon=rate)
    available = module.Nim.available_actions(state)
    before = state.copy()
    with fixed_seed(20261105):
        chosen = [ai.choose_action(state, epsilon=flag) for _ in range(count)]
    for action in chosen:
        if not isinstance(action, tuple) or action not in available:
            raise ValueError(f"ação inválida retornada: {action!r}")
    if state != before:
        raise ValueError(f"o estado foi alterado: {before!r} -> {state!r}")
    return Counter(chosen)


def check_choose_action(r, module):
    r.section("choose_action")
    state = [1, 2]
    entries = {
        ((1, 2), (0, 1)): 0.9,
        ((1, 2), (1, 1)): 0.2,
        ((1, 2), (1, 2)): -0.4,
    }

    def choose(query_state, values, rate=0.1, flag=False):
        with fixed_seed(51):
            return supported_ai(module, values, epsilon=rate).choose_action(
                query_state, epsilon=flag,
            )

    r.check("Seleção gulosa retorna a única ação com maior valor Q",
            lambda: choose(state, entries), (0, 1))
    r.check("epsilon=False desativa exploração mesmo com self.epsilon = 1",
            lambda: draw_actions(module, state, entries, 1, flag=False,
                                 count=100), Counter({(0, 1): 100}))
    r.check("self.epsilon = 0 sempre escolhe a melhor ação",
            lambda: draw_actions(module, state, entries, 0, count=100),
            Counter({(0, 1): 100}))
    r.check("Valores todos negativos: escolhe o maior deles",
            lambda: choose([2], {((2,), (0, 1)): -0.7,
                                 ((2,), (0, 2)): -0.2}), (0, 2),
            hint="O melhor valor não precisa ser positivo.")
    r.check("Ação desconhecida de valor 0 supera uma ação negativa",
            lambda: choose([2], {((2,), (0, 1)): -0.7}), (0, 2))
    r.check("Um valor positivo supera ações desconhecidas",
            lambda: choose(state, {((1, 2), (1, 2)): 0.1}), (1, 2))
    r.check("Ignora uma ação inválida com valor Q maior",
            lambda: choose([1], {((1,), (0, 1)): -0.4,
                                 ((1,), (0, 2)): 100}), (0, 1))
    r.check("Os valores de outros estados não interferem na escolha",
            lambda: choose([2], {((2,), (0, 1)): 0.4,
                                 ((2,), (0, 2)): 0.2,
                                 ((1,), (0, 2)): 100}), (0, 1))
    r.check("Com uma única ação válida, retorna essa ação",
            lambda: choose([0, 0, 1], {}, rate=1, flag=True), (2, 1))

    tied = {((1, 2), (0, 1)): 0.5, ((1, 2), (1, 1)): 0.5,
            ((1, 2), (1, 2)): -0.1}
    r.check_condition(
        "Empate: aceita qualquer ação ótima, mas nunca uma ação inferior",
        lambda: draw_actions(module, state, tied, 1, flag=False, count=100),
        lambda counts: set(counts) <= {(0, 1), (1, 1)},
        "somente (0, 1) e/ou (1, 1)",
    )
    r.check_condition(
        "Sem valores aprendidos, qualquer ação válida é aceita",
        lambda: choose([0, 2, 0], {}),
        lambda action: action in {(1, 1), (1, 2)},
        "(1, 1) ou (1, 2)",
    )

    def default_flag():
        ai = supported_ai(module, entries, epsilon=0)
        return ai.choose_action(state)

    r.check("O argumento epsilon é opcional", default_flag, (0, 1))

    r.check_condition(
        "Exploração total sorteia todas as ações, inclusive a melhor",
        lambda: draw_actions(module, state, entries, 1, count=2400),
        lambda counts: set(counts) == {(0, 1), (1, 1), (1, 2)}
        and all(abs(count - 800) <= 130 for count in counts.values()),
        "as três ações com aproximadamente 800 escolhas cada (±130)",
        hint="A exploração deve sortear entre todas as ações disponíveis.",
    )

    # A exploração também pode sortear a melhor ação. Com três ações, a
    # probabilidade de NÃO escolher a melhor é epsilon * 2/3.
    for rate in (0.1, 0.35, 0.8):
        expected = rate * 2 / 3

        def nongreedy_fraction(rate=rate):
            counts = draw_actions(module, state, entries, rate, count=3000)
            return 1 - counts[(0, 1)] / 3000

        r.check_condition(
            f"epsilon={rate}: equilibra exploração e escolha da melhor ação",
            nongreedy_fraction,
            lambda actual, target=expected: abs(actual - target) <= 0.045,
            f"fração de ações inferiores próxima de {expected:.3f} (±0,045)",
            hint="Use self.epsilon como probabilidade de sortear qualquer ação válida.",
        )


def check_integration(r, module):
    r.section("integração")

    def victory_update():
        ai = module.NimAI()
        ai.update([2], (0, 1), [0], 1)
        return ai.get_q_value([2], (0, 1))

    r.check_close("update() registra a recompensa de vitória em um estado final",
                  victory_update, 0.5)

    def defeat_update():
        ai = module.NimAI()
        ai.update([1], (0, 1), [0], -1)
        return ai.get_q_value([1], (0, 1))

    r.check_close("update() penaliza quem retira o último objeto",
                  defeat_update, -0.5)

    def future_update():
        ai = module.NimAI()
        ai.q[((1, 2), (1, 1))] = 0.2
        ai.q[((1, 0), (0, 1))] = 0.8
        ai.update([1, 2], (1, 1), [1, 0], 0)
        return ai.get_q_value([1, 2], (1, 1))

    r.check_close("update() combina o valor antigo e a melhor recompensa futura",
                  future_update, 0.5)

    def learned_move():
        ai = module.NimAI()
        ai.update([2], (0, 1), [0], 1)
        ai.update([2], (0, 2), [0], -1)
        return ai.choose_action([2], epsilon=False)

    r.check("Após recompensas opostas, prefere a ação que foi recompensada",
            learned_move, (0, 1))

    def train_and_inspect():
        with fixed_seed(123), redirect_stdout(io.StringIO()):
            ai = module.train(30)
        if not isinstance(ai, module.NimAI) or not ai.q:
            raise ValueError("train() deve retornar uma IA com valores Q aprendidos")
        valid_entries = all(
            isinstance(state, tuple)
            and isinstance(action, tuple)
            and action in module.Nim.available_actions(list(state))
            and isinstance(value, (int, float))
            and math.isfinite(value)
            for (state, action), value in ai.q.items()
        )
        has_positive = any(value > 0 for value in ai.q.values())
        has_negative = any(value < 0 for value in ai.q.values())
        return valid_entries, has_positive, has_negative

    r.check("Treinamento completo registra pares válidos e vitórias/derrotas",
            train_and_inspect, (True, True, True),
            hint="As quatro funções precisam trabalhar juntas durante train().")

    def complete_game():
        with fixed_seed(321), redirect_stdout(io.StringIO()):
            ai = module.train(20)
        game = module.Nim()
        limit = sum(game.piles)
        with fixed_seed(42):
            for _ in range(limit):
                previous_player = game.player
                action = ai.choose_action(game.piles, epsilon=False)
                if action not in module.Nim.available_actions(game.piles):
                    raise ValueError(f"ação inválida durante a partida: {action!r}")
                game.move(action)
                if game.winner is not None:
                    return all(pile == 0 for pile in game.piles), (
                        game.winner == module.Nim.other_player(previous_player)
                    )
        raise ValueError("a partida não terminou no limite de jogadas válidas")

    r.check("IA joga uma partida completa: quem remove o último objeto perde",
            complete_game, (True, True))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--modulo", default="nim",
        help="módulo Python a testar, sem .py (padrão: nim)",
    )
    args = parser.parse_args(argv)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        module = importlib.import_module(args.modulo)
        if not hasattr(module, "Nim") or not hasattr(module, "NimAI"):
            raise ImportError("o módulo precisa definir Nim e NimAI")
    except Exception as error:
        print(f"Não foi possível carregar {args.modulo}.py:")
        print(f"  {type(error).__name__}: {error}")
        print("Confira o nome do arquivo e corrija eventuais erros de sintaxe.")
        return 2

    print(f"Verificando {args.modulo}.py")
    print("As falhas não interrompem a execução dos demais testes.")
    reporter = Reporter()
    check_get_q_value(reporter, module)
    check_update_q_value(reporter, module)
    check_best_future_reward(reporter, module)
    check_choose_action(reporter, module)
    check_integration(reporter, module)
    return 0 if reporter.summary() else 1


if __name__ == "__main__":
    sys.exit(main())
