from maze.maze import Maze
from graphic.game import Game
import math
from PIL import Image, ImageDraw
import time
import pygame
import cairosvg
import io


def load_svg(filename):
    new_bites = cairosvg.svg2png(url=filename)
    byte_io = io.BytesIO(new_bites)
    return pygame.image.load(byte_io)


w, h = 1440, 810
pygame.init()

g_display = pygame.display.set_mode((w, h))
pygame.display.set_caption("GameWithFake3D experience")

running = True

color = {1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 255), 4: (138, 43, 226)}


def current_milli_time():
    return round(time.time() * 1000)


# Maze dimensions (ncols, nrows)
nx, ny = 10, 10
# Maze entry position
ix, iy = 0, 0

maze = Maze(int(nx/2), int(ny/2), ix, iy)
maze.make_maze()

ma_map = [[1 for a in range(nx+1)] for i in range(ny+1)]

ma_map[5][5] = 0

g = Game(ma_map, nx+1, ny+1)
g.set_x(1.5)
g.set_y(1.5)
g.set_dir(-45)

mw, mh = (len(g.game) * 5 + 4) * 4, (len(g.game[0]) * 5 + 4) * 4
img = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.rectangle([(0, 0), (8, mh - 1)], (0, 0, 0, 255))
draw.rectangle([(0, 0), (mw - 1, 8)], (0, 0, 0, 255))
draw.rectangle([(mw - 8, 0), (mw - 1, mh - 1)], (0, 0, 0, 255))
draw.rectangle([(0, mh - 8), (mw - 1, mh - 1)], (0, 0, 0, 255))
for x in range(len(g.game[0])):
    for y in range(len(g.game)):
        if g.game[y][x] == 0:
            draw.rectangle([(8 + 20 * x, 8 + 20 * y), (28 + 20 * x, 28 + 20 * y)], (0, 0, 0, 255))
bg = pygame.image.load("backgroud.png")
img.save("maze.png")

for i in g.game:
    print(i)
maze.write_svg('maze.svg')

last_millis = current_milli_time()

# map_img = load_svg("maze.svg")
map_img = pygame.image.load("maze.png")

while running:
    last_millis, d_millis = current_milli_time(), current_milli_time() - last_millis
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    p_key = pygame.key.get_pressed()
    if p_key[pygame.K_z]:
        d = g.direction
        o_x, o_y = g.x, g.y
        g.add_x(3 * math.cos(math.radians(d)) * d_millis / 1000)
        g.add_y(-3 * math.sin(math.radians(d)) * d_millis / 1000)
        try:
            if g.game[int(g.y)][int(g.x)] == 0:
                g.set_x(o_x)
                g.set_y(o_y)
        except IndexError:
            g.set_x(o_x)
            g.set_y(o_y)
    if p_key[pygame.K_s]:
        d = g.direction
        o_x, o_y = g.x, g.y
        g.add_x(-3 * math.cos(math.radians(d)) * d_millis / 1000)
        g.add_y(3 * math.sin(math.radians(d)) * d_millis / 1000)
        try:
            if g.game[int(g.y)][int(g.x)] == 0:
                g.set_x(o_x)
                g.set_y(o_y)
        except IndexError:
            g.set_x(o_x)
            g.set_y(o_y)
    if p_key[pygame.K_q]:
        g.add_dir(110 * d_millis / 1000)
    if p_key[pygame.K_d]:
        g.add_dir(-110 * d_millis / 1000)
    view = g.get_view()
    i = 0
    g_display.fill((255, 255, 255))
    g_display.blit(bg, (0, 0))
    for l in reversed(view.get_lines(w)):
        n = int(h - h * l[0]) / 2
        pygame.draw.line(g_display, color[l[1]], (i, n), (i, h - n), 1)
        i += 1
    font = pygame.font.SysFont(None, 24)
    co = font.render('x : ' + str(g.x) + '  y : ' + str(g.y), True, (0, 0, 0))
    g_display.blit(co, (20, 20))
    try:
        fps = font.render('fps : ' + str(int(1 / (d_millis / 1000))), True, (0, 0, 0))
    except:
        fps = font.render('fps : 0', True, (0, 0, 0))
    g_display.blit(fps, (20, 40))
    g_display.blit(map_img, (900, 20))
    pygame.display.update()

pygame.quit()

# while True:
#    g.view()
#    if keyboard.is_pressed("z"):
#        d = g.direction
#        g.add_x(1*math.cos(math.radians(d))*d_millis/1000)
#        g.add_y(-1*math.sin(math.radians(d))*d_millis/1000)
#    if keyboard.is_pressed("q"):
#        g.add_dir(30*d_millis/1000)
#    if keyboard.is_pressed("d"):
#        g.add_dir(-30*d_millis/1000)
