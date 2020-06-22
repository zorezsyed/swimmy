import pygame
import random   



class Bubble():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(1, 3)
        self.pic = pygame.image.load('assets/Bubble.png')
        self.on_screen = True
        self.pic = pygame.transform.scale(self.pic, (15, 15))

    def update(self, screen):
        self.y -= self.speed
        screen.blit(self.pic, (self.x, self.y))
        if self.y < -self.pic.get_height():
            self.on_screen = False

class Enemy():
    def __init__(self, x, y, speed, size):
        self.x = x
        self.y = y
        self.type = random.randint(0, 3)
        if self.type == 0:
            self.pic = pygame.image.load("assets/Fish01_A.png")
            self.pic2 = pygame.image.load('assets/Fish01_B.png')
        if self.type == 1:
            self.pic = pygame.image.load('assets/Fish02_A.png')
            self.pic2 = pygame.image.load('assets/Fish02_B.png')
        if self.type == 2:
            self.pic = pygame.image.load('assets/Fish03_A.png')
            self.pic2 = pygame.image.load('assets/Fish03_B.png')
        if self.type == 3:
            self.pic = pygame.image.load('assets/Fish04_A.png')
            self.pic2 = pygame.image.load('assets/Fish04_B.png')
        self.speed = speed
        self.size = size
        self.hitbox = pygame .Rect(self.x, self.y, int(self.size*1.25), self.size)
        self.animation_timer_max = 5
        self.animation_timer = self.animation_timer_max
        self.animation_frame = 0

        self.pic = pygame.transform.scale(self.pic, (int(self.size*1.25), self.size))
        self.pic2 = pygame.transform.scale(self.pic2, (int(self.size*1.25), self.size))

        if self.speed < 0:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.pic2 = pygame.transform.flip(self.pic2, True, False)
        
    def update(self, screen):
        self.animation_timer -= 1
        if  self.animation_timer <= 0:
            self.animation_timer = self.animation_timer_max
            self.animation_frame += 1
            if self.animation_frame > 1:
                self.animation_frame = 0
        self.x += self.speed
        self.hitbox.x += self.speed
        # pygame.draw.rect(screen, (255, 255, 255), self.hitbox)
        if self.animation_frame == 0:
            screen.blit(self.pic, (self.x, self.y))
        else:
            screen.blit(self.pic2, (self.x, self.y))                                    

# Start the game
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

backround_pic = pygame.image.load("assets/Scene_A.png")
background_pic2 = pygame.image.load('assets/Scene_B.png')
player_pic = pygame.image.load("assets/zorez_close1nowhitehair.png")
player_pic2 = pygame.image.load("assets/zorez_closenowhitehair.png")
player_eating_pic = pygame.image.load("assets/zorez_open2.png")

player_eating_timer_max = 8
player_eating_timer = 0
player_swimming_timer_max = 8
player_swimming_timer = player_swimming_timer_max
player_swimming_frame = 0

bg_animation_timer_max = 10
bg_animation_timer = bg_animation_timer_max
bg_animation_frame = 0

player_starting_x = 480
player_starting_y = 310
player_starting_size = 30
player_x = player_starting_x
player_y = player_starting_y
player_speed = 0.3
player_speed_x = 0
player_speed_y = 0
player_size = player_starting_size
player_facing_left = True
player_hitbox = pygame.Rect(player_x, player_y, int(player_size*1.25), player_size)
player_alive = False

score = -1
score_font = pygame.font.SysFont('default', 30)
score_text = score_font.render('Score: '+str(score), 1, (255, 255, 255))
play_button_pic = pygame.image.load('assets/BtnPlayIcon.png')
play_button_x = game_width/2 - play_button_pic.get_width()/2
play_button_y = game_height/2 - play_button_pic.get_height()/2

enemy_timer_max = 40
enemy_timer = enemy_timer_max

enemies = []
enemies_to_remove = []

bubbles = []
bubbles_to_remove = []
bubble_timer = 0

# initialize mixer
# pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.mixer.init()
underwater = pygame.mixer.Sound('assets/underwater.wav')
chomp = pygame.mixer.Sound('assets/chomp.wav')
scream = pygame.mixer.Sound('assets/scream.wav')
underwater.play(loops=-1)
# ***************** Loop Land Below *****************
# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_speed_x += player_speed
    if keys[pygame.K_LEFT]:
        player_speed_x -= player_speed
    if keys[pygame.K_DOWN]:
        player_speed_y += player_speed
    if keys[pygame.K_UP]:
        player_speed_y -= player_speed
#    if keys[pygame.K_SPACE]:
#        player_size += 10
    if player_speed_x > 1:
        player_speed_x -= 0.1
    if player_speed_x < -1:
        player_speed_x += 0.1
    if player_speed_y > 1:
        player_speed_y -= 0.1
    if player_speed_y < -1:
        player_speed_y += 0.1
    player_x += player_speed_x
    player_y += player_speed_y
    if player_speed_x > 0:
        player_facing_left = True
    else:
        player_facing_left = False
    if player_x < 0:
        player_x = 0
        player_speed_x = 0
    if player_x > game_width-player_size*1.25:
        player_x = game_width-player_size*1.25
        player_speed_x = 0
    if player_y < 0:
        player_y = 0
        player_speed_y = 0
    if player_y > game_height - player_size:
        player_y = game_height-player_size
        player_speed_y = 0

    bg_animation_timer -= 1
    if bg_animation_timer <= 0:
        bg_animation_frame +=1
        if bg_animation_frame > 1:
            bg_animation_frame = 0
        bg_animation_timer = bg_animation_timer_max

    if bg_animation_frame == 0:
        screen.blit(backround_pic, (0, 0))
    else:
        screen.blit(background_pic2, (0, 0))

    enemy_timer-=1
    if enemy_timer<=0:
        new_enemy_y = random.randint(0, game_height)
        new_enemy_speed = random.randint(2, 5)
        new_enemy_size = random.randint(player_size/2, player_size*2)
        if random.randint(0, 1) == 0:
            enemies.append(Enemy(-new_enemy_size*2, new_enemy_y, new_enemy_speed, new_enemy_size))
        else:
            enemies.append(Enemy(game_width, new_enemy_y, -new_enemy_speed, new_enemy_size))
        enemy_timer = enemy_timer_max

    for enemy in enemies_to_remove:
        enemies.remove(enemy)
    enemies_to_remove = []

    for enemy in enemies:
        enemy.update(screen)
        if enemy.x < -1000 or enemy.x > game_width+1000:
            enemies_to_remove.append(enemy)
    
    bubble_timer -= 1
    if bubble_timer <= 0 and player_alive:
        if player_facing_left:
            bubbles.append(Bubble(player_x + player_size*1.25, player_y))
        else:
            bubbles.append(Bubble(player_x, player_y))
        bubble_timer = random.randint(40, 90)

    for bubble in bubbles:
        if bubble.on_screen:
            bubble.update(screen)
        else:
            bubbles_to_remove.append(bubble)

    for bubble in bubbles_to_remove:
        bubbles.remove(bubble)
    bubbles_to_remove = []
    
    if player_alive:
        player_hitbox.x = player_x
        player_hitbox.y = player_y
        player_hitbox.width = int(player_size*1.25)
        player_hitbox.height = int(player_size)
#        pygame.draw.rect(screen, (255, 255, 255), player_hitbox)

        for enemy in enemies:
            if player_hitbox.colliderect(enemy.hitbox):
                if player_size >= enemy.size:
                    score += enemy.size
                    player_size += 2
                    enemies.remove(enemy)
                    player_eating_timer = player_eating_timer_max
                    chomp.play()
                else:
                    player_alive = False
                    scream.play()

        player_swimming_timer -= 1
        if player_swimming_timer <= 0:
            player_swimming_timer = player_swimming_timer_max
            player_swimming_frame += 1
        if player_swimming_frame > 1:
            player_swimming_frame = 0

        if player_eating_timer > 0: 
            player_pic_small = pygame.transform.scale(player_eating_pic, (int(player_size*1.25), player_size))
            player_eating_timer -= 1
        else:
            if player_swimming_frame == 0:
                player_pic_small = pygame.transform.scale(player_pic, (int(player_size*1.25), player_size))
            else:
                player_pic_small = pygame.transform.scale(player_pic2, (int(player_size*1.25), player_size))
        if player_facing_left:
            player_pic_small = pygame.transform.flip(player_pic_small, True, False)
        screen.blit(player_pic_small, (player_x, player_y))
    
    if player_alive:
        score_text = score_font.render('Score: '+str(score), 1, (255, 255, 255))
    else:
        score_text = score_font.render('Final Score: '+str(score), 1, (255, 255, 255))
    if score >= 0:
        screen.blit(score_text, (30, 30))

    if not player_alive:
        screen.blit(play_button_pic, (play_button_x, play_button_y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if mouse_x > play_button_x and mouse_x < play_button_x + play_button_pic.get_width():
                if mouse_y > play_button_y and mouse_y < play_button_y + play_button_pic.get_height():
                    player_alive = True
                    score = 0
                    player_x = player_starting_x
                    player_y = player_starting_y = 310
                    player_size = player_starting_size = 30
                    player_speed_x = 0
                    player_speed_y = 0
                    for enemy in enemies:
                        enemies_to_remove.append(enemy)
    
    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("MY GAME fps: " + str(clock.get_fps()))
