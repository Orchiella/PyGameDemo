import random

import pygame

pygame.init()
width, height = 600 + 5, 600 + 5  # 多一点防止边线被挡
cell_size = 20
cols, rows = width // cell_size, height // cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aldous-Broder Maze")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    # 从视觉上打通墙壁
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

    # 标出/擦除移动子
    def show(self, is_show=True):
        x, y = self.x * cell_size, self.y * cell_size
        pygame.draw.rect(screen, YELLOW if is_show else BLACK, (x + 3, y + 3, (cell_size - 6), (cell_size - 6)))
        # if is_show:
        #     print("Cell in ({},{}) highlighted!".format(self.x, self.y))


# 从数据上打通墙壁
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


def main():
    fps = 5
    clock = pygame.time.Clock()

    screen.fill(BLACK)
    for y in range(30):
        pygame.draw.line(screen, WHITE, (0, y * 20), (600, y * 20), 2)
    for x in range(30):
        pygame.draw.line(screen, WHITE, (x * 20, 0), (x * 20, 600), 2)

    grid = [[Cell(col, row) for row in range(rows)] for col in range(cols)]
    current_cell = grid[random.randint(0, cols - 1)][random.randint(0, rows - 1)]
    current_cell.visited = True
    current_cell.show()
    pygame.display.flip()
    print("Initial cell is randomly picked at {}".format((current_cell.x, current_cell.y)))

    unvisited_cells_num = cols * rows - 1
    steps = 0
    running = True
    while running:
        if unvisited_cells_num == 0:
            print("Summon finished with {} visits".format(steps))
            clock.tick(1)
        else:
            clock.tick(fps)

            last_cell = current_cell  # 仅用于追踪移动子上一个单元，以便擦除原先的移动子，我真服了pygame没有直接移动绘制内容的代码

            neighbors = []
            x, y = current_cell.x, current_cell.y
            # 仅根据边界获取有效邻居
            if x > 0:
                neighbors.append(grid[x - 1][y])
            if x < cols - 1:
                neighbors.append(grid[x + 1][y])
            if y > 0:
                neighbors.append(grid[x][y - 1])
            if y < rows - 1:
                neighbors.append(grid[x][y + 1])
            unvisited_neighbors = [neighbor for neighbor in neighbors if not neighbor.visited]

            if unvisited_neighbors:
                # 随机选择一个未访问的邻居
                next_cell = random.choice(unvisited_neighbors)
                del_wall(current_cell, next_cell)
                next_cell.visited = True
                unvisited_cells_num -= 1
                current_cell = next_cell
                current_cell.remove_wall()
                print("The wall between {} and {} broken".format((current_cell.x, current_cell.y), (next_cell.x,
                                                                                                  next_cell.y)))
            else:
                # 都访问过了，直接随机穿墙
                current_cell = random.choice(neighbors)
                print("The wall between {} and {} passed".format((current_cell.x, current_cell.y), (last_cell.x,
                                                                                                  last_cell.y)))
            current_cell.show()
            last_cell.show(False)
            steps += 1
            progress = (1 - unvisited_cells_num / 900) * 100
            pygame.display.set_caption(f"A-B Maze - {progress:.2f}%")
            pygame.display.flip()  # 刷新屏幕代码一定要放在所有视觉逻辑的最后面！！！
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


if __name__ == "__main__":
    main()
