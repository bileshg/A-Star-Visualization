import math
import pygame
from enum import Enum
from queue import PriorityQueue


class Color(Enum):
    DEFAULT = (255, 255, 255)
    GRID_LINE = (128, 128, 128)
    START_NODE = (255, 32, 32)
    END_NODE = (32, 32, 255)
    BARRIER = (0, 0, 0)
    OPEN = (0, 255, 0)
    VISITED = (255, 255, 0)
    PATH = (255, 192, 255)


class Cell:

    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = Color.DEFAULT
        self.neighbors = []
        self.width = width

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == Color.VISITED

    def is_open(self):
        return self.color == Color.OPEN

    def is_barrier(self):
        return self.color == Color.BARRIER

    def is_start(self):
        return self.color == Color.START_NODE

    def is_end(self):
        return self.color == Color.END_NODE

    def reset(self):
        self.color = Color.DEFAULT

    def make_start(self):
        self.color = Color.START_NODE

    def make_closed(self):
        self.color = Color.VISITED

    def make_open(self):
        self.color = Color.OPEN

    def make_barrier(self):
        self.color = Color.BARRIER

    def make_end(self):
        self.color = Color.END_NODE

    def make_path(self):
        self.color = Color.PATH

    def draw(self, win):
        pygame.draw.rect(win, self.color.value,
                         (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        return False


class Grid:

    def __init__(self, rows, row_length_in_pixels, pygame_window):
        self.rows = rows
        self.length = row_length_in_pixels
        self.window = pygame_window
        self.spacing = row_length_in_pixels // rows
        self.__cell_matrix = None
        self.create_new_cells()

    def create_new_cells(self):
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.rows):
                spot = Cell(i, j, self.spacing)
                row.append(spot)
            grid.append(row)

        self.__cell_matrix = grid

    def get(self, i, j):
        return self.__cell_matrix[i][j]

    def __draw_grid_lines(self):
        for i in range(self.rows):
            pygame.draw.line(self.window, Color.GRID_LINE.value,
                             (0, i * self.spacing),
                             (self.length, i * self.spacing))
            for j in range(self.rows):
                pygame.draw.line(self.window, Color.GRID_LINE.value,
                                 (j * self.spacing, 0),
                                 (j * self.spacing, self.length))

    def draw(self):
        self.window.fill(Color.DEFAULT.value)

        for row in self.__cell_matrix:
            for cell in row:
                cell.draw(self.window)

        self.__draw_grid_lines()
        pygame.display.update()

    def update_neighbors(self):
        for i in range(self.rows):
            for j in range(self.rows):
                self.get(i, j).neighbors = []
                if self.get(i, j).row < self.rows - 1 and not self.get(
                        i + 1, j).is_barrier():  # DOWN
                    self.get(i, j).neighbors.append(self.get(i + 1, j))

                if self.get(i, j).row > 0 and not self.get(
                        i - 1, j).is_barrier():  # UP
                    self.get(i, j).neighbors.append(self.get(i - 1, j))

                if self.get(i, j).col < self.rows - 1 and not self.get(
                        i, j + 1).is_barrier():  # RIGHT
                    self.get(i, j).neighbors.append(self.get(i, j + 1))

                if self.get(i, j).col > 0 and not self.get(
                        i, j - 1).is_barrier():  # LEFT
                    self.get(i, j).neighbors.append(self.get(i, j - 1))


def heuristic(current, target):
    tx, ty = target
    x, y = current
    dx = abs(tx - x)
    dy = abs(ty - y)
    return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)


def reconstruct_path(came_from, start, end, grid):
    current = came_from[end]
    while current != start:
        current.make_path()
        grid.draw()
        current = came_from[current]


def a_star(visualizer):
    grid = visualizer.grid
    size = grid.rows
    start = visualizer.start
    end = visualizer.end

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {
        grid.get(i, j): math.inf
        for i in range(size) for j in range(size)
    }
    g_score[start] = 0
    f_score = {
        grid.get(i, j): math.inf
        for i in range(size) for j in range(size)
    }
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, start, end, grid)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(
                    neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        grid.draw()

        if current != start:
            current.make_closed()

    return False


class Visualizer:

    def __init__(self, rows=50, size_in_pixels=800, caption='Visualizer'):
        self.rows = rows
        self.window = pygame.display.set_mode((size_in_pixels, size_in_pixels))
        pygame.display.set_caption(caption)
        self.grid = Grid(rows, size_in_pixels, self.window)

        self.start = None
        self.end = None
        self.executed = False

    def __click_helper(self, pos):
        y, x = pos

        row = y // self.grid.spacing
        col = x // self.grid.spacing

        return row, col

    def __process_left_click(self):
        pos = pygame.mouse.get_pos()
        row, col = self.__click_helper(pos)
        current_cell = self.grid.get(row, col)
        if not self.start and current_cell != self.end:
            self.start = current_cell
            self.start.make_start()

        elif not self.end and current_cell != self.start:
            self.end = current_cell
            self.end.make_end()

        elif current_cell not in [self.end, self.start]:
            current_cell.make_barrier()

    def __process_right_click(self):
        pos = pygame.mouse.get_pos()
        row, col = self.__click_helper(pos)
        current_cell = self.grid.get(row, col)
        current_cell.reset()
        if current_cell == self.start:
            self.start = None
        elif current_cell == self.end:
            self.end = None

    def execute(self, func):
        self.executed = True
        while self.executed:
            self.grid.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.executed = False

                if pygame.mouse.get_pressed()[0]:  # LEFT
                    self.__process_left_click()

                elif pygame.mouse.get_pressed()[2]:  # RIGHT
                    self.__process_right_click()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.start and self.end:
                        self.grid.update_neighbors()
                        func(self)

                    if event.key == pygame.K_c:
                        self.start = None
                        self.end = None
                        self.grid.create_new_cells()
        pygame.quit()


def main():
    Visualizer(rows=30,
               size_in_pixels=450,
               caption="A* Path Finding Algorithm").execute(a_star)


if __name__ == '__main__':
    main()
