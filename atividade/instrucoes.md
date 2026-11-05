# Nim

> A versão mais recente do Python que você deve usar neste curso é o Python 3.12.

Escreva uma IA que aprenda sozinha a jogar Nim por meio de aprendizado por reforço.

```text
$ python play.py
Playing training game 1
Playing training game 2
Playing training game 3
...
Playing training game 9999
Playing training game 10000
Done training

Piles:
Pile 0: 1
Pile 1: 3
Pile 2: 5
Pile 3: 7

AI's Turn
AI chose to take 1 from pile 2.
```

## Quando Fazer

Até [2027-06-30T23:59:00+00:00](https://time.cs50.io/20270630T235900Z).

## Como Obter Ajuda

1. Faça perguntas pelo [Ed](https://cs50.edx.org/ed)!
2. Faça perguntas em qualquer uma das [comunidades do CS50](https://cs50.harvard.edu/ai/communities/)!

## Contexto

Lembre-se de que, no jogo Nim, começamos com uma determinada quantidade de pilhas, cada uma contendo uma determinada quantidade de objetos. Os jogadores se alternam: em sua vez, um jogador remove qualquer quantidade não negativa de objetos de uma única pilha que não esteja vazia. Quem remover o último objeto perde.

É possível imaginar uma estratégia simples para esse jogo: se houver apenas uma pilha com três objetos restantes e for a sua vez, a melhor opção será remover dois desses objetos, deixando para o adversário o terceiro e último objeto. Mas, se houver mais pilhas, a estratégia se torna consideravelmente mais complicada. Neste problema, construiremos uma IA que aprenderá a estratégia desse jogo por meio de aprendizado por reforço. Ao jogar contra si mesma repetidamente e aprender com a experiência, nossa IA acabará aprendendo quais ações realizar e quais evitar.

Em particular, usaremos Q-learning neste projeto. Lembre-se de que, no Q-learning, tentamos aprender um valor de recompensa (um número) para cada par `(state, action)`, isto é, estado e ação. Uma ação que leva à derrota terá uma recompensa de -1; uma ação que faz o outro jogador perder terá uma recompensa de 1; e uma ação que faz a partida continuar terá uma recompensa imediata de 0, mas também terá alguma recompensa futura.

Como representaremos os estados e as ações em um programa Python? Um “estado” do jogo Nim é simplesmente o tamanho atual de todas as pilhas. Um estado poderia ser, por exemplo, `[1, 1, 3, 5]`, representando 1 objeto na pilha 0, 1 objeto na pilha 1, 3 objetos na pilha 2 e 5 objetos na pilha 3. Uma “ação” no jogo Nim será um par de inteiros `(i, j)`, representando a retirada de `j` objetos da pilha `i`. Assim, a ação `(3, 5)` representa “retirar 5 objetos da pilha 3”. Aplicar essa ação ao estado `[1, 1, 3, 5]` resultaria no novo estado `[1, 1, 3, 0]`: o mesmo estado, mas agora com a pilha 3 vazia.

Lembre-se de que a fórmula principal do Q-learning é a seguinte. Sempre que estamos em um estado `s` e realizamos uma ação `a`, podemos atualizar o valor Q, `Q(s, a)`, de acordo com:

```text
Q(s, a) <- Q(s, a) + alpha * (estimativa do novo valor - estimativa do valor antigo)
```

Na fórmula acima, `alpha` é a taxa de aprendizado: quanto valorizamos as informações novas em comparação com as informações que já temos. A `estimativa do novo valor` representa a soma da recompensa recebida pela ação atual com a estimativa de todas as recompensas futuras que o jogador receberá. A `estimativa do valor antigo` é simplesmente o valor atual de `Q(s, a)`. Aplicando essa fórmula sempre que nossa IA realizar uma nova ação, ela começará, ao longo do tempo, a aprender quais ações são melhores em cada estado.

## Primeiros Passos

- Baixe o [código de distribuição](https://cdn.cs50.net/ai/2023/x/projects/4/nim.zip) e descompacte-o.

## Entendendo o Projeto

Primeiro, abra `nim.py`. Há duas classes definidas nesse arquivo, `Nim` e `NimAI`, além de duas funções, `train` e `play`. A classe `Nim` e as funções `train` e `play` já foram implementadas para você, enquanto `NimAI` possui algumas funções que você deverá implementar.

Examine a classe `Nim`, que define como uma partida de Nim é jogada. Na função `__init__`, observe que cada partida precisa acompanhar uma lista de pilhas, o jogador atual (0 ou 1) e o vencedor da partida, caso exista. A função `available_actions` retorna um conjunto com todas as ações disponíveis em um estado. Por exemplo, `Nim.available_actions([2, 1, 0, 0])` retorna o conjunto `{(0, 1), (1, 1), (0, 2)}`, pois as três ações possíveis são retirar 1 ou 2 objetos da pilha 0 ou retirar 1 objeto da pilha 1.

As demais funções são usadas para definir a dinâmica da partida: `other_player` determina quem é o adversário de determinado jogador; `switch_player` troca o jogador atual pelo adversário; e `move` realiza uma ação no estado atual e troca o jogador atual pelo adversário.

Em seguida, examine a classe `NimAI`, que define nossa IA que aprenderá a jogar Nim. Observe que, na função `__init__`, começamos com um dicionário vazio, `self.q`. Esse dicionário acompanhará todos os valores Q que nossa IA aprender, associando pares `(state, action)` a valores numéricos. Como detalhe de implementação, embora normalmente representemos `state` como uma lista, listas não podem ser usadas como chaves de dicionários Python. Por isso, usaremos uma versão do estado em forma de tupla ao consultar ou definir valores em `self.q`.

Por exemplo, se quiséssemos definir como `-1` o valor Q do estado `[0, 0, 0, 2]` e da ação `(3, 2)`, escreveríamos algo como:

```python
self.q[(0, 0, 0, 2), (3, 2)] = -1
```

Observe também que cada objeto `NimAI` possui os valores `alpha` e `epsilon`, que serão usados, respectivamente, no Q-learning e na seleção de ações.

A função `update` já foi escrita para você. Ela recebe como entrada um estado `old_state`, uma ação `action` realizada nesse estado, o estado resultante `new_state` após a execução dessa ação e a recompensa imediata `reward` por realizá-la. Em seguida, a função executa o Q-learning: primeiro obtém o valor Q atual para o estado e a ação, chamando `get_q_value`; determina as melhores recompensas futuras possíveis, chamando `best_future_reward`; e usa esses dois valores para atualizar o valor Q, chamando `update_q_value`. Essas três funções deverão ser implementadas por você.

Por fim, a última função ainda não implementada é `choose_action`, que seleciona uma ação a ser realizada em determinado estado, de maneira gulosa ou usando o algoritmo epsilon-greedy.

As classes `Nim` e `NimAI` são usadas nas funções `train` e `play`. A função `train` treina uma IA executando `n` partidas simuladas contra ela mesma e retorna a IA treinada. A função `play` recebe uma IA treinada como entrada e permite que uma pessoa jogue uma partida de Nim contra ela.

## Especificação

Conclua a implementação de `get_q_value`, `update_q_value`, `best_future_reward` e `choose_action` em `nim.py`. Em todas essas funções, sempre que uma função receber um `state` como entrada, você poderá assumir que ele é uma lista de inteiros. Sempre que uma função receber uma `action` como entrada, você poderá assumir que ela é um par de inteiros `(i, j)`, indicando uma pilha `i` e uma quantidade de objetos `j`.

A função `get_q_value` deve receber um `state` e uma `action` como entrada e retornar o valor Q correspondente a esse par de estado e ação.

- Lembre-se de que os valores Q são armazenados no dicionário `self.q`. As chaves de `self.q` devem ser pares `(state, action)`, em que `state` é uma tupla com os tamanhos de todas as pilhas, em ordem, e `action` é uma tupla `(i, j)`, representando uma pilha e uma quantidade.
- Se não houver em `self.q` um valor Q para esse par de estado e ação, a função deverá retornar `0`.

A função `update_q_value` recebe um estado `state`, uma ação `action`, um valor Q existente `old_q`, uma recompensa atual `reward` e uma estimativa de recompensas futuras `future_rewards`. Ela deve atualizar o valor Q desse par de estado e ação de acordo com a fórmula do Q-learning.

- Lembre-se de que a fórmula do Q-learning é: `Q(s, a) <- estimativa do valor antigo + alpha * (estimativa do novo valor - estimativa do valor antigo)`.
- Lembre-se de que `alpha` é a taxa de aprendizado associada ao objeto `NimAI`.
- A estimativa do valor antigo é simplesmente o valor Q existente para o par de estado e ação. A estimativa do novo valor deve ser a soma da recompensa atual com a recompensa futura estimada.

A função `best_future_reward` recebe um `state` como entrada e retorna a melhor recompensa possível entre todas as ações disponíveis nesse estado, de acordo com os dados de `self.q`.

- Para qualquer ação que ainda não exista em `self.q` para o estado fornecido, assuma um valor Q igual a 0.
- Se não houver ações disponíveis nesse estado, retorne 0.

A função `choose_action` deve receber um `state` como entrada e, opcionalmente, um parâmetro booleano `epsilon`, que indica se o algoritmo epsilon-greedy deve ser usado. Ela deve retornar uma ação disponível nesse estado.

- Se `epsilon` for `False`, a função deverá agir de maneira gulosa e retornar a melhor ação disponível nesse estado, isto é, a ação com o maior valor Q, considerando 0 quando nenhum valor Q for conhecido.
- Se `epsilon` for `True`, a função deverá seguir o algoritmo epsilon-greedy: escolher uma ação aleatória disponível com probabilidade `self.epsilon` e, caso contrário, escolher a melhor ação disponível.
- Se várias ações tiverem o mesmo valor Q, qualquer uma delas será um retorno aceitável.

Não modifique nenhuma outra parte de `nim.py` além das funções indicadas na especificação, embora você possa escrever funções auxiliares e importar outros módulos da biblioteca padrão do Python. Você também pode importar `numpy` ou `pandas`, caso esteja familiarizado com essas bibliotecas, mas não deve usar nenhum outro módulo Python de terceiros. Você pode modificar `play.py` para realizar seus próprios testes.

## Dicas

- Se `lst` for uma lista, use `tuple(lst)` para convertê-la em uma tupla.

## Testes

Se desejar, você pode executar o comando abaixo, depois de [configurar o `check50`](https://cs50.readthedocs.io/projects/check50/en/latest/index.html) no seu sistema, para avaliar se seu código está correto. Isso não é obrigatório: você pode simplesmente enviar a atividade seguindo as etapas ao final desta especificação, e esses mesmos testes serão executados no servidor do CS50. De qualquer forma, lembre-se de também verificar e testar seu código por conta própria!

```bash
check50 ai50/projects/2024/x/nim
```

Execute o comando abaixo para avaliar o estilo do seu código usando `style50`.

```bash
style50 nim.py
```

> Lembre-se de que **você não pode importar módulos**, com exceção dos módulos da biblioteca padrão do Python, **além daqueles explicitamente autorizados neste documento**. Fazer isso impedirá tanto a execução do `check50` quanto a correção da atividade pelo `submit50`, que usa o `check50`. Se isso acontecer, provavelmente você importou algo não permitido ou modificou o código de distribuição de maneira não autorizada pela especificação. Existem ferramentas que tornam alguns destes projetos triviais, mas esse não é o objetivo: você está aprendendo os conceitos em um nível mais fundamental. Se o uso de uma ferramenta não foi autorizado aqui, ela não pode ser usada.

## Como Enviar

1. Acesse [este link](https://submit.cs50.io/invites/d03c31aef1984c29b5e7b268c3a87b7b), entre com sua conta do GitHub e clique em **Authorize cs50**. Em seguida, marque a caixa indicando que deseja conceder à equipe do curso acesso aos seus envios e clique em **Join course**.
2. [Instale o Git](https://git-scm.com/downloads) e, opcionalmente, [instale o `submit50`](https://cs50.readthedocs.io/submit50/).
3. Se você instalou o `submit50`, execute:

   ```bash
   submit50 ai50/projects/2024/x/nim
   ```

   Caso contrário, usando o Git, envie seu trabalho para `https://github.com/me50/USERNAME.git`, em que `USERNAME` é seu nome de usuário do GitHub, em uma branch chamada `ai50/projects/2024/x/nim`.

> Se você enviar seu código diretamente pelo Git, em vez de usar `submit50`, **não inclua arquivos ou pastas além daqueles que a especificação acima orienta a modificar**. Ou seja, não envie o diretório inteiro!

O trabalho deverá ser corrigido em até cinco minutos. Você poderá então acessar [seu progresso no CS50 AI](https://cs50.me/cs50ai) para consultar o resultado!

---

## Complemento para Esta Turma

As seções acima são a tradução integral do enunciado do CS50. O prazo, os canais de ajuda e as etapas de envio nelas descritos pertencem ao curso original; para esta turma, siga o prazo e a forma de entrega definidos pelo professor.

O texto original usa a expressão “quantidade não negativa”. No código fornecido, uma jogada válida exige retirar **pelo menos um objeto** de uma única pilha, sem ultrapassar a quantidade disponível nela. A função `Nim.available_actions` já aplica essa regra. Quem retira o último objeto perde.

Os arquivos `nim.py` e `play.py` do código oficial já estão nesta pasta. Implemente as quatro funções solicitadas em `nim.py`. Não é necessário instalar pacotes adicionais para executar o projeto e os testes locais.

Para acompanhar seu progresso, execute nesta pasta:

```bash
python test_nim.py
```

O script agrupa os testes por função, apresenta o que era esperado e o que foi obtido, fornece dicas em caso de falha e mostra um resumo ao final. Funções que ainda lançam `NotImplementedError` aparecem como falhas, e os outros testes continuam sendo executados. Na verificação individual, as funções auxiliares já testadas são substituídas por versões de apoio, para permitir que você acompanhe separadamente o progresso de cada função. A seção de integração verifica as funções reais trabalhando juntas.

Os testes usam somente a biblioteca padrão do Python. A verificação da seleção aleatória usa uma semente fixa e margens de tolerância; em caso de empate entre os melhores valores Q, qualquer ação ótima é aceita. Esses testes são auxiliares e não garantem a correção de todos os casos possíveis, nem substituem os testes oficiais do CS50.

Depois de implementar as funções, execute:

```bash
python play.py
```

O programa treinará a IA em 10.000 partidas contra ela mesma e permitirá que você jogue contra ela no terminal. Como o aprendizado envolve exploração aleatória, o treinamento não garante que a IA jogue perfeitamente em todas as partidas.

## Atribuição e Licença

Material original: **CS50’s Introduction to Artificial Intelligence with Python — Nim**, de Brian Yu, David J. Malan e CS50/Harvard University.

Fonte: [enunciado original do Nim](https://cs50.harvard.edu/ai/projects/4/nim/), consultado em 5 de novembro de 2026. O enunciado original não contém imagens; seus exemplos de terminal, blocos de código, seções, listas e links foram preservados em Markdown. A saída do terminal foi mantida em inglês para corresponder ao programa fornecido.

Alterações: tradução para português e acréscimo das orientações locais na seção “Complemento para Esta Turma”. Os arquivos de código inicial são os distribuídos pelo CS50; o gabarito e o script de testes são complementos desta atividade.

O material original e esta tradução e adaptação são disponibilizados sob a [Licença Internacional Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), conforme a [licença do curso](https://cs50.harvard.edu/ai/license/).
