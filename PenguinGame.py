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
heart = pygame.image.load("PenguinGame/heart.png")
heart == pygame.transform.scale(heart, (200, 200))
deadheart = pygame.image.load("PenguinGame/deadheart.png")
deadheart == pygame.transform.scale(deadheart, (2000, 2000))

# Generate the maplist, used to load the maps and give the amount of maps used
maps = [1,2,3,4,5,6,7,8,9,10,11]

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
  @param dt
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
  #fill the screen white
  screen.fill("white")
  return screen, breite, hoehe, clock, frames, player_speed, dt, xplayer, yplayer, blocksize

def load_map(level):
    """!
    Load the map, as well as the matrix, that is used as a base for the map (system like tilemap)
    @param map_matrix contains the currently played map, various numbers are used to signal certain things (0 = nothing, 1 = Ice cube, 2 = Finish flag, 3 = Start of the route of the Enemy, 4 = End of the rout of the Enemy)
    @param row a single row that is used to draw the screen
    @return
    """
    map_matrix = []
    with open(f"Maps/map{level}.txt", "r") as f:
        for line in f:
            row = [int(num) for num in line.strip()]
            map_matrix.append(row)
    return map_matrix

def blockmap(screen):
  icecube_image = pygame.image.load("PenguinGame/ice_stone.png")
  icecube_image = pygame.transform.scale(icecube_image, (80, 80))
  finish_image = pygame.image.load("PenguinGame/flag2.png")
  finish_image = pygame.transform.scale(finish_image, (80, 80))

  return icecube_image, finish_image

def icecuberects(map_matrix, icecube_image, finish_image, blocksize, enemy_image):
  icecube_rects = []
  enemy_start_x = 0
  enemy_start_y = 0
  enemy_end_x = 0
  enemy_end_y = 0
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
  try:
      return icecube_rects, icecube_rect, finish_rect, enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y
  except Exception as E:
      print(E)
      return icecube_rects, icecube_rect, finish_rect, 0, 0, 0, 0

def blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect):
  for rect in icecube_rects:
    screen.blit(icecube_image, rect)
  screen.blit(finish_image, finish_rect)

def draw_map(map_image, screen):
  screen.blit(map_image, (0, 0))

def screen_setup(screen):
  pygame.display.update()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()

def move(direction_x, direction_y, icecube_rects, screen):
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
    breite, hoehe = screen.get_size()
    breite_player, hoehe_player = player_image.get_size()
    if player_rect.x > breite + breite_player or player_rect.x < 0 - breite_player or player_rect.y > hoehe + hoehe_player or player_rect.y < 0 - hoehe_player:
        player_rect.x = 0
        player_rect.y = 0
        return False
    return True


def move_enemy(enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start):
    enemy_speed = 0.01
    if enemy_rect.x == enemy_end_x and enemy_rect.y == enemy_end_y:
        going_to_start = True
    elif enemy_rect.x == enemy_start_x and enemy_rect.y == enemy_start_y:
        going_to_start = False
    if going_to_start == False:
        enemy_rect.x += enemy_speed * ((enemy_end_x - enemy_start_x) * 1.2)
        enemy_rect.y += enemy_speed * ((enemy_end_y - enemy_start_y) * 1.2)
    else:
        enemy_rect.x -= enemy_speed * ((enemy_end_x - enemy_start_x) * 1.2)
        enemy_rect.y -= enemy_speed * ((enemy_end_y - enemy_start_y) * 1.2)
    screen.blit(enemy_image, enemy_rect)
    return going_to_start

def movement(icecube_rects, w, a, s, d, screen, finish_rect, icecube_image, finish_image, did_win, player_rect, simg, dimg, aimg, direction_y, direction_x, player_speed, lives, heart, deadheart):
  speed = 40
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
        draw_map(map_image, screen)
        blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect)
        screen.blit(player_image, (player_rect.x, player_rect.y))
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
        draw_map(map_image, screen)
        blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect)
        screen.blit(player_image, (player_rect.x, player_rect.y))
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
        draw_map(map_image, screen)
        blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect)
        screen.blit(player_image, (player_rect.x, player_rect.y))
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
        draw_map(map_image, screen)
        blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect)
        screen.blit(player_image, (player_rect.x, player_rect.y))
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

  return w, a, s, d, did_win, player_image, lives

def blitlives (heart, deadheart, lives, screen):
  if lives == 3:
     screen.blit(heart, (590, 600))
     screen.blit(heart, (600, 600))
     screen.blit(heart, (610, 600))
  elif lives == 2:
     screen.blit(deadheart, (590, 600))
     screen.blit(heart, (600, 600))
     screen.blit(heart, (610, 600))
  elif lives == 1:
     screen.blit(deadheart, (590, 600))
     screen.blit(deadheart, (600, 600))
     screen.blit(heart, (610, 600))
  elif lives == 0:
     pygame.quit()

def button(screen):
  button_width = 200
  button_height = 100
  button_color = (255, 0, 0)
  button_text = "Start"
  button_font = pygame.font.Font(None, 36)
  button_text_color = (255, 255, 255)
  return button_width, button_height, button_color, button_text, button_font, button_text_color

def main():
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

                    while running:
                      if level > len(maps):
                         pygame.quit()
                         break
                      screen.blit(map_image, (0,0))
                      if did_win:
                          player_rect.x = 0
                          player_rect.y = 0
                          direction_x = 0
                          direction_y = 0
                          break
                      w, a, s, d, did_win, player_image, lives = movement(icecube_rects, w, a, s, d, screen, finish_rect, icecube_image, finish_image, did_win, player_rect, simg, dimg, aimg, direction_y, direction_x, player_speed, lives, heart, deadheart)
                      going_to_start = move_enemy(enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start)
                      if lives == 0:
                          print("Lost")
                          pygame.quit()

                      blitlives(heart, deadheart, lives, screen)
                      blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect)
                      screen.blit(player_image, (player_rect.x, player_rect.y))
                      screen_setup(screen)
                      pygame.display.update()
                    did_win = False
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
