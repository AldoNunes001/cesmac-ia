# Jogo da Velha

> A versão mais recente do Python que você deve usar neste curso é o Python 3.12.

Usando o algoritmo Minimax, implemente uma IA capaz de jogar jogo da velha de forma ótima.

![Jogo da Velha](https://cs50.harvard.edu/ai/projects/0/tictactoe/images/game.png)

## Primeiros Passos

- Baixe o código.
- Depois de entrar no diretório do projeto, crie um ambiente virtual e execute:

```bash
pip install -r requirements.txt
```

Esse comando instala o pacote Python necessário, `pygame`.

## Entendendo o Projeto

Há dois arquivos principais neste projeto: `runner.py` e `tictactoe.py`.

O arquivo `tictactoe.py` contém toda a lógica do jogo e da escolha de jogadas ótimas. O arquivo `runner.py` já foi implementado e contém o código responsável pela interface gráfica.

Depois de concluir todas as funções exigidas em `tictactoe.py`, você deverá conseguir executar:

```bash
python runner.py
```

para jogar contra a sua IA.

Abra o arquivo `tictactoe.py` para entender o que já foi fornecido. Três variáveis estão definidas:

- `X`
- `O`
- `EMPTY`

Elas representam os possíveis valores existentes no tabuleiro.

A função `initial_state` retorna o estado inicial do tabuleiro. O tabuleiro é representado como uma lista contendo três listas, correspondentes às suas três linhas. Cada lista interna contém três valores, e cada valor pode ser `X`, `O` ou `EMPTY`.

As demais funções devem ser implementadas por você.

## Especificação

Conclua a implementação das seguintes funções:

- `player`
- `actions`
- `result`
- `winner`
- `terminal`
- `utility`
- `minimax`

### `player`

A função `player` deve receber um estado de `board` como entrada e retornar qual jogador deve realizar a próxima jogada: `X` ou `O`.

- No estado inicial, `X` joga primeiro.
- Os jogadores se alternam depois de cada jogada.
- Qualquer valor de retorno será aceito caso seja fornecido um tabuleiro terminal, isto é, um tabuleiro em que a partida já terminou.

### `actions`

A função `actions` deve retornar um `set` contendo todas as ações possíveis em determinado tabuleiro.

- Cada ação deve ser representada como uma tupla `(i, j)`.
- `i` representa o índice da linha: `0`, `1` ou `2`.
- `j` representa o índice da célula dentro da linha: `0`, `1` ou `2`.
- Uma jogada possível corresponde a qualquer célula que ainda não contenha `X` ou `O`.
- Qualquer valor de retorno será aceito caso seja fornecido um tabuleiro terminal.

### `result`

A função `result` recebe um `board` e uma `action` como entrada e deve retornar um novo estado do tabuleiro, sem modificar o tabuleiro original.

- Se a `action` for inválida para o tabuleiro, o programa deverá [lançar uma exceção](https://docs.python.org/3/tutorial/errors.html#raising-exceptions).
- O tabuleiro retornado deve representar o tabuleiro original depois que o jogador atual realizar a jogada indicada por `action`.
- O tabuleiro original deve permanecer inalterado, porque o Minimax precisa examinar muitos estados diferentes do tabuleiro.
- Portanto, alterar diretamente uma célula de `board` está incorreto.
- Provavelmente será útil criar uma [cópia profunda](https://docs.python.org/3/library/copy.html#copy.deepcopy) do tabuleiro antes de modificá-lo.

### `winner`

A função `winner` deve receber um `board` e retornar o vencedor, caso exista.

- Retorne `X` se o jogador X tiver vencido.
- Retorne `O` se o jogador O tiver vencido.
- Um jogador vence ao formar uma sequência de três jogadas na horizontal, na vertical ou na diagonal.
- Você pode assumir que haverá, no máximo, um vencedor.
- Retorne `None` quando não houver vencedor, seja porque a partida ainda está em andamento, seja porque terminou empatada.

### `terminal`

A função `terminal` deve receber um `board` e retornar um valor booleano indicando se a partida terminou.

- Retorne `True` se alguém tiver vencido ou se todas as células tiverem sido preenchidas sem que exista um vencedor.
- Retorne `False` se a partida ainda estiver em andamento.

### `utility`

A função `utility` deve receber um `board` terminal e retornar sua utilidade.

- Retorne `1` se X tiver vencido.
- Retorne `-1` se O tiver vencido.
- Retorne `0` se a partida tiver terminado empatada.
- Você pode assumir que `utility` somente será chamada quando `terminal(board)` for `True`.

### `minimax`

A função `minimax` deve receber um `board` e retornar a jogada ótima para o jogador que deve jogar naquele momento.

- Retorne a ação válida ideal como uma tupla `(i, j)`.
- Se várias jogadas forem igualmente ótimas, qualquer uma delas será aceita.
- Retorne `None` se o tabuleiro for terminal.

Para todas as funções que recebem um `board`, você pode assumir que o tabuleiro é válido: ele contém três linhas, e cada linha contém três valores escolhidos entre `X`, `O` e `EMPTY`.

Não modifique as declarações das funções fornecidas, inclusive a quantidade ou a ordem de seus argumentos.

Depois que todas as funções forem implementadas corretamente, você deverá conseguir executar:

```bash
python runner.py
```

Em seguida, poderá jogar contra a sua IA. Como o jogo da velha termina empatado quando os dois lados jogam de maneira ótima, você nunca deverá conseguir derrotar a IA. Ela poderá derrotá-lo caso você também não jogue de maneira ótima.

## Dicas

- Para testar as funções a partir de outro arquivo Python, importe-as usando uma instrução como:

```python
from tictactoe import initial_state
```

- Você pode adicionar funções auxiliares a `tictactoe.py`, desde que seus nomes não entrem em conflito com os nomes das funções ou variáveis já existentes.
- A poda alfa-beta é opcional, mas pode tornar a IA mais eficiente.

## Testes

Para testar sua implementação execute:

```bash
python test_tictactoe.py
```

Esse comando avalia se o seu código está correto. 

Você não deve importar módulos que não façam parte da biblioteca padrão do Python ou que não tenham sido expressamente autorizados pela especificação da atividade. 

---

## Atribuição e Licença

Material original: **CS50’s Introduction to Artificial Intelligence with Python — Tic-Tac-Toe**, de CS50/Harvard University.

 O material original está licenciado sob a [Licença Internacional Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
