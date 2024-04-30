import pygame #2D graphics library
# import pygame.image
import os
pygame.font.init()
pygame.mixer.init()

#when you post an event, it gets added to pygame.event.get()
#so instead the for loop just checck for these events

#everything we are using is refered to as surface

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #creates a new window with given width and height
#reason for using all capitals is just for good convention as these are mostly constants

pygame.display.set_caption("First Game!") #this gives your window a title

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) # // for integer division instead of float

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#creating first event loop i.e. something popping up on the screen
#so we create a main function which contains a loop that deals with main game loop 
#i.e. when creating a game, there's a loop which does things like: redrawing the window, checking for collisions (this part is specific to this game), updating the score, etc.

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1 #represents the creation of a custom user event
RED_HIT = pygame.USEREVENT + 2 #we have 2 here because otherwise these would have the same code for an event

# my try idk if this works or not
#YELLOW_SPACESHIP_IMAGE = pygame.image.load('C:/Users/Vyom/Desktop/Python more like ahhhhh/MIni Python Projects/Basic PyGame Game/Assets/spaceship_yellow.png')  
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png')
)
#resizing and rotating the spaceship
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png')
)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

#resizing and rotating the spaceship
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(WHITE) # this will colour the main window
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    #creating font for score
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))


    #.blit used when you wanna draw a surface on the screen
    # i'm gonna update the position using the yellow variable with the help of rectangle
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #originally 300, 100
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) #originally 700, 100

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # but it will not show effect until manually updated using pygame.display.update
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    #we have different methods to do this but we use this one right now because it lets us press multiple keys at the same timea
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: #DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    #we have different methods to do this but we use this one right now because it lets us press multiple keys at the same time
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: #DOWN
        red.y += VEL

#moves bullets, handles collison with bullets, checks collision with wall, checks collision with character
#to check for collision with character we will create an event
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL #moving the bullet right
        if red.colliderect(bullet): #this function helps check if two rectangles are colliding
            #if we collide with character
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL #moving the bullet left
        if yellow.colliderect(bullet): #this function helps check if two rectangles are colliding
            #if we collide with character
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    #Rect -> x, y, width, height
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run: #infinite loop that terminates when game ends 
        clock.tick(FPS)
        for event in pygame.event.get():  #this is the "event loop" that checks for different events occuring in pygame
            if event.type == pygame.QUIT:
                run = False #exits the while loop
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    
    #.quit() uninitializes all pygame modules i.e after you say nthe line pygame.quit() you wont be able to use most of or all pygame function
    #The .QUIT in pygame is used to check if you pressed the cross button on the window which is a pygame event. If you have to quit a window you should press the cross button most of the times.
    # pygame.quit() 
    main()

    #instead of quitting, restart

#this is making sure that we only actually run this main function if we ran this file directly
#this is lowkey difficult to understand so just know that we do this always
if __name__ == "__main__":
    main() 