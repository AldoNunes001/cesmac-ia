import random


class Space:

    def __init__(self, height, width, num_hospitals):
        """Create a new state space with given dimensions."""
        self.height = height
        self.width = width
        self.num_hospitals = num_hospitals
        self.houses = set()
        self.hospitals = set()

    def add_house(self, row, col):
        """Add a house at a particular location in state space."""
        self.houses.add((row, col))

    def available_spaces(self):
        """Returns all cells not currently used by a house or hospital."""

        # Consider all possible cells
        candidates = set(
            (row, col)
            for row in range(self.height)
            for col in range(self.width)
        )

        # Remove all houses and hospitals
        for house in self.houses:
            candidates.remove(house)
        for hospital in self.hospitals:
            candidates.remove(hospital)
        return candidates

    def hill_climb(self, maximum=None, image_prefix=None, log=False):
        """Performs hill-climbing to find a solution."""
        count = 0

        # Start by initializing hospitals randomly
        self.hospitals = set()
        for _ in range(self.num_hospitals):
            self.hospitals.add(random.choice(list(self.available_spaces())))
        if log:
            print("Initial state: cost", self.get_cost(self.hospitals))
        if image_prefix:
            self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")

        # TODO 1: repita a busca até atingir `maximum` ou um ótimo local.
        # TODO 2: gere todos os estados vizinhos movendo um hospital por vez.
        # TODO 3: encontre os vizinhos de menor custo e trate empates.
        # TODO 4: avance somente quando houver melhora e gere a imagem da etapa.
        raise NotImplementedError("Implemente o algoritmo hill climbing.")

    def random_restart(self, maximum, image_prefix=None, log=False):
        """Repeats hill-climbing multiple times and returns the best result."""

        # TODO 1: execute hill_climb `maximum` vezes.
        # TODO 2: calcule o custo de cada resultado e retenha o melhor.
        # TODO 3: respeite os parâmetros `log` e `image_prefix`.
        raise NotImplementedError("Implemente o hill climbing com reinícios.")

    def get_cost(self, hospitals):
        """Calculates sum of distances from houses to nearest hospital."""

        # TODO: some, para cada casa, a distância de Manhattan até o hospital
        # mais próximo.
        raise NotImplementedError("Implemente o cálculo do custo.")

    def get_neighbors(self, row, col):
        """Returns neighbors not already containing a house or hospital."""

        # TODO: retorne as posições ortogonais válidas, dentro do tabuleiro e
        # que não estejam ocupadas por casas ou hospitais.
        raise NotImplementedError("Implemente a geração de vizinhos.")

    def output_image(self, filename):
        """Generates image with all houses and hospitals."""
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        cost_size = 40
        padding = 10

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (
                self.width * cell_size,
                self.height * cell_size + cost_size + padding * 2,
            ),
            "white",
        )
        house = Image.open("assets/images/House.png").resize(
            (cell_size, cell_size)
        )
        hospital = Image.open("assets/images/Hospital.png").resize(
            (cell_size, cell_size)
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 30)
        draw = ImageDraw.Draw(img)

        for i in range(self.height):
            for j in range(self.width):

                # Draw cell
                rect = [
                    (
                        j * cell_size + cell_border,
                        i * cell_size + cell_border,
                    ),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                draw.rectangle(rect, fill="black")

                if (i, j) in self.houses:
                    img.paste(house, rect[0], house)
                if (i, j) in self.hospitals:
                    img.paste(hospital, rect[0], hospital)

        # Add cost
        draw.rectangle(
            (
                0,
                self.height * cell_size,
                self.width * cell_size,
                self.height * cell_size + cost_size + padding * 2,
            ),
            "black",
        )
        draw.text(
            (padding, self.height * cell_size + padding),
            f"Cost: {self.get_cost(self.hospitals)}",
            fill="white",
            font=font,
        )

        img.save(filename)


def main():
    # Create a new space and add houses randomly
    space = Space(height=10, width=20, num_hospitals=3)
    for _ in range(15):
        space.add_house(
            random.randrange(space.height), random.randrange(space.width)
        )

    # Use local search to determine hospital placement
    hospitals = space.hill_climb(image_prefix="hospitals", log=True)
    print("Hospitals:", hospitals)


if __name__ == "__main__":
    main()
