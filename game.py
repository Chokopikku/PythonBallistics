import pygame, sys
from pygame.locals import *
from math import *

# Define Constants
WIDTH = 1366
HEIGHT = 768
FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0, 0, 128)
GREEN = (0, 255, 0)
G = -20 # gravitational constant

# Catapult variables
cw_x = 255
cw_y = 620
ball_x = 75
ball_y = 600
rot_speed = 2

# Physics
t = 0 # time
s = (ball_x, ball_y) # space
si = s # space_initial
vi = 100 # velocity_initial
vx = 0 # velocity_x_axis / horizontal
vy = 0 # velocity_y_axis / vertical
v = 0 # instant velocity
theta = 0 # launch angle
travel = False # is travelling

# Initialize Pygame and create game window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movimento Balístico")

# For setting FPS
clock = pygame.time.Clock()


# Define catapult model and size
orig_catapult = pygame.image.load("assets/catapult.png")
orig_catapult = pygame.transform.scale(orig_catapult, (200, 20))
catapult_base = pygame.image.load("assets/catapult_base.png")
catapult_base = pygame.transform.scale(catapult_base, (150, 120))
orig_cw = pygame.image.load("assets/catapult_cw.png")
orig_cw = pygame.transform.scale(orig_cw, (30, 40))
ballImg = pygame.image.load('assets/rock.png')
ballImg = pygame.transform.scale(ballImg, (30, 30))

# Make background transparent while rotating
orig_catapult.set_colorkey(BLACK)
orig_cw.set_colorkey(BLACK)

# Make a copy of the image for smooth rotation
catapult = orig_catapult.copy()
cw = orig_cw.copy()
ball = ballImg.copy()
# Define rect to place the catapult at desired position
catapult_rect = catapult.get_rect()
catapult_rect.center = (180, 630)

cw_rect = cw.get_rect()
ball_rect = ball.get_rect()


# Game loop
running = True
while running:
    # Set FPS
    clock.tick(FPS)
    # Clear Screen before drawing
    screen.fill(BLACK)

    # Check for Exit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not travel:

        # Make a copy of the original center of the catapult
        old_catapult_center = catapult_rect.center

        keys = pygame.key.get_pressed()

        # Define an angle for the rotation
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and theta < 45:
            theta = (theta + rot_speed) % 360
            cw_x -= 0.5
            cw_y -= 3
            ball_x += 0.5
            ball_y +=3

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and theta > 0:
            theta = (theta - rot_speed) % 360
            cw_x += 0.5
            cw_y += 3
            ball_x -= 0.5
            ball_y -= 3
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and vi > 50:
            vi -= 1
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and vi < 200:
            vi += 1
        if keys[pygame.K_SPACE]:
            s = (100, 500)
            si = s
            v = 0
            t = 0
            travel = True
            # set the initial velocity
            vx = vi * cos(radians(theta))
            vy = vi * sin(radians(theta))

        # Rotate the original image
        new_catapult = pygame.transform.rotate(orig_catapult, theta)
        catapult_rect = new_catapult.get_rect()
        # Set the new center to the old center
        catapult_rect.center = old_catapult_center

    else:
        t += clock.get_time()/1000
        s = (si[0] + (vx*t)*2 , si[1] - (((vy*t) + (0.5*G*t*t)))*2) # *2 for pixel-to-meter ratio adjustment
        v = sqrt(pow(vx, 2) + pow(vy, 2))
        screen.fill((0, 0, 0))
        screen.blit(ballImg, s)

        if s[1] >= 630: # ground collision
            travel = False
            vx = 0
            vy = 0
            vi = 50
            v = 0
            s = (ball_x, ball_y)
            si = s
            t = 0

    # Set information text
    font = pygame.font.Font('freesansbold.ttf', 20)

    text_theta = font.render("theta = %d" % theta, True, WHITE)
    text_theta_pos = (10, 20)
    text_vi = font.render("vi = %.1f m/s" % vi, True, WHITE)
    text_vi_pos = (10, 40)
    text_vx = font.render("vx = %.1f m/s" % vx, True, WHITE)
    text_vx_pos = (10, 60)
    text_vy = font.render("vy = %.1f m/s" % vy, True, WHITE)
    text_vy_pos = (10, 80)
    text_v = font.render("v = %.1f m/s" % v, True, WHITE)
    text_v_pos = (10, 100)
    text_x = font.render("x = %.1f m" % s[0], True, WHITE)
    text_x_pos = (10, 120)
    text_y = font.render("y = %.1f m" % (si[1] + (((vy*t) + (0.5*G*t*t)))), True, WHITE)
    text_y_pos = (10, 140)
    text_t = font.render("t = %.1f s" % t, True, WHITE)
    text_t_pos = (10, 160)

    # Draw the new Scene
    screen.blit(text_t, text_t_pos)
    screen.blit(text_vi, text_vi_pos)
    screen.blit(text_vx, text_vx_pos)
    screen.blit(text_vy, text_vy_pos)
    screen.blit(text_v, text_v_pos)
    screen.blit(text_x, text_x_pos)
    screen.blit(text_y, text_y_pos)
    screen.blit(text_theta, text_theta_pos)
    screen.blit(new_catapult, catapult_rect)
    screen.blit(cw, (cw_x, cw_y))
    screen.blit(ball, (ball_x, ball_y))
    screen.blit(catapult_base, (80, 600))

    # Flip the display after drawing
    pygame.display.flip()

pygame.quit()
