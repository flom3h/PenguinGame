import pygame
import time

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
maps = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]

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
  return screen, breite, hoehe, clock, frames, player_speed, dt, xplayer, yplayer, blocksize

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

    
def movement(icecube_rects, w, a, s, d, screen, finish_rect, icecube_image, finish_image, did_win, player_rect, simg, dimg, aimg, direction_y, direction_x, player_speed):
  speed = 40
  blocksize = 80
  keys = pygame.key.get_pressed()
  global player_image
  if keys[pygame.K_w] and w:
    player_image = wimg
    if did_win == False:
       direction_y = -speed
       direction_x = 0
       collision = False
    while collision == False:
      if player_rect.colliderect(finish_rect):
          did_win = True
          collision = True
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
            moving = True  
            break
        collision = move(direction_x, direction_y, icecube_rects, screen)
        pygame.display.flip()
        draw_map(map_image, screen)
        w = False
        a = True
        s = True
        d = True

  elif keys[pygame.K_s] and s:
    player_image = simg
    if did_win == False:
        direction_y = speed
        direction_x = 0
    collision = False
    while collision == False:
      if player_rect.colliderect(finish_rect):
          did_win = True
          collision = True
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
            moving = True  
            break
        collision = move(direction_x, direction_y, icecube_rects, screen)
        pygame.display.flip()
        draw_map(map_image, screen)
        s = False
        w = True
        a = True
        d = True

  elif keys[pygame.K_a] and a:
    player_image = aimg
    if did_win == False:
        direction_y = 0
        direction_x = - speed
    collision = False
    while collision == False:
      if player_rect.colliderect(finish_rect):
          did_win = True
          collision = True
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
            moving = True  
            break
        collision = move(direction_x, direction_y, icecube_rects, screen)
        pygame.display.flip()
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
            moving = True  
            break
        collision = move(direction_x, direction_y, icecube_rects, screen)
        pygame.display.flip()
        draw_map(map_image, screen)
        d = False
        w = True
        a = True
        s = True

  return w, a, s, d, did_win, player_image


def main():
    direction_y = 0
    direction_x = 0
    running = True
    screen, breite, hoehe, clock, frames, player_speed, dt, xplayer, yplayer, blocksize = pygame_init()
    icecube_image, finish_image = blockmap(screen)
    enemy_rect = enemy_image.get_rect()
    w = True
    a = True
    s = True
    d = True
    did_win = False
    player_speed = 40
    for level in range(1, len(maps)):
        map_matrix = load_map(level)
        icecube_rects, icecube_rect, finish_rect, enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y = icecuberects(
            map_matrix, icecube_image, finish_image, blocksize, enemy_image)
        draw_map(map_image, screen)
        enemy_rect.x = enemy_start_x
        enemy_rect.y = enemy_start_y
        going_to_start = True
        while running:
            screen.blit(map_image, (0,0))
            if did_win:
                player_rect.x = 0
                player_rect.y = 0
                direction_x = 0
                direction_y = 0
                break
            w, a, s, d, did_win, player_image = movement(icecube_rects, w, a, s, d, screen, finish_rect, icecube_image,
                                                        finish_image, did_win, player_rect, simg, dimg, aimg, direction_y, direction_x, player_speed)
            blitcubes(icecube_rects, screen, icecube_image, finish_image, finish_rect)
            going_to_start = move_enemy(enemy_start_x, enemy_start_y, enemy_end_x, enemy_end_y, enemy_rect, enemy_image, screen, going_to_start)
            screen.blit(player_image, (player_rect.x, player_rect.y))
            screen_setup(screen)
            #pygame.display.flip()
        did_win = False
        w = True
        a = True
        s = True
        d = True


if __name__ == '__main__':
    screen, breite, hoehe, clock, frames, player_speed, dt, xplayer, yplayer, blocksize = pygame_init()
    enemy_image = pygame.image.load("PenguinGame/eisbaer.png")
    enemy_image = pygame.transform.scale(enemy_image, (80, 60))
    main()
    pygame.quit()