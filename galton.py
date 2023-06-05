import pygame
from random import randrange
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
pymunk.pygame_util.positive_y_is_up = False

RES = WIDTH, HEIGHT = 2900, 980
# 1200,1000
FPS = 60

pygame.init()
surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

space = pymunk.Space()
space.gravity = 0, 8000
ball_mass, ball_radius = 1, 7
segment_thickness = 6
split_thickness = 10
split = WIDTH //2

# for variable proceed to label.png
#galton funnel1
a, b, c, d = 10, 100, 18, 40
x1, x2, x3, x4 = a, split // 2 - c, split // 2 + c, split - a
y1, y2, y3, y4, y5 = b, HEIGHT // 4 - d, HEIGHT // 4, HEIGHT // 2 - 1.5 * b, HEIGHT - 4 * b
L1, L2, L3, L4 = (x1, -100), (x1, y1), (x2, y2), (x2, y3)
R1, R2, R3, R4 = (x4, -100), (x4, y1), (x3, y2), (x3, y3)
B1, B2 = (0, HEIGHT), (split, HEIGHT)

#galton funnel2 
e, f, g, h = split + 10, 100, 18, 40
x11, x22, x33, x44 = e, WIDTH+ split // 2 - g, WIDTH+ split // 2 + g, WIDTH+ split - e
y11, y22, y33, y44, y55 = f, HEIGHT // 4 - h, HEIGHT // 4, HEIGHT // 2 - 1.5 * f, HEIGHT - 4 * f
L11, L22, L33, L44 = (x11, -100), (x11, y11), (x22, y22), (x22, y33)
R11, R22, R33, R44 = (x44, -100), (x44, y11), (x33, y22), (x33, y33)
#base/floor
B11, B22 = (split, HEIGHT), (WIDTH, HEIGHT)
#split wall
S1, S2 = (split-2, 0), (split, HEIGHT)
#

#----------------------------------------------------------

def create_ball(space):
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = randrange(x1, x4), randrange(-y1, y1)
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.1
    ball_shape.friction = 0.1
    space.add(ball_body, ball_shape)
    return ball_body


def create_segment(from_, to_, thickness, space, color):
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pygame.color.THECOLORS[color]
    space.add(segment_shape)


def create_peg(x, y, space, color):
    circle_shape = pymunk.Circle(space.static_body, radius=10, offset=(x, y))
    circle_shape.color = pygame.color.THECOLORS[color]
    circle_shape.elasticity = 0.1
    circle_shape.friction = 0.5
    space.add(circle_shape)

#------call functions------
# pegs
peg_y, step = y4, 80
#                 ^ y intervals
x_step = 80
for i in range(10):
    #           ^ range of y axis
    peg_x = -1.5 * step if i % 2 else -step
    for j in range(split // step + 2):
        #           ^ range for x
        create_peg(peg_x, peg_y, space, 'darkslateblue')
        if i == 9:
            create_segment((peg_x, peg_y + 50), (peg_x, HEIGHT), segment_thickness, space, 'darkslategray')
        peg_x += step
    peg_y += 0.3 * step


#pegs & walls galton 2
peg_y2, step = y44, 60
#                   ^y intervals
for i in range(10):
    #           ^ range of y axis
    peg_x2 = split + 0.5 * step if i % 2 else split+step
    for j in range(split // step + 2):
        #           ^ range for x axis
        create_peg(peg_x2, peg_y2, space, 'darkslateblue')
        if i == 9:
            create_segment((peg_x2, peg_y2 + 50), (peg_x2, HEIGHT), segment_thickness, space, 'darkslategray')
        peg_x2 += step
    peg_y2 += 0.5 * step



#open label.png to view coord
# ball basket, the funnel #1
platforms1 = (L1, L2), (L2, L3), (L3, L4), (R1, R2), (R2, R3), (R3, R4), (S1, S2)
for platform1 in platforms1:
    create_segment(*platform1, segment_thickness, space, 'darkolivegreen')
    #floor
create_segment(B1, B2, 20, space, 'darkslategray')

# ball basket, the funnel #2
platforms2 = (L11, L22), (L22, L33), (L33, L44), (R11, R22), (R22, R33), (R33, R44), (S1,S2)
for platform2 in platforms2:
    create_segment(*platform2, segment_thickness, space, 'darkolivegreen')
    #floor
create_segment(B11, B22, 20, space, 'darkslategray')

#split wall
# platforms3 = (S1, S2)
# for platform3 in platforms3:
#     create_segment(*platform3, split_thickness, space, 'red')
#     #floor
create_segment(S1, S2, 9, space, 'red')

# balls
balls = [([randrange(256) for i in range(3)], create_ball(space)) for j in range(600)]


#---main loop---
while True:
    surface.fill(pygame.Color('black'))

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()

    space.step(1 / FPS)
    space.debug_draw(draw_options)

    # [pygame.draw.circle(surface, color, ball.position, ball_radius) for color, ball in balls]
    [pygame.draw.circle(surface, color, (int(ball.position[0]), int(ball.position[1])),
                    ball_radius) for color, ball in balls]
    

    [pygame.draw.circle(surface, color, (int(ball.position[0]), int(ball.position[1])),
                    ball_radius) for color, ball in balls]

    pygame.display.flip()
    clock.tick(FPS)

    #dynamic, kinematic, static
    #dynamic reacts to collisions and affected by forces n gravity, have finite mass, interact w all types of bodies
    #kinematic r managed from your code, not affected by gravity and have infinite mass, such objects can be moved. Example: moving platforms
    #static r not mobile, used as objects of the enviornment.

