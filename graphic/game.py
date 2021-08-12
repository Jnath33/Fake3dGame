from graphic.view import View


def rebase_angle(angle):
    return angle if 0 <= angle < 360 else rebase_angle(angle + 360) if angle < 0 else rebase_angle(angle - 360)


char = {1: "@", 2: "#", 3: "=", 4: "%"}


class Game:
    def __init__(self, game, sx, sy):
        self.game = game
        self.sx, self.sy = sx, sy
        self.x, self.y, self.direction = 0, 0, 0

    def get_view(self):
        return View(self.x, self.y, self.direction, self.game, 70)

    def view(self):
        v = View(self.x, self.y, self.direction, self.game, 70)
        h = 50
        p = ["" for i in range(h + 1)]
        lines = v.get_lines(200)
        lines.reverse()
        for l in lines:
            n = int(h - h * l[0]) / 2
            for i in range(h + 1):
                if n < i < h - n:
                    p[i] += char[l[1]]
                else:
                    p[i] += " "
        print("\n".join(p))

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_dir(self, dir):
        self.direction = rebase_angle(dir)

    def add_x(self, ax):
        self.x = min(max(0, self.x + ax), self.sx)

    def add_y(self, ay):
        self.y = min(max(0, self.y + ay), self.sy)

    def add_dir(self, adir):
        self.direction = rebase_angle(self.direction + adir)
