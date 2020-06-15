import pygame

class Enemy():
    def __init__(self, x, y, speed, size):
        self.x = x
        self.y = y
        self.pic = pygame.image.load("../assets/Fish01_A.png")
        self.speed = speed
        self.size = size

        self.pic = pygame.transform.scale(self.pic, (int(self.size*1.25), self.size))
        
    def update(self, screen):
        self.x += self.speed
        screen.blit(self.pic, (self.x, self.y))
                                     

# Start the game
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

backround_pic = pygame.image.load("../assets/Scene_A.png")
player_pic = pygame.image.load("../assets/Fish06_A.png")

player_x = 0
player_y = 0
player_speed = 10
player_size = 30
player_facing_left = False

enemy = Enemy(20, 10, 3, 100)
enemy2 = Enemy(50, 70, 4, 50)

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
        player_facing_left = False
        player_x += player_speed
    if keys[pygame.K_LEFT]:
        player_facing_left = True
        player_x -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_SPACE]:
        player_size += 2
    
    screen.blit(backround_pic, (0, 0))
    enemy.update(screen)
    enemy2.update(screen)

    player_pic_small = pygame.transform.scale(player_pic, (int(player_size*1.25), player_size))    
    if player_facing_left:
        player_pic_small = pygame.transform.flip(player_pic_small, True, False)
    screen.blit(player_pic_small, (player_x, player_y))
    
    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("MY GAME fps: " + str(clock.get_fps()))
