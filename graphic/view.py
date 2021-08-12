import math


def rebase_angle(angle):
    return angle if 0 <= angle < 360 else rebase_angle(angle + 360) if angle < 0 else rebase_angle(angle - 360)


class View:
    def __init__(self, px, py, direction, maze, fov):
        self.px, self.py = px, py
        self.direction = direction
        self.maze = maze
        self.fov = fov

    def get_line_size(self, angle):
        view = rebase_angle(self.direction + angle)
        d = self.calcul_distance(view, self.px, self.py, int(self.px), int(self.py))
        try:
            return 0.98 * min(1, 1 / (d[0] + 1) + 0.1), d[1]
        except ZeroDivisionError:
            return 0.98, d[1]

    def calcul_distance(self, angle, nx, ny, cx, cy, c_dist=0):
        a = math.radians(angle)
        d = 1 if math.cos(a) > 0 else -1, -1 if math.sin(a) > 0 else 1
        x_c = nx - cx
        y_c = ny - cy
        l_x = 1 - x_c if math.cos(a) > 0 else x_c
        l_y = y_c if math.sin(a) > 0 else 1 - y_c
        a_1 = math.radians(angle % 90)
        a_2 = math.radians(90) - a_1
        if a < math.pi / 2 or math.pi < a < math.pi * 3 / 2:
            a_x = a_1
            a_y = a_2
        else:
            a_x = a_2
            a_y = a_1
        if math.sin(a_x) * l_x < math.sin(a_y) * l_y:
            n_dist = c_dist + l_x / math.cos(a_x)
            if cx+d[0] < 0 or cx+d[0] >= len(self.maze[0]) or self.maze[cy][cx + d[0]] == 0:
                return n_dist, 2 + d[0]
            else:
                return self.calcul_distance(angle, cx + int((d[0]+1)/2), math.tan(a_x) * l_x * d[1] + ny, cx + d[0], cy, n_dist)
        elif math.sin(a_x) * l_x > math.sin(a_y) * l_y:
            n_dist = c_dist + l_y / math.cos(a_y)
            if cy+d[1] < 0 or cy+d[1] >= len(self.maze) or self.maze[cy + d[1]][cx] == 0:
                return n_dist, 3 + d[1]
            else:
                return self.calcul_distance(angle, math.tan(a_y) * l_y * d[0] + nx, cy + int((d[1]+1)/2), cx, cy + d[1], n_dist)
        else:
            next_x = int(nx) + d[0]
            next_y = int(ny) + d[1]
            n_dist = c_dist + l_x / math.cos(a_x)
            if next_x < 0 or next_x >= len(self.maze[0]) or next_y < 0 or next_y >= len(self.maze) or self.maze[next_y][
                next_x] == 0 or self.maze[next_y - d[0]][next_x] == 0 or self.maze[next_y][
                next_x - d[1]] == 0:
                return n_dist, 1
            else:
                return self.calcul_distance(angle, next_x, next_y, cx + d[0], cy + d[1], n_dist)

    def get_lines(self, rows=120):
        lines = []
        for i in range(rows):
            lines.append(self.get_line_size(-self.fov / 2 + i * self.fov / rows))
        return lines
