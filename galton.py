import pygame
import pymunk.pygame_util
from random import randrange
from pymunk.vec2d import Vec2d

#initialize pygame and set up the display
pygame.init()
width, height = 1700, 880
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

#initialize pymunk space and set gravity
space = pymunk.Space()
space.gravity = 0, 8000

#balls parameters
num_balls = 350
ball_radius = 7
ball_mass = 1
#balls2 parameters
ball_mass2, ball_radius2 = 1,7

#wall parameters
segment_thickness = 6
split = width//2-100
split2 = width-200
overlay = 880

#galton funnel
a, b, c, d = 10, 100, 18, 40
x1, x2, x3, x4 = a, split // 2 - c, split // 2 + c, split - a
y1, y2, y3, y4, y5 = b, height // 4 - d, height // 4, height // 2 - 1.5 * b, height - 4 * b
L1, L2, L3, L4 = (x1, -100), (x1, y1), (x2, y2), (x2, y3)
R1, R2, R3, R4 = (x4, -100), (x4, y1), (x3, y2), (x3, y3)
B1, B2 = (0, height), (split, height)

#split wall
S1, S2 = (split, 0), (split, height)
S11,S22 = (split2,0), (split2,height)

#galton funnel2
e, f, g, h = split + 10, 100, 18, 40
x11, x22, x33, x44 = e, split2 - split // 2 - g, split2 - split // 2 + g, split2+split - e
y11, y22, y33, y44, y55 = f, height // 4 - h, height // 4, height // 2 - 1.5 * f, height - 4 * f
L11, L22, L33, L44 = (x11, -100), (x11, y11), (x22, y22), (x22, y33)
R11, R22, R33, R44 = (x44, -100), (x44, y11), (x33, y22), (x33, y33)
B11, B22 = (split, height), (split2, height)

#button
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 50)
        self.border_width = 2
        self.border_color = (255, 255, 255)
        self.button_color = (0, 0, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
#               x,y coords x,y size  text on button
button = Button(1520, 20, 170, 100, "Reset")

#--------------------------------------

#create ball
def create_ball(space):
    moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    body = pymunk.Body(ball_mass, moment)
    body.position = randrange(x1, x4), randrange(-y1, y1)
    shape = pymunk.Circle(body, ball_radius)
    shape.elasticity = 0.1
    space.add(body, shape)
    return body, shape

#create ball2
def create_ball2(space):
    moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    body = pymunk.Body(ball_mass, moment)
    body.position = randrange(x11, x44), randrange(-y11, y11)
    shape = pymunk.Circle(body, ball_radius)
    shape.elasticity = 0.1
    space.add(body, shape)
    return body, shape

#create wall
def create_segment(from_, to_, thickness, space, color):
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pygame.color.THECOLORS[color]
    space.add(segment_shape)

#create peg
def create_peg(x, y, space, color):
    circle_shape = pymunk.Circle(space.static_body, radius=10, offset=(x, y))
    circle_shape.color = pygame.color.THECOLORS[color]
    circle_shape.elasticity = 0.1
    circle_shape.friction = 0.5
    space.add(circle_shape)

#------call functions------
#pegs & walls
peg_y, step = y4, 70
#                 ^ y intervals
for i in range(10):
    #           ^ range of y axis
    peg_x = -1.5 * step if i % 2 else -step
    for j in range(split // step + 2):
        #           ^ range for x
        create_peg(peg_x, peg_y, space, 'darkslateblue')
        if i == 9:
            #create wall
            create_segment((peg_x, peg_y + 50), (peg_x, height), segment_thickness, space, 'darkslategray')
        peg_x += step
    peg_y += 0.5 * step

#pegs & walls galton 2
peg_y2, step = y44, 50
#                   ^y intervals
for i in range(13):
    #           ^ range of y axis
    peg_x2 = split + 0.5 * step if i % 2 else split+step
    for j in range(690 // step + 2):
        #           ^ range for x axis
        create_peg(peg_x2, peg_y2, space, 'darkslateblue')
        if i == 9:
            #create wall
            create_segment((peg_x2, peg_y2 + step + 90), (peg_x2, height), segment_thickness, space, 'darkslategray')
            #                                     ^ wall height 
        peg_x2 += step
    peg_y2 += 0.5 * step

#open label.png to view coordinates

#ball basket, the funnel #1
platforms1 = (L1, L2), (L2, L3), (L3, L4), (R1, R2), (R2, R3), (R3, R4)
for platform1 in platforms1:
    create_segment(*platform1, segment_thickness, space, 'darkolivegreen')
    #floor
create_segment(B1, B2, 20, space, 'darkslategray')

#split wall
create_segment(S1, S2, 9, space, 'red')
create_segment(S11, S22, 9, space, 'yellow')

# ball basket, the funnel #2
platforms2 = (L11, L22), (L22, L33), (L33, L44), (R11, R22), (R22, R33), (R33, R44)
for platform2 in platforms2:
    create_segment(*platform2, segment_thickness, space, 'darkolivegreen')
    #floor
create_segment(B11, B22, 20, space, 'darkslategray')

#list to hold the balls
balls = []
balls2 = []

#pre-spawn balls
for _ in range(num_balls):
    ball = create_ball(space)
    balls.append(ball)

#pre-spawn balls2
for _ in range(num_balls):
    ball = create_ball2(space)
    balls2.append(ball)

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.is_clicked(pygame.mouse.get_pos()):
                #balls1
                #remove balls
                for _ in range(num_balls):
                    ball = balls.pop()
                    space.remove(ball[0], ball[1])
                #spawn balls
                for _ in range(num_balls):
                    ball = create_ball(space)
                    balls.append(ball)

                #balls2
                #remove balls2
                for _ in range(num_balls):
                    ball = balls2.pop()
                    space.remove(ball[0], ball[1])
                #spawn balls2
                for _ in range(num_balls):
                    ball = create_ball2(space)
                    balls2.append(ball)

    #update physics and draw balls and floor
    screen.fill((0, 0, 0))
    space.step(1 / 60.0)
    space.debug_draw(draw_options)
    button.draw(screen)    # Draw the button on the screen
    pygame.display.flip()
    clock.tick(60)