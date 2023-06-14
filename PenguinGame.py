import pygame
import pygame_menu
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
maps = [1,2,3,4,5,6,7,8,9,10,11]
heart = pygame.image.load("PenguinGame/heart.png")
heart == pygame.transform.scale(heart, (200, 200))
deadheart = pygame.image.load("PenguinGame/deadheart.png")
deadheart == pygame.transform.scale(deadheart, (2000, 2000))
pygame.mixer.init()
pygame.mixer.music.load("si.mp3")
pygame.mixer.music.play(-1)



def pygame_init():
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
  font = pygame.font.Font(None, 36)
  return screen, breite, hoehe, clock, frames, player_speed, dt, xplayer, yplayer, blocksize, font

def load_map(level):
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

def icecuberects(map_matrix, icecube_image, finish_image, blocksize):
  icecube_rects = []
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
        
  return icecube_rects, icecube_rect, finish_rect

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

def movement(icecube_rects, w, a, s, d, screen, finish_rect, icecube_image, finish_image, did_win, player_rect, simg, dimg, aimg, direction_y, direction_x, player_speed, lives, heart, deadheart):
  speed = 40
  blocksize = 80
  keys = pygame.key.get_pressed()
  global player_image
  if keys[pygame.K_w] and w:
    player_image = wimg
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
    if did_win == False:
        direction_y = 0
        direction_x = -speed
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

def menu_screen(screen, font):
   WHITE = (255, 255, 255)
   BLACK = (0, 0, 0)

   pass
   

def main():
    direction_y = 0
    direction_x = 0
    lives = 3
    running = True
    screen, breite, hoehe, clock, frames, player_speed, dt, xplayer, yplayer, blocksize, font = pygame_init()
    icecube_image, finish_image = blockmap(screen)
    w = True
    a = True
    s = True
    d = True
    
    did_win = False
    player_speed = 40
    for level in range(1,len(maps)):
        map_matrix = load_map(level)
        icecube_rects, icecube_rect, finish_rect = icecuberects(map_matrix, icecube_image, finish_image, blocksize)
        draw_map(map_image, screen)

        while running:
          if did_win:
              player_rect.x = 0
              player_rect.y = 0
              direction_x = 0
              direction_y = 0
              break
          w, a, s, d, did_win, player_image, lives = movement(icecube_rects, w, a, s, d, screen, finish_rect, icecube_image, finish_image, did_win, player_rect, simg, dimg, aimg, direction_y, direction_x, player_speed, lives, heart, deadheart)
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
        
if __name__ == '__main__':
  main()
pygame.quit()
