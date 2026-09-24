# Exercício 3 — Agendamento como satisfação de restrições

Neste exercício, sete disciplinas ou eventos, representados pelas letras de
`A` a `G`, precisam ser agendados em um dos três dias disponíveis. Cada par em
`CONSTRAINTS` representa eventos que não podem acontecer no mesmo dia.

Você resolverá o mesmo problema de duas formas:

- `schedule0.py`: implementação manual com busca por backtracking;
- `schedule1.py`: modelagem com a biblioteca `python-constraint`.

## Parte 1 — Backtracking manual

Complete em `schedule0.py`:

### `select_unassigned_variable`

Percorra `VARIABLES` na ordem fornecida e retorne a primeira variável que ainda
não esteja presente em `assignment`. Se todas estiverem atribuídas, retorne
`None`.

### `consistent`

Percorra os pares de `CONSTRAINTS`. Uma restrição só pode ser verificada quando
as duas variáveis do par já tiverem valores. Nesse caso, a atribuição é
inconsistente se os valores forem iguais.

A função deve funcionar tanto com atribuições parciais quanto completas.

### `backtrack`

Implemente a busca recursiva:

1. se todas as variáveis estiverem atribuídas, retorne a solução;
2. selecione uma variável ainda não atribuída;
3. tente cada valor de `DAYS` em uma cópia da atribuição;
4. continue a busca somente se a nova atribuição for consistente;
5. devolva a primeira solução completa encontrada;
6. retorne `None` quando nenhuma escolha funcionar.

Use uma cópia do dicionário em cada tentativa para que uma ramificação da busca
não altere as demais.

Execute com:

```bash
python schedule0.py
```

## Parte 2 — Biblioteca de restrições

Instale a dependência, se necessário:

```bash
python -m pip install python-constraint
```

Em `schedule1.py`, complete `build_problem` para:

1. adicionar todas as `VARIABLES` com `DAYS` como domínio;
2. adicionar uma restrição de desigualdade para cada par em `CONSTRAINTS`;
3. retornar o objeto `Problem` configurado.

Depois, complete `main` para obter e imprimir todas as soluções. Execute com:

```bash
python schedule1.py
```

## Critérios de verificação

Para cada solução produzida:

- as sete variáveis devem possuir um dia;
- os valores devem pertencer a `DAYS`;
- para todo par `(x, y)` em `CONSTRAINTS`, os dias de `x` e `y` devem ser
  diferentes.

As duas implementações podem imprimir soluções em ordens diferentes. A versão
manual para na primeira solução, enquanto a versão com a biblioteca deve listar
todas elas.

## Questões para reflexão

- Qual é o caso-base da função recursiva?
- Em que situação ocorre o retrocesso (*backtrack*)?
- Que vantagens e desvantagens existem ao usar uma biblioteca para modelar o
  mesmo problema?
