# Exercício 2 — Localização de hospitais com busca local

Neste exercício, você implementará *hill climbing* para escolher posições de
hospitais em uma cidade representada por uma grade.

Cada casa e hospital ocupa uma célula. O custo de uma solução é a soma, para
cada casa, da distância de Manhattan até o hospital mais próximo:

```text
distância((r1, c1), (r2, c2)) = |r1 - r2| + |c1 - c2|
```

O objetivo é minimizar esse custo.

## Arquivo a completar

Implemente os trechos marcados com `TODO` em `hospitals.py`, nesta ordem:

### 1. `get_cost`

Para cada casa, calcule a distância até todos os hospitais, selecione a menor
delas e some-a ao custo total.

### 2. `get_neighbors`

Uma posição possui até quatro vizinhas ortogonais: acima, abaixo, à esquerda e
à direita. Retorne apenas posições que:

- estejam dentro dos limites da grade;
- não contenham uma casa;
- não contenham outro hospital.

### 3. `hill_climb`

O estado inicial dos hospitais já é criado aleatoriamente. A partir dele:

1. mova um hospital por vez para cada uma de suas posições vizinhas;
2. calcule o custo de todos os estados gerados;
3. reúna todos os estados empatados com o menor custo;
4. encerre se esse custo não for menor que o custo atual;
5. caso contrário, escolha aleatoriamente um dos melhores estados e continue;
6. respeite o limite opcional `maximum` de iterações.

Não altere `self.hospitals` enquanto estiver enumerando os vizinhos. Crie uma
cópia do conjunto para cada movimento candidato.

Quando `log=True`, mostre o custo de cada melhoria encontrada. Quando
`image_prefix` for informado, gere uma imagem depois de cada movimento usando
`output_image`.

### 4. `random_restart`

Execute `hill_climb` várias vezes, sempre partindo de um novo estado aleatório,
e retorne o conjunto de hospitais com o menor custo encontrado. Use o parâmetro
`maximum` como a quantidade de reinícios.

## Execução

O recurso de imagem usa Pillow. Instale-o, se necessário, e execute o programa
a partir desta pasta, pois os recursos visuais estão em `assets`:

```bash
python -m pip install Pillow
python hospitals.py
```

O programa deverá imprimir uma sequência de custos estritamente decrescente e
criar imagens como `hospitals000.png`, `hospitals001.png` etc. Como o estado
inicial é aleatório, os valores e as posições podem mudar a cada execução.

Para experimentar os reinícios aleatórios, troque temporariamente no `main` a
chamada a `hill_climb` por uma chamada a `random_restart`.

## Critérios de verificação

- O custo nunca aumenta durante uma execução de `hill_climb`.
- Nenhum hospital ocupa uma casa ou sai da grade.
- Cada estado vizinho altera a posição de exatamente um hospital.
- `random_restart` devolve a melhor solução entre todas as execuções.

## Questões para reflexão

- Por que o algoritmo pode parar sem encontrar a melhor solução global?
- Como os reinícios aleatórios ajudam a contornar ótimos locais?
- Que efeito você espera ao permitir movimentos diagonais?
