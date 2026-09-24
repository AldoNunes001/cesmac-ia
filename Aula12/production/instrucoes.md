# Exercício 1 — Otimização da produção

Neste exercício, você deverá traduzir um problema de produção para o formato
esperado pelo `scipy.optimize.linprog`.

## Problema

Uma empresa precisa decidir quantas horas dedicar a dois processos, `x1` e
`x2`. O objetivo é minimizar o custo total:

```text
minimizar 50x1 + 80x2
```

As decisões devem respeitar as seguintes restrições:

```text
 5x1 +  2x2 <= 20
10x1 + 12x2 >= 90
x1, x2 >= 0
```

Observe que `linprog` recebe restrições de desigualdade no formato
`A_ub @ x <= b_ub`. Portanto, uma das restrições acima precisa ser
multiplicada por `-1` antes de ser informada à biblioteca.

## Sua tarefa

Complete a função `solve_production_problem` em `production.py`:

1. represente a função objetivo como uma lista de coeficientes;
2. monte a matriz `A_ub` com os coeficientes das restrições;
3. monte o vetor `b_ub` com os limites das restrições;
4. chame `scipy.optimize.linprog` e retorne o objeto resultante.

Não altere a função `main`. Os limites padrão de `linprog` já garantem que as
duas variáveis sejam não negativas, mas você pode declará-los explicitamente.

## Execução

Instale o SciPy, caso necessário, e execute o programa a partir desta pasta:

```bash
python -m pip install scipy
python production.py
```

Para conferir sua modelagem, a solução ótima deve estar próxima de:

```text
X1: 1.50 hours
X2: 6.25 hours
Minimum cost: 575.00
```

Pequenas diferenças nas últimas casas decimais são normais.

## Questões para reflexão

- Por que a segunda restrição precisa mudar de sinal?
- Qual restrição fica ativa na solução ótima?
- O que acontece se o limite `20` da primeira restrição for reduzido?
