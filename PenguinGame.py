#! /C:/Program Files/Python311/
""""! @brief Slider Game made with Pygame from Merlin Tschann and Florian Pieles"""

""""
@file
@brief A Penguin slider game, made with python using the pygame library, from Merlin Tschann and Florian Pieles
The Game is controlled by the keyboard, the goal of the game is to get the penguin through the levels without crashing into the polarbear or one of the walls
"""

##
"""
@mainpage Penguin slider game
This is the documentation of the Penguin Slider Game
"""

#Import the required library (pygame)

import pygame


# Load the pictures, scale the loaded assets
#image of the map
"""
@param map_image background image
@param player_image Penguin image (character, that the player plays)
@param wimg player_image, but rotated into the upward direction when the key w is pressed (player_image is same)
@param player_rect rectangle hitbox for the player
@param simg player_image, but rotated into the downward direction when the key s is pressed
@param dimg player_image, but rotated into the right direction when the key d is pressed
@param aimg player_image, but rotated into the left direction when the key a is pressed
@param maps maplist that contains the maps, that will be loaded into the game (Format: map{number}.txt )
@param enemy_image Polar Bear image (the enemy)
@param heart_width the length of the heart (x-axis)
@param heart_height the length of the heart (y-axis)
@param deadheart_width the length of a lost heart (x-axis)
@param deadheart_height the length of a lost heart (y-axis)
@param heart image of a life (in form of heart)
@param deadheart image of a lost life (in form of a gray heart)
"""
map_image = pygame.image.load("PenguinGame/map.png")
map_image = pygame.transform.scale(map_image, (640, 640))
player_image = pygame.image.load("PenguinGame/penguin1.png")
player_image = pygame.transform.scale(player_image, (60, 75))
wimg = pygame.image.load("PenguinGame/penguin1.png")
wimg = pygame.transform.scale(wimg, (60, 75))
player_rect = player_image.get_rect()
simg = pygame.image.load("PenguinGame/penguins.png")
simg = pygame.transform.scale (simg, (60,75))
dimg = pygame.image.load("PenguinGame/penguind.png")
dimg = pygame.transform.scale(dimg, (80,60))
aimg = pygame.image.load("PenguinGame/penguina.png")
aimg = pygame.transform.scale(aimg, (80,60))
enemy_image = pygame.image.load("PenguinGame\eisbaer.png")
enemy_image = pygame.transform.scale(enemy_image, (80,60))
heart_width = 130
heart_height = 130
deadheart_width = 130
deadheart_height = 130
heart = pygame.image.load("PenguinGame/heart.png")
heart = pygame.transform.scale(heart, (heart_width, heart_height))
deadheart = pygame.image.load("PenguinGame/deadheart.png")
deadheart = pygame.transform.scale(deadheart, (deadheart_width, deadheart_height))

# Generate the maplist, used to load the maps and give the amount of maps used
maps = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]

# initialize the music player, load the music
pygame.mixer.init()
pygame.mixer.music.load("si.mp3")

# Make the music loop an unlimited amount of times
pygame.mixer.music.play(-1)




def pygame_init():
  """!
  Initialize the Pygame library and set up the game screen as well as basic variables
  
  @param screen The size of the game window
  @param breite wideness of the screen
  @param hoehe height of the screen
  @param clock used to controll the frame rate and the time
  @param frames framerate, used to controll the speed of the game (smoothness)
  @param player_speed the speed at which the player (the penguin) moves
  @param dt deltatime
  @param xplayer position, where the player spawns at (x-axis)
  @param yplayer position, where the player spawns at (y-axis)
  @param blocksize size in pixels of the ice cubes
  
  @return screen, breite, hoehe, clock, frames, player_speed, dt, xplayer, yplayer, blocksize
  """
  #Initialize Pygame
  pygame.init()

  screen = pygame.display.set_mode((640, 640))
  breite, hoehe = screen.get_size()
  clock = pygame.time.Clock()
  frames = 60
  player_speed = 300
  dt = 0
  xplayer = 400
  yplayer = 400
  blocksize = 80
  screen.fill("white")
  return screen, breite, hoehe, clock, frames, player_speed, dt, xplayer, yplayer, blocksize

def load_map(level):
    """!
    Load the map, as well as the matrix, that is used as a base for the map (system like tilemap)
    @param map_matrix contains the currently played map, various numbers are used to signal certain things (0 = nothing, 1 = Ice cube, 2 = Finish flag, 3 = Start of the route of the Enemy, 4 = End of the rout of the Enemy)
    @param row a single row that is used to draw the screen
    @return the full matrix of the current map
    """
    map_matrix = []
    with open(f"Maps/map{level}.txt", "r") as f:
        for line in f:
            row = [int(num) for num in line.strip()]
            map_matrix.append(row)
    return map_matrix

def blockmap(screen):
  """!
  Loads the Images of the icecubes, as well as the finish flag
  @param icecube_image image of the icecube
  @param finish_image image of the finishing flag (the goal)
  @return icecube_image, finish_image 
  """
  icecube_image = pygame.image.load("PenguinGame/ice_stone.png")
  icecube_image = pygame.transform.scale(icecube_image, (80, 80))
  finish_image = pygame.image.load("PenguinGame/flag2.png")
  finish_image = pygame.transform.scale(finish_image, (80, 80))
  return icecube_image, finish_image

def icecuberects(map_matrix, icecube_image, finish_image, blocksize, enemy_image):
  """!
  Loads the Icecubes into the map, generates rectangle hit boxes for the ice cubes. Using the numbers from the matrix (0 = nothing, 1 = Ice cube, 2 = Finish flag, 3 = Start of the route of the Enemy, 4 = End of the rout of the Enemy)
  @param icecube_rects list where the icecube with hitboxes are stored in
  @param enemy_start_x startposition of the enemy (x coordinate)
  @param  enemy_start_y startposition of the enemy (y coordinate)
  @param enemy_end_x endposition of the enemy (x coordinate)
  @param enemy_end_y endposition of the enemy (y coordinates)
  @return icecube_rects, icecube_rect, finish_rect, enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y
  """
  icecube_rects = []
  enemy_start_x = -500
  enemy_start_y = -500
  enemy_end_x = -500
  enemy_end_y = -500
  for row in range(len(map_matrix)):
    for col in range(len(map_matrix[row])):
      if map_matrix[row][col] == 1:
        icecube_rect = icecube_image.get_rect()
        icecube_rect.x = col * blocksize
        icecube_rect.y = row * blocksize
        icecube_rects.append(icecube_rect)
      elif map_matrix[row][col] == 2:
        finish_rect = finish_image.get_rect()
        finish_rect.x = col * blocksize
        finish_rect.y = row * blocksize
      elif map_matrix[row][col] == 3:
        enemy_start_x = col * blocksize
        enemy_start_y = row * blocksize
      elif map_matrix[row][col] == 4:
        enemy_end_x = col * blocksize
        enemy_end_y = row * blocksize
  return icecube_rects, icecube_rect, finish_rect, enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y

def blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect):
  """!
  Blites every single icecube in the icecube_rects list
  """
  for rect in icecube_rects:
    screen.blit(icecube_image, rect)
  screen.blit(finish_image, finish_rect)

def draw_map(map_image, screen):
  """!
  Blites the map image
  """
  screen.blit(map_image, (0, 0))

def screen_setup(screen):
  """!
  Updates the Screen and looks for pygame events (single event: pygame.QUIT)
  """
  pygame.display.update()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()

def move(direction_x, direction_y, icecube_rects, screen):
  """!
  Keeps the speed of the Character until he runs into an object, also defines the way the Penguin is moving
  @param new_x the player position (x-axis) + the speed
  @param new_y the player position (y-axis) + the speed
  @param new_rect hitbox of the character while moving
  @param collision a bool, that activates when the character has hit something
  @param player_rect.x new name for new_x
  @param player_rect.y new name for new_y
  @return collision
  """
  blocksize = 80
  new_x = player_rect.x + direction_x
  new_y = player_rect.y + direction_y
  new_rect = pygame.Rect(new_x, new_y, player_rect.width, player_rect.height)
  collision = False
  for icecube_rect in icecube_rects:
    if new_rect.colliderect(icecube_rect):
      collision = True
      break
    screen.blit(player_image, (player_rect.x, player_rect.y))
  if not collision:
    player_rect.x = new_x
    player_rect.y = new_y
    screen.blit(player_image, (player_rect.x, player_rect.y))
  return collision

def check_in_screen(screen):
    """!
    Checks if the character is in the game window (in px)
    @param breite wideness of the game window (in px)
    @param height height of the gamw window (in px)
    @breite_player wideness of the player (in px)
    @hoehe_player height of the player (in px)
    @return True/False if the character is outside of the screen
    """
    breite, hoehe = screen.get_size()
    breite_player, hoehe_player = player_image.get_size()
    if player_rect.x > breite + breite_player or player_rect.x < 0 - breite_player or player_rect.y > hoehe + hoehe_player or player_rect.y < 0 - hoehe_player:
        player_rect.x = 0
        player_rect.y = 0
        return False
    return True


def move_enemy(enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start):
    """!
    Defines movement of the enemy
    @param i multiplication factor of the speed
    @param enemy_speed speed that the character moves at
    @param enemy_rect hitbox of the enemy
    @param enemy_end_x endposition of the enemy (x coordinate)
    @param enemy_end_y endposition of the enemy (y coordinates)
    @param going_to_start bool that checks, in which direction the enemy is going
    @return going_to_start
    """
    i = 1.2
    enemy_speed = 0.01
    if enemy_rect.x == enemy_end_x and enemy_rect.y == enemy_end_y:
        going_to_start = True
    elif enemy_rect.x == enemy_start_x and enemy_rect.y == enemy_start_y:
        going_to_start = False
    if going_to_start == False:
        enemy_rect.x += enemy_speed * ((enemy_end_x - enemy_start_x) * i)
        enemy_rect.y += enemy_speed * ((enemy_end_y - enemy_start_y) * i)
    else:
        enemy_rect.x -= enemy_speed * ((enemy_end_x - enemy_start_x) * i)
        enemy_rect.y -= enemy_speed * ((enemy_end_y - enemy_start_y) * i)
    screen.blit(enemy_image, enemy_rect)
    return going_to_start

def movement(icecube_rects, w, a, s, d, finish_rect, icecube_image, finish_image, did_win, player_rect, simg, dimg, aimg, direction_y, direction_x, player_speed, lives, heart, deadheart, enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start):
  """!
  Looks if a key is pressed and moves the Character into the direction, also checks if the Character collides with an objects and if the finishing flag was reached. Also manages the lives system (if the Character goes out of screen or into the polar bear, 1 live is lost)
  @param speed speed of the Character
  @param blocksize size of the icecubes
  @param keys variable that looks for the pressed keys
  @param player_image image of the Character
  @param collision a bool, that activates when the character has hit something
  @param did_win a bool, that activates when the character has hit the finishing flag
  @param direction_x direction on x-axis
  @param direction_y direction on y-axis
  @param moving bool, that looks if the character is outside of the screen
  @param lives amount of lives the player has
  @param w a bool that activates if the key w is pressed
  @param a a bool that activates if the key a is pressed
  @param d a bool that activates if the key d is pressed
  @param s a bool that activates if the key s is pressed
  @param enemy_start_x startposition of the enemy (x coordinate)
  @param enemy_start_y startposition of the enemy (y coordinate)
  @param enemy_end_x endposition of the enemy (x coordinate)
  @param enemy_end_y endposition of the enemy (y coordinates)
  @param player_rect hitbox of the character
  @return w, a, s, d, did_win, player_image, lives, enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start
  """
  speed = 10
  blocksize = 80
  keys = pygame.key.get_pressed()
  global player_image
  if keys[pygame.K_w] and w:
    player_image = wimg
    collision = False
    if did_win == False:
       direction_y = -speed
       direction_x = 0
    while collision == False:
      if player_rect.colliderect(finish_rect):
          did_win = True
          collision = True
          direction_x = 0
          direction_y = 0
          break
      else:
        moving = check_in_screen(screen)
        if player_rect.colliderect(enemy_rect):
            lives -= 1
            blitlives(heart, deadheart, lives, screen)
            player_rect.x = 0
            player_rect.y = 0
            direction_x = 0
            direction_y = 0
            break
        draw_map(map_image, screen)
        blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect)
        screen.blit(player_image, (player_rect.x, player_rect.y))
        move_enemy(enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start)
        blitlives(heart, deadheart, lives, screen)
        pygame.display.flip()
        if moving == False:
            direction_x = 0
            direction_y = 0
            lives -= 1
            moving = True  
            break
        collision = move(direction_x, direction_y, icecube_rects, screen)
        pygame.display.flip()
        blitlives(heart, deadheart, lives, screen)
        draw_map(map_image, screen)
        w = False
        a = True
        s = True
        d = True

  elif keys[pygame.K_s] and s:
    player_image = simg
    collision = False
    if did_win == False:
        direction_y = speed
        direction_x = 0
    while collision == False:
      if player_rect.colliderect(finish_rect):
          did_win = True
          collision = True
          direction_x = 0
          direction_y = 0
          break
      else:
        moving = check_in_screen(screen)
        if player_rect.colliderect(enemy_rect):
            lives -= 1
            blitlives(heart, deadheart, lives, screen)
            player_rect.x = 0
            player_rect.y = 0
            direction_x = 0
            direction_y = 0
            break
        draw_map(map_image, screen)
        blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect)
        screen.blit(player_image, (player_rect.x, player_rect.y))
        move_enemy(enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start)
        blitlives(heart, deadheart, lives, screen)
        pygame.display.flip()
        if moving == False:
            direction_x = 0
            direction_y = 0
            lives -= 1
            moving = True  
            break
        collision = move(direction_x, direction_y, icecube_rects, screen)
        pygame.display.flip()
        blitlives(heart, deadheart, lives, screen)
        draw_map(map_image, screen)
        s = False
        w = True
        a = True
        d = True

  elif keys[pygame.K_a] and a:
    player_image = aimg
    collision = False
    if did_win == False:
        direction_y = 0
        direction_x = -speed
    while collision == False:
      if player_rect.colliderect(finish_rect):
          did_win = True
          collision = True
          direction_x = 0
          direction_y = 0
          break
      else:
        moving = check_in_screen(screen)
        if player_rect.colliderect(enemy_rect):
            lives -= 1
            blitlives(heart, deadheart, lives, screen)
            player_rect.x = 0
            player_rect.y = 0
            direction_x = 0
            direction_y = 0
            break
        draw_map(map_image, screen)
        blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect)
        move_enemy(enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start)
        screen.blit(player_image, (player_rect.x, player_rect.y))
        blitlives(heart, deadheart, lives, screen)
        pygame.display.flip()
        if moving == False:
            direction_x = 0
            direction_y = 0
            lives -= 1
            moving = True  
            break
        collision = move(direction_x, direction_y, icecube_rects, screen)
        pygame.display.flip()
        blitlives(heart, deadheart, lives, screen)
        draw_map(map_image, screen)
        a = False
        w = True
        s = True
        d = True

  elif keys[pygame.K_d] and d:
    player_image = dimg
    if did_win == False:
        direction_y = 0
        direction_x = speed
    collision = False
    while collision == False:

      if player_rect.colliderect(finish_rect):
          did_win = True
          collision = True
          direction_x = 0
          direction_y = 0
          break
      else:
        moving = check_in_screen(screen)
        if player_rect.colliderect(enemy_rect):
            lives -= 1
            blitlives(heart, deadheart, lives, screen)
            player_rect.x = 0
            player_rect.y = 0
            direction_x = 0
            direction_y = 0
            break
        draw_map(map_image, screen)
        blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect)
        screen.blit(player_image, (player_rect.x, player_rect.y))
        move_enemy(enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start)
        blitlives(heart, deadheart, lives, screen)
        pygame.display.flip()
        if moving == False:
            direction_x = 0
            direction_y = 0
            lives -= 1
            moving = True  
            break
        collision = move(direction_x, direction_y, icecube_rects, screen)
        pygame.display.flip()
        draw_map(map_image, screen)
        blitlives(heart, deadheart, lives, screen)
        d = False
        w = True
        a = True
        s = True

  return w, a, s, d, did_win, player_image, lives, enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start

def blitlives(heart, deadheart, lives, screen):
    """!
    Blites the Hearts with the lives variable

    """
    for leben in range(lives):
        x = (heart_width-80) * leben
        screen.blit(heart, (x, -15))
    for deadleben in range(lives, 3):
        x = (heart_width-80) * deadleben
        screen.blit(deadheart, (x, -17))
    if lives < 1:
        pygame.quit()
        exit()


def button(screen):
  """!
  Gives the Parameters for a button
  @param button_width length of the button (x-axis)
  @param button_height height of the button
  @param button_color color of the button
  @param button_text text of the button
  @param button_font font for the buttontext
  @param button_text_color color of the buttontext
  @return button_width, button_height, button_color, button_text, button_font, button_text_color
  """
  button_width = 200
  button_height = 100
  button_color = (255, 0, 0)
  button_text = "Start"
  button_font = pygame.font.Font(None, 36)
  button_text_color = (255, 255, 255)
  return button_width, button_height, button_color, button_text, button_font, button_text_color

def main():
    """!
    The function, where everything is executed
    @param enemy_image picture that the enemy uses
    @param direction_y direction on y-axis for character
    @param direction_x direction on x-axis for character
    @param lives amount of lives the player has
    @param running the variable that lets the code execute
    @param did_win checks if the character has collided with the finish flag
    @param player_speed speed that the character moves at
    @param w @param w a bool that activates if the key w is pressed
    @param a a bool that activates if the key a is pressed
    @param d a bool that activates if the key d is pressed
    @param s a bool that activates if the key s is pressed
    @param button_x width of the button
    @param button_y height of the button
    @param mouse_pos position of the mouse cursor
    @param map_matrix contains the currently played map, various numbers are used to signal certain things (0 = nothing, 1 = Ice cube, 2 = Finish flag, 3 = Start of the route of the Enemy, 4 = End of the rout of the Enemy)
    @param enemy_rect hitbox of the enemy
    @param going_to_start bool that checks, in which direction the enemy is going
    """
    global enemy_image
    direction_y = 0
    direction_x = 0
    lives = 3
    running = True
    screen, breite, hoehe, clock, frames, player_speed, dt, xplayer, yplayer, blocksize = pygame_init()
    icecube_image, finish_image = blockmap(screen)
    button_width, button_height, button_color, button_text, button_font, button_text_color= button(screen)
    enemy_rect = enemy_image.get_rect()
    did_win = False
    player_speed = 40

    w = True
    a = True
    s = True
    d = True
    
    button_x = (screen.get_width() - button_width) // 2
    button_y = (screen.get_height() - button_height) // 2
    while running:
       for event in pygame.event.get ():
          if event.type == pygame.KEYDOWN:
             if pygame.K_ESCAPE:
                pygame.quit()
          if event.type == pygame.MOUSEBUTTONDOWN:
             mouse_pos = pygame.mouse.get_pos()
             if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                for level in range(1,len(maps)):
                    map_matrix = load_map(level)
                    icecube_rects, icecube_rect, finish_rect, enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y = icecuberects(map_matrix, icecube_image, finish_image, blocksize, enemy_image)
                    draw_map(map_image, screen)
                    enemy_rect.x = enemy_start_x
                    enemy_rect.y = enemy_start_y
                    going_to_start = True
                    direction_y = 0
                    direction_x = 0
                    while running:
                      if level > len(maps):
                         pygame.quit()
                         break
                      screen.blit(map_image, (0,0))
                      if player_rect.colliderect(enemy_rect):
                          lives -= 1
                          blitlives(heart, deadheart, lives, screen)
                      if did_win:
                          player_rect.x = 0
                          player_rect.y = 0
                          direction_x = 0
                          direction_y = 0
                          break
                      going_to_start = move_enemy(enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start)
                      w, a, s, d, did_win, player_image, lives, enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start = movement(icecube_rects, w, a, s, d, finish_rect, icecube_image, finish_image, did_win, player_rect, simg, dimg, aimg, direction_y, direction_x, player_speed, lives, heart, deadheart, enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start)
                      if lives == 0:
                          print("Lost")
                          pygame.quit()
                          exit()

                      blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect)
                      screen.blit(player_image, (player_rect.x, player_rect.y))
                      blitlives(heart, deadheart, lives, screen)
                      screen_setup(screen)
                      pygame.display.update()
                    did_win = False
                    player_rect.x = 0
                    player_rect.y = 0
                    w = True
                    a = True
                    s = True
                    d = True
       pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
       text_surface = button_font.render(button_text, True, button_text_color)
       text_rect = text_surface.get_rect(center= (button_x + button_width //2, button_y + button_height //2))
       screen.blit(text_surface, text_rect)
       pygame.display.flip()

        
if __name__ == '__main__':
  main()
pygame.quit()
