import pygame
import sys
import random
import colorsys

# Configurações iniciais
CONFIG = {
    "WIDTH": 720,
    "HEIGHT": 480,
    "BLOCK_SIZE": 4,
    "ALG_RUN": False,
    "USE_RANDOM_COLOR": False,
    "TAXA_COR": 10,
    "ROWS": lambda: CONFIG["WIDTH"] // CONFIG["BLOCK_SIZE"],
    "COLUMNS": lambda: CONFIG["HEIGHT"] // CONFIG["BLOCK_SIZE"]
}

COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "CIAN": (52, 78, 91),
    "RED": (204, 20, 20),
    "GREEN": (20, 255, 20),
    "YELLOW": (255, 255, 102)
}

# Inicialização do pygame
pygame.init()
display = pygame.display.set_mode((CONFIG["WIDTH"], CONFIG["HEIGHT"]))
clock = pygame.time.Clock()
pygame.display.set_caption("PixelArt")

# Função de texto centralizado
def draw_text(text, font, color, scr, x, y):
    title = font.render(text, True, color)
    scr.blit(title, title.get_rect(center=(x, y)))

# Gerenciamento de cores
def escolhe_cor(cor, taxa_hue=0.05, taxa_lightness=0.1, limite_lightness=(0.2, 0.8)):
    r, g, b = [x / 255.0 for x in cor]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + random.uniform(-taxa_hue, taxa_hue)) % 1.0
    l = max(limite_lightness[0], min(limite_lightness[1], l + random.uniform(-taxa_lightness, taxa_lightness)))
    return tuple(int(x * 255) for x in colorsys.hls_to_rgb(h, l, s))

# Criação da grade de vértices
def make_grid():
    rows, cols = CONFIG["ROWS"](), CONFIG["COLUMNS"]()
    return [[Vortex(i, j, CONFIG["BLOCK_SIZE"], display) for j in range(cols)] for i in range(rows)]

class Vortex:
    def __init__(self, row, col, size, display):
        self.row, self.col = row, col
        self.x, self.y = row * size, col * size
        self.size, self.display = size, display
        self.color, self.is_vortex, self.visited = COLORS["WHITE"], True, False
        self.neighbours = []
        self._define_wall()

    def _define_wall(self):
        if self.row in (0, CONFIG["ROWS"]() - 1) or self.col in (0, CONFIG["COLUMNS"]() - 1):
            self.is_vortex, self.color = False, COLORS["BLACK"]

    def draw(self, color=None):
        color = color or self.color
        pygame.draw.rect(self.display, color, (self.x, self.y, self.size, self.size))

    def update_color(self, color):
        self.color, self.visited = color, True
        self.draw()

    def add_neighbours(self, grid):
        rows, cols = CONFIG["ROWS"](), CONFIG["COLUMNS"]()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = self.row + dr, self.col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc].is_vortex:
                self.neighbours.append(grid[nr][nc])

# Função principal do jogo
def main():
    grid = make_grid()
    start_node, end_node = grid[1][1], grid[CONFIG["ROWS"]() - 2][CONFIG["COLUMNS"]() - 2]
    current_color = COLORS["GREEN"]
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    CONFIG["ALG_RUN"] = not CONFIG["ALG_RUN"]
                elif event.key == pygame.K_c:
                    grid = make_grid()

            if pygame.mouse.get_pressed()[0]:  # Botão esquerdo do mouse
                x, y = pygame.mouse.get_pos()
                row, col = x // CONFIG["BLOCK_SIZE"], y // CONFIG["BLOCK_SIZE"]
                if grid[row][col].is_vortex:
                    grid[row][col].update_color(current_color)

        if CONFIG["ALG_RUN"]:
            # Lógica do algoritmo em andamento (placeholder)
            pass

        display.fill(COLORS["BLACK"])
        for row in grid:
            for vortex in row:
                vortex.draw()

        draw_text("Pressione ESPAÇO para iniciar/parar", pygame.font.Font(None, 30), COLORS["WHITE"], display, CONFIG["WIDTH"] // 2, 20)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
