import random

import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self): #initialize variables here
        super().__init__()
        # Animations
        player_walk1 = pygame.image.load("graphics\Player\p1_walk\PNG\p1_walk03.png").convert_alpha()
        player_walk2 = pygame.image.load("graphics\Player\p1_walk\PNG\p1_walk05.png").convert_alpha()
        player_walk3 = pygame.image.load("graphics\Player\p1_walk\PNG\p1_walk06.png").convert_alpha()
        self.player_jump = pygame.image.load("graphics\Player\p1_jump.png").convert_alpha()
        self.player_walk = [player_walk1, player_walk2, player_walk3]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 310))
        self.gravity = 0
        self.jump_counter = 3

        self.jump_sound = pygame.mixer.Sound("graphics\AudioJump.mp3")
        self.jump_sound.set_volume(0.1)
    def player_input(self):
        keys = pygame.key.get_pressed() #using key.get_pressed() has more delay
        if keys[pygame.K_SPACE] and self.rect.bottom >= 310 and self.jump_counter > 0: #multiple jumps
            self.gravity = -19
            self.jump_counter -= 1
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 310: #when touching the ground
            self.rect.bottom = 310
            self.jump_counter = 3
    def animate(self):
        if self.rect.bottom < 310: self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index > len(player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, spd):
        super().__init__()
        if type == 'fly':
            fly_frame_1 = pygame.image.load("graphics\Enemies\FlyFly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics\Enemies\FlyFly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y = 210
        elif type == 'snail':
            snail_frame_1 = pygame.image.load("graphics\Enemies\snailWalk1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("graphics\Enemies\snailWalk2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y))
        self.spd = spd
        self.type = type
    def animate(self):
        if self.type == 'fly':
            self.animation_index += 0.1
        elif self.type == 'snail':
            self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animate()
        self.rect.x -= 5 + self.spd
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100: self.kill()

def displayScore():
    t = pygame.time.get_ticks() - start_time
    score_surface = font.render(f'Score: {t}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface, score_rect)
    return t
def obstacleMovement(obstacle_list, spd): #obselete
    if obstacle_list:       #runs only if the obstacle_list is filled
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= spd
            if obstacle_rect.bottom == 300: screen.blit(snail_surface, obstacle_rect)
            elif obstacle_rect.bottom == 210: screen.blit(fly_surface, obstacle_rect)
        #Update obstacle list with obstacles who are on the screen or newly generated (ie delete obstacles)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return [] #obs
def collisions(player, obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect): return False
    return True
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle, False): #if True, snail deletes itself upon contact, else False
        obstacle.empty()
        return False
    else: return True
def playerAnimation():
    global player_surface, player_index

    if player_rect.bottom < 310:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]
    #move through the index


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
font = pygame.font.Font("graphics\Pixeltype.ttf", 50)

clock = pygame.time.Clock()
start_time = 0
game_spd = 0
score = 0
game_active = False
bgm = pygame.mixer.Sound("C:\\Users\ed\PycharmProjects\pygameTutorial\graphics\Chicago - In The Country.mp3")
bgm.set_volume(0.5)
bgm.play(loops = -1)
#Groups (OOP)
player = pygame.sprite.GroupSingle() #parent for just Player
player.add(Player())
obstacle = pygame.sprite.Group()
#only add obstacle with when timer event occurs

height = 200
bg_surface = pygame.image.load("graphics\Sky.png").convert()
ground_surface = pygame.image.load("graphics\ground.png").convert()

# score_surface = score_font.render('My Game', False, (64,64,64))
# score_rect = score_surface.get_rect(center = (400, 50))

#Obstacles
obstacle_rect_list = []

#Snail Animations
snail_frame_1 = pygame.image.load("graphics\Enemies\snailWalk1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics\Enemies\snailWalk2.png").convert_alpha()
snail_frame_list = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frame_list[snail_frame_index]

#Fly Animations
fly_frame_1 = pygame.image.load("graphics\Enemies\FlyFly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics\Enemies\FlyFly2.png").convert_alpha()
fly_frame_list = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frame_list[fly_frame_index]

#Player
player_walk1 = pygame.image.load("graphics\Player\p1_walk\PNG\p1_walk03.png").convert_alpha()
player_walk2 = pygame.image.load("graphics\Player\p1_walk\PNG\p1_walk05.png").convert_alpha()
player_walk3 = pygame.image.load("graphics\Player\p1_walk\PNG\p1_walk06.png").convert_alpha()

player_walk = [player_walk1, player_walk2, player_walk3]
player_index = 0
player_jump = pygame.image.load("graphics\Player\p1_jump.png").convert_alpha()

player_surface = player_walk[player_index]

player_rect = player_surface.get_rect(midbottom = (80, 310))
player_gravity = 0
player_jump_counter = 2

#Intro screen
player_stand = pygame.image.load("graphics\Player\p1_stand.png").convert_alpha()
#player_stand = pygame.transform.scale(player_stand, (200, 400))
#player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = font.render('Pixel Runner', False, (111,196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))
game_message = font.render('Press R to starts', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 320))

#Timer
#Plus one to avoid conflict with other events reserved for pygame
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1100)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer, 10000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos): player_gravity = -15
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_jump_counter > 0:
                    player_jump_counter -= 1
                    player_gravity = -19
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            #Event Timers
            if event.type == obstacle_timer:
                obstacle.add(Obstacle(choice(['fly', 'snail', 'snail']), game_spd))
                # rand = randint(0, 2)
                # if rand == 1:
                #     obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1000), 300)))
                # elif rand == 2:
                #     obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1000), 210)))
            if event.type == fly_animation_timer:
                 game_spd += 0
            #     if fly_frame_index == 0: fly_frame_index = 1
            #     else: fly_frame_index = 0
            #     fly_surface = fly_frame_list[fly_frame_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_active = True
                #obstacle_rect_list = []
                obstacle_rect_list.clear()
                player_rect.midbottom = (80, 310)
                player_gravity = 0
                start_time = pygame.time.get_ticks()


    if game_active:
        screen.blit(bg_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # pygame.draw.rect(screen, ('#c0e8ec'), score_rect)
        # pygame.draw.rect(screen, ('#c0e8ec'), score_rect, 10)
        # screen.blit(score_surface, score_rect)
        score = displayScore()

        #Player, Jump counters
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 310:
        #     player_rect.bottom = 310
        #     player_jump_counter = 2
        # playerAnimation()
        # screen.blit(player_surface, player_rect)
        player.draw(screen)
        player.update() #update all the sprites in player
        obstacle.draw(screen)
        obstacle.update()

        #Obstacle Movement
        #obstacle_rect_list = obstacleMovement(obstacle_rect_list, game_spd)

        #Collisions
        #game_active = collisions(player_rect, obstacle_rect_list)
        #if snail_rect.colliderect(player_rect):
        #    game_active = False
        game_active = collision_sprite()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        score_message = font.render(f'Your Score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)
        # key = pygame.key.get_pressed()
        # if key[pygame.K_r]:
        #     game_active = True
        #     snail_rect.x = 800
    pygame.display.update()
    clock.tick(60)