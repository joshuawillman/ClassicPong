# add acceleration to ball over time
# Add sound when ball hits player
# Add sound if score
# Respawn ball if goes pass player with delay
# Add music
# Add game menu
# Add end game screen that says which player won
# BUG = Collision when ball hits top of player

# import necessary packages
import pygame as pg, sys, random
from pygame import *

WINDOWWIDTH = 1000
WINDOWHEIGHT = 740 # includes space for scoreboard
FPS = 30

TITLE = "PONG"
PLAYERSPEED = 15

# colors 
BLACK = (0,0,0)
BLUE = (96,225,244)
PINK = (244,122,96)
WHITEGREY = (238,234,238)
GREYBLUE = (155,166,167)
GREY = (94,92,94)

# initialize pygame and create window
pg.init()
DISPLAYSURF = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pg.display.set_caption(TITLE)

FPSCLOCK = pg.time.Clock() # For syncing the FPS

class BluePlayer(pg.sprite.Sprite):
    ''' create blue (left) player'''
    def __init__(self, width, height):
        super().__init__()

        # Create the player with width, height and color attributes
        self.image = pg.Surface([width, height])
        self.image.fill(BLUE)

        # Draw blue player
        self.rect = self.image.get_rect()

        # Create player variables
        self.changey = 0

    def move_up(self, move_y):
        '''move player up'''
        self.changey -= move_y

    def move_down(self, move_y):
        '''move player up'''
        self.changey += move_y

    def update(self):
        '''update player movement'''
        self.rect.y += self.changey

        '''boundary checking'''
        if self.rect.y <= 40:
            self.rect.y = 40

        if self.rect.y > WINDOWHEIGHT - self.rect.height:
            self.rect.y = WINDOWHEIGHT - self.rect.height

class PinkPlayer(pg.sprite.Sprite):
    ''' create blue (left) player'''
    def __init__(self, width, height):
        super().__init__()

        # Create the player with width, height and color attributes
        self.image = pg.Surface([width, height])
        self.image.fill(PINK)

        # Draw blue player
        self.rect = self.image.get_rect()

        # Create player variables
        self.changey = 0

    def move_up(self, move_y):
        '''move player up'''
        self.changey -= move_y

    def move_down(self, move_y):
        '''move player up'''
        self.changey += move_y

    def update(self):
        '''update player movement'''
        self.rect.y += self.changey

        '''boundary checking'''
        if self.rect.y <= 40:
            self.rect.y = 40

        if self.rect.y > WINDOWHEIGHT - self.rect.height:
            self.rect.y = WINDOWHEIGHT - self.rect.height

class Ball(pg.sprite.Sprite):
    ''' create ball '''
    def __init__(self):
        super().__init__()

        # create image of ball
        self.image = pg.Surface([20,20])
        self.image.fill(GREYBLUE)

        # draw image
        self.rect = self.image.get_rect()
        # spawn location
        self.rect.centerx = WINDOWWIDTH / 2
        self.rect.centery = WINDOWHEIGHT / 2 
        
        # set the direction of the ball to a random direction
        direction = random.choice(["leftdown", "rightdown", 
                                   "leftup", "rightup"])
        self.direct = direction
    
        # speed variables
        self.changex = random.randint(6, 9)
        self.changey = random.randint(3, 5)

        # Keep track of score
        self.blue_score = 0
        self.pink_score = 0
        self.goal = False
    
    def update(self):
        '''update ball movement'''
        if self.direct == 'leftdown':
            self.rect.x += self.changex
            self.rect.y -= self.changey
        if self.direct == 'leftup':
            self.rect.x -= self.changex
            self.rect.y -= self.changey
        if self.direct == 'rightdown':
            self.rect.x += self.changex
            self.rect.y += self.changey
        if self.direct == 'rightup':
            self.rect.x -= self.changex
            self.rect.y += self.changey

        # boundary checking
        if self.rect.top <= 40 or self.rect.bottom >= WINDOWHEIGHT:
            self.changey *= -1
        # scoring and boundary checking
        if self.rect.left > WINDOWWIDTH + 100:
            self.blue_score += 1
            self.goal = True
            self.kill()
        if self.rect.right < 0 - 100:
            self.pink_score += 1
            self.goal = True
            self.kill()

class OutOfBounds(pg.sprite.Sprite):
    pass

def show_start_screen():
    # game start screen
    DISPLAYSURF.fill(WHITEGREY)
    draw_text(DISPLAYSURF, TITLE, 100, WINDOWWIDTH / 2, WINDOWHEIGHT / 4, GREY)
    pg.display.update()
    wait_for_key() 

def wait_for_key():
    # pause for key event
    waiting = True
    while waiting:
        FPSCLOCK.tick(100)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                waiting = False

def draw_text(surface, text, size, x, y, color):
    '''draw text to screen'''
    font = pg.font.Font(pg.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# load images
logo = pg.image.load('logo.png').convert_alpha()
logo_rect = logo.get_rect(center=(WINDOWWIDTH/2, WINDOWHEIGHT/2 + 20))

running = True
show_menu = True
while running: # main game loop
    if show_menu:
        show_start_screen()
        pg.time.delay(1500)

        show_menu = False

        # List that contains all sprites in the game
        active_sprites_list = pg.sprite.Group()
        # create list to store ball
        balls = pg.sprite.Group()

        # Spawn players and set starting locations
        blue = BluePlayer(20, 100)
        blue.rect.x = 25
        blue.rect.y = (WINDOWHEIGHT / 2 - blue.rect.centery) + 20

        pink = PinkPlayer(20, 100)
        pink.rect.x = WINDOWWIDTH - 45
        pink.rect.y = (WINDOWHEIGHT / 2 - pink.rect.centery) + 20

        ball = Ball()

        # Add sprites to the list of objects
        active_sprites_list.add(blue, pink, ball)
        balls.add(ball)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                pink.move_up(PLAYERSPEED)
            if event.key == pg.K_DOWN:
                pink.move_down(PLAYERSPEED)
            if event.key == pg.K_w:
                blue.move_up(PLAYERSPEED)
            if event.key == pg.K_s:
                blue.move_down(PLAYERSPEED)

        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                pink.move_up(-PLAYERSPEED)
            if event.key == pg.K_DOWN:
                pink.move_down(-PLAYERSPEED)
            if event.key == pg.K_w:
                blue.move_up(-PLAYERSPEED)
            if event.key == pg.K_s:
                blue.move_down(-PLAYERSPEED)

    # Game logic goes here
    active_sprites_list.update()
    balls.update()

    # Collision detection
    # check for collision between blue player and ball
    blue_hit = pg.sprite.collide_rect(ball, blue)
    if blue_hit:
        ball.changex *= -1

    # check for collision between blue player and ball
    pink_hit = pg.sprite.collide_rect(ball, pink)
    if pink_hit:
        ball.changex *= -1

    # return to menu
    if ball.pink_score == 10 or ball.blue_score == 10:
        show_menu = True

    # Drawing code goes here
    DISPLAYSURF.fill(WHITEGREY)
    # draw logo and game field
    DISPLAYSURF.blit(logo, logo_rect)
    pg.draw.rect(DISPLAYSURF, GREY, (10, 50, WINDOWWIDTH - 20, WINDOWHEIGHT - 60), 4)
    pg.draw.line(DISPLAYSURF, GREY, ((WINDOWWIDTH/2) - 2, 50), ((WINDOWWIDTH/2) - 2, 290), 4)
    pg.draw.line(DISPLAYSURF, GREY, ((WINDOWWIDTH/2) - 2, WINDOWHEIGHT - 250), ((WINDOWWIDTH/2) - 2, WINDOWHEIGHT - 10), 4)
    pg.draw.circle(DISPLAYSURF, GREY, [WINDOWWIDTH//2, (WINDOWHEIGHT//2) + 20], 100, 4)

    # Display scoreboard
    pg.draw.rect(DISPLAYSURF, GREY, (0,0,WINDOWWIDTH,40))

    # Display scores
    draw_text(DISPLAYSURF, "SCORE: ", 35, WINDOWWIDTH / 4, 10, BLUE)
    draw_text(DISPLAYSURF, str(ball.blue_score), 35, WINDOWWIDTH / 4 + 60, 10, BLUE)
    draw_text(DISPLAYSURF, "SCORE: ", 35, (WINDOWWIDTH / 4 + WINDOWWIDTH / 2), 10, PINK)
    draw_text(DISPLAYSURF, str(ball.pink_score), 35, (WINDOWWIDTH / 4 + WINDOWWIDTH / 2) + 60, 10, PINK)

    # Draw sprites at once all/refresh the position of the player
    active_sprites_list.draw(DISPLAYSURF)

    pg.display.update()
    FPSCLOCK.tick(FPS) # limit frames per second
