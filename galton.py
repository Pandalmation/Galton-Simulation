import pygame
import pymunk.pygame_util
from random import randrange

#initialize pygame and set up the display
pygame.init()
width, height = 1700, 880
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

#initialize pymunk space and set gravity
space = pymunk.Space()
space.gravity = 0, 9810

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
    
#pegs & walls
peg_y, step = y4, 68
#                 ^ y intervals
for i in range(10):
    #           ^ range of y axis
    peg_x = -1.5 * step if i % 2 else -step
    for j in range(split // step + 2):
        #           ^ range for x
        create_peg(peg_x, peg_y, space, 'darkslateblue')
        if i == 8:
            #create wall
            create_segment((peg_x, peg_y + 95), (peg_x, height), segment_thickness, space, 'darkslategray')
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
            #                                       ^ wall height 
        peg_x2 += step
    peg_y2 += 0.5 * step

#open label.png to view coordinates

#ball floor, the funnel #1
platforms1 = (L1, L2), (L2, L3), (L3, L4), (R1, R2), (R2, R3), (R3, R4)
for platform1 in platforms1:
    create_segment(*platform1, segment_thickness, space, 'darkolivegreen')
    #floor
create_segment(B1, B2, 20, space, 'darkslategray')

#split wall
create_segment(S1, S2, 10, space, 'black')
create_segment(S11, S22, 10, space, 'black')

# ball floor, the funnel #2
platforms2 = (L11, L22), (L22, L33), (L33, L44), (R11, R22), (R22, R33), (R33, R44)
for platform2 in platforms2:
    create_segment(*platform2, segment_thickness, space, 'darkolivegreen')
    #floor
create_segment(B11, B22, 20, space, 'darkslategray')

#button-----------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.default_color = WHITE
        self.pressed_color = GRAY
        self.is_pressed = False
        self.action = action

    def draw(self, surface):
        color = self.pressed_color if self.is_pressed else self.default_color
        pygame.draw.rect(surface, color, self.rect)
        font = pygame.font.Font(None, 50)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.is_pressed:
                self.is_pressed = False
                self.action()

def text(text, x, y):
    font = pygame.font.Font(None, 35)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    #coords
    text_rect.center = (x,y)
    screen.blit(text_surface, text_rect)
    return text_surface,text_rect

def restart():
    restart_balls()
    restart_balls2()

#reset
def reset():
    global balls, num_balls, ball_radius, ball_radius2, ball_mass, ball_mass2
    num_balls = 350
    ball_radius = 7
    ball_radius2 = 7
    ball_mass = 1
    ball_mass2 = 1
    for ball in balls:
        space.remove(ball[0], ball[1])
    balls = []
    for _ in range(num_balls):
        ball = create_ball2(space)
        balls.append(ball)

    global balls2
    for ball in balls2:
        space.remove(ball[0], ball[1])
    balls2 = []
    for _ in range(num_balls):
        ball = create_ball(space)
        balls2.append(ball)
    print("reset")
    print(f"num_ball:{num_balls}")
    print(f"ball_mass:{ball_mass}")
    print(f"ball_radius:{ball_radius}")

#edit ball quantity
def increase_balls():
    global num_balls
    num_balls += 50
    restart_balls()
    restart_balls2()
    print(f"num_ball(+):{num_balls}")

def decrease_balls():
    global num_balls
    if num_balls > 50:
        num_balls -= 50
        restart_balls()
        restart_balls2()
    print(f"num_ball(-):{num_balls}")

#edit mass
def increase_mass():
    global ball_mass, ball_mass2
    ball_mass += 5
    ball_mass2 += 5
    restart()
    print(f"ball_mass(+):{ball_mass}")

def decrease_mass():
    global ball_mass, ball_mass2
    if ball_mass > 6 and ball_mass2 > 6:
        ball_mass -= 5
        ball_mass2 -= 5    
    restart()
    print(f"ball_mass(-):{ball_mass}")

#edit radius
def increase_radius():
    global ball_radius, ball_radius2
    ball_radius += 0.25
    ball_radius2 += 0.25
    restart()
    print(f"ball_radius(+):{ball_radius}")

def decrease_radius():
    global ball_radius, ball_radius2
    if ball_radius > 0 and ball_radius2 > 0:
        ball_radius -= 0.25
        ball_radius2 -= 0.25
    restart()
    print(f"ball_radius(-):{ball_radius}")


#               x,y coords x,y size  text on button
button = Button(1520, 20, 170, 100, "Restart", restart)
button1 = Button(1520, 150, 170, 100, "Reset", reset)
button2 = Button(1520, 310, 70, 50, "+", increase_balls)
button3 = Button(1600, 310, 70, 50, "-", decrease_balls)
button4 = Button(1520, 420, 70, 50, "+", increase_mass)
button5 = Button(1600, 420, 70, 50, "-", decrease_mass)
button6 = Button(1520, 535, 70, 50, "+", increase_radius)
button7 = Button(1600, 535, 70, 50, "-", decrease_radius)

#ball--------------------------------------

#create ball
def create_ball(space):
    moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    body = pymunk.Body(ball_mass, moment)
    body.position = randrange(x1, x4), randrange(-y1, y1)
    shape = pymunk.Circle(body, ball_radius)
    shape.elasticity = 0.1
    shape.friction = 0.1
    space.add(body, shape)
    return body, shape

#list to hold balls
balls = []
#pre-spawn balls
for _ in range(num_balls):
    ball = create_ball(space)
    balls.append(ball)

#create ball2
def create_ball2(space):
    moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    body = pymunk.Body(ball_mass, moment)
    body.position = randrange(x11, x44), randrange(-y11, y11)
    shape = pymunk.Circle(body, ball_radius)
    shape.elasticity = 0.1
    shape.friction = 0.1
    space.add(body, shape)
    return body, shape

#list to hold balls2
balls2 = [] 
#pre-spawn balls2
for _ in range(num_balls):
    ball = create_ball2(space)
    balls2.append(ball)

# Function to restart the balls
def restart_balls():
    global balls
    for ball in balls:
        space.remove(ball[0], ball[1])
    balls = []
    for _ in range(num_balls):
        ball = create_ball2(space)
        balls.append(ball)

def restart_balls2():
    global balls2
    for ball in balls2:
        space.remove(ball[0], ball[1])
    balls2 = []
    for _ in range(num_balls):
        ball = create_ball(space)
        balls2.append(ball)

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        button.handle_event(event)
        button1.handle_event(event)
        button2.handle_event(event)
        button3.handle_event(event)
        button4.handle_event(event)
        button5.handle_event(event)
        button6.handle_event(event)
        button7.handle_event(event)

    screen.fill((0, 0, 0))
    space.step(1 / 60.0)
    space.debug_draw(draw_options)
    button.draw(screen)
    button1.draw(screen)
    button2.draw(screen)
    button3.draw(screen)
    button4.draw(screen)
    button5.draw(screen)
    button6.draw(screen)
    button7.draw(screen)
    text("ball quantities",1600,290)
    text("ball mass",1600,400)
    text("ball radius",1600,510)
    pygame.display.flip()
    clock.tick(60)
