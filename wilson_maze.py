import pygame
import random

pygame.init()
width, height = 600 + 5, 600 + 5  # 多一点防止边线被挡
cell_size = 20
cols, rows = width // cell_size, height // cell_size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Wilson Maze")


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    # 视觉上打通墙壁
    def remove_wall(self):
        x, y = self.x * cell_size, self.y * cell_size
        if not self.walls["top"]:
            pygame.draw.line(screen, BLACK, (x, y), (x + cell_size, y), 2)
        if not self.walls["right"]:
            pygame.draw.line(screen, BLACK, (x + cell_size, y), (x + cell_size, y + cell_size), 2)
        if not self.walls["bottom"]:
            pygame.draw.line(screen, BLACK, (x + cell_size, y + cell_size), (x, y + cell_size), 2)
        if not self.walls["left"]:
            pygame.draw.line(screen, BLACK, (x, y + cell_size), (x, y), 2)


# 数据上打通墙壁
def del_wall(current_cell, next_cell):
    dx = next_cell.x - current_cell.x
    dy = next_cell.y - current_cell.y
    if dx == 1:  # 下一格在右
        current_cell.walls["right"] = False
        next_cell.walls["left"] = False
    elif dx == -1:  # 下一格在左
        current_cell.walls["left"] = False
        next_cell.walls["right"] = False
    elif dy == 1:  # 下一格在下
        current_cell.walls["bottom"] = False
        next_cell.walls["top"] = False
    elif dy == -1:  # 下一个在上
        current_cell.walls["top"] = False
        next_cell.walls["bottom"] = False


def get_neighbor(grid, cell):
    neighbors = []
    x, y = cell.x, cell.y
    # 仅根据边界获取有效邻居
    if x > 0:
        neighbors.append(grid[x - 1][y])
    if x < cols - 1:
        neighbors.append(grid[x + 1][y])
    if y > 0:
        neighbors.append(grid[x][y - 1])
    if y < rows - 1:
        neighbors.append(grid[x][y + 1])
    return neighbors


def main():
    fps = 50
    clock = pygame.time.Clock()

    grid = [[Cell(col, row) for row in range(rows)] for col in range(cols)]
    screen.fill(BLACK)
    for y in range(30 + 1):
        pygame.draw.line(screen, WHITE, (0, y * 20), (600, y * 20), 2)
    for x in range(30 + 1):
        pygame.draw.line(screen, WHITE, (x * 20, 0), (x * 20, 600), 2)

    unvisited_cells = [grid[x][y] for x in range(cols) for y in range(rows)]
    random_cell = random.choice(unvisited_cells)
    random_cell.visited = True
    unvisited_cells.remove(random_cell)
    # 构造初始连通区域（只有一个点）
    print("Initial cell is randomly picked at {}!".format((random_cell.x, random_cell.y)))

    steps = 0
    running = True
    while running:
        if not unvisited_cells:
            print("Summon finished with {} steps".format(steps))
            clock.tick(1)
        else:
            current_cell = random.choice(unvisited_cells)
            print("A path started in {}!".format((current_cell.x, current_cell.y)))
            path = [current_cell]  # 构造以随机选点为起点的路径

            # 四周游走，直到碰到其他通路（既连通区域）
            while True:
                current_cell = random.choice(get_neighbor(grid, current_cell))
                steps += 1
                if current_cell in path:
                    # 消除环路，确保无环性，以保证两点通路唯一性
                    path = path[:path.index(current_cell)]
                    print("A loop is erased at {}!".format((current_cell.x, current_cell.y)))
                path.append(current_cell)
                if current_cell.visited:
                    break

            for i in range(len(path)):
                if i != 0:
                    del_wall(path[i - 1], path[i])
                if i != len(path) - 1:
                    unvisited_cells.remove(path[i])
                path[i].visited = True
                path[i].remove_wall()
                clock.tick(fps)
                pygame.display.flip()
            print("A path is built ending at {}!".format((current_cell.x, current_cell.y)))

            progress = (1 - len(unvisited_cells) / 900) * 100
            pygame.display.set_caption(f"Wilson Maze - {progress:.2f}%")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


if __name__ == "__main__":
    main()
