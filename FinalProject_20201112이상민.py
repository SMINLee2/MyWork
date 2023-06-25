import pygame
import random
import numpy as np

pygame.init()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)
window_width = 1000
window_height = 800
pygame.display.set_caption("PINGPONG:BREAK THE BRICKS!")
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

Fisrtstage_sprites_list = pygame.sprite.Group()
Secondstage_sprites_list = pygame.sprite.Group()
brick_list = pygame.sprite.Group()
ball_list = pygame.sprite.Group()
bar_list = pygame.sprite.Group()
Mbrick_list = pygame.sprite.Group()

class Bar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface([200, 25])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.rect.centerx = window_width/2
        self.rect.y = 775

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 8

        self.rect.x += self.speedx
        
        if self.rect.right > window_width:
            self.rect.right = window_width
        if self.rect.left < 0:
            self.rect.left = 0

class StopBrick(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        rect_width = ((window_width - 70) - 35*(x-1)) / x
        rect_height = ((window_height/3 - 70) - 20*(y-1)) / y
        self.image = pygame.Surface([rect_width,rect_height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([25,25])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, BLACK, self.rect.center, 12.5)
        self.rect.centerx = window_width/2
        self.rect.centery = window_height * 2 / 3

        self.vx = 5
        self.vy = 5
 
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.right > window_width:
            self.rect.right = window_width
            self.vx *= -1
            
        elif self.rect.x < 0:
            self.rect.x = 0
            self.vx *= -1

        elif self.rect.y < 0:
            self.rect.y = 0
            self.vy *= -1

class Moving_Brick(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30,30])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.right > window_width:
            self.rect.right = window_width
            self.vx *= -1
            
        elif self.rect.x < 0:
            self.rect.x = 0
            self.vx *= -1
        
        elif self.rect.bottom > window_height/2:
            self.rect.bottom = window_height/2
            self.vy *= -1
            
        elif self.rect.y < 0:
            self.rect.y = 0
            self.vy *= -1

x_m = 8
y_m = 5
loc_bricks = []
rect_width = ((window_width - 70) - 35*(x_m-1)) / x_m
rect_height = ((window_height/3 - 70) - 20*(y_m-1)) / y_m
for col in range(x_m):
    for row in range(y_m):
        x = col * (rect_width + 35) + 35  # 사각형의 x 좌표
        y = row * (rect_height + 20) + 35  # 사각형의 y 좌표
        loc_bricks.append([x,y])

for i in range(x_m*y_m):
    # This represents a block
    block = StopBrick(x_m,y_m)
    # Set a random location for the block
    block.rect.x = loc_bricks[i][0]
    block.rect.y = loc_bricks[i][1]
    brick_list.add(block)
    Fisrtstage_sprites_list.add(block)

for i in range(5):
    block = Moving_Brick()
    block.rect.centerx = np.random.randint(1000)
    block.rect.y = np.random.randint(0, 365)
    Mbrick_list.add(block)
    Secondstage_sprites_list.add(block)

bar = Bar()
Fisrtstage_sprites_list.add(bar)
Secondstage_sprites_list.add(bar)
bar_list.add(bar)
ball = Ball()
Fisrtstage_sprites_list.add(ball)
Secondstage_sprites_list.add(ball)
ball_list.add(ball)

class GameState:
    def __init__(self):
        self.state = 'intro'
        self.score = 0
        self.missed = 0
        self.game_over = 0        
        self.success = 1
        self.failure = 2


    def initialize_stage(self):
        brick_list.empty()
        Fisrtstage_sprites_list.empty()

        for i in range(x_m * y_m):
            block = StopBrick(x_m, y_m)
            block.rect.x = loc_bricks[i][0]
            block.rect.y = loc_bricks[i][1]
            brick_list.add(block)
            Fisrtstage_sprites_list.add(block)

        Fisrtstage_sprites_list.add(bar)
        Fisrtstage_sprites_list.add(ball)
        
        Mbrick_list.empty()
        Secondstage_sprites_list.empty()

        for i in range(10):
            block = Moving_Brick()
            block.rect.centerx = np.random.randint(1000)
            block.rect.y = np.random.randint(0, 365)
            Mbrick_list.add(block)
            Secondstage_sprites_list.add(block)
        Secondstage_sprites_list.add(bar)
        Secondstage_sprites_list.add(ball)
        self.game_over = 0
        self.missed = 0
        self.score = 0
        
    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'First_Stage'
            
        screen.fill(WHITE)
        Ready = large_font.render('Are you Ready?', True, RED)
        Click = large_font.render('Click it!', True, RED)
        screen.blit(Ready, Ready.get_rect(centerx=window_width // 2, centery=window_height // 2 - 25))
        screen.blit(Click, Click.get_rect(centerx=window_width // 2, centery=window_height // 2 + 25))
        pygame.display.flip()
    
    def First_stage(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                False
    
        # Clear the screen
        screen.fill(WHITE)
    
        # Calls update() method on every sprite in the list
        Fisrtstage_sprites_list.update()

        hits_barck = pygame.sprite.groupcollide(bar_list, ball_list, False, False)
        if hits_barck:
            ball.vy *= -1

        hits_balck = pygame.sprite.groupcollide(ball_list, brick_list, False, True)
        if hits_balck:
            ball.vy *= -1
            self.score += 1

        if ball.rect.top >= window_height:
            self.missed += 1
            ball.vy *= -1
            ball.rect.centerx = window_width/2
            ball.rect.centery = window_height * 2 / 3
    
        Fisrtstage_sprites_list.draw(screen)
        #Fisrtstage_sprites_list.draw(screen)
        if len(brick_list) == 0:
            self.game_over = self.success

        if self.missed >= 3:
            self.game_over = self.failure
        
        score_image = small_font.render('Point {}'.format(self.score), True, BLUE)
        screen.blit(score_image, (10, 10))

        missed_image = small_font.render('Missed {}'.format(self.missed), True, BLUE)
        screen.blit(missed_image, missed_image.get_rect(right=window_width - 10, top=10))
        
        if self.game_over > 0:
            if self.game_over == self.success:
                self.state = 'First_Success'
            elif self.game_over == self.failure:
                self.initial_firststage_sprites_list = pygame.sprite.Group()
                for block in brick_list:
                    self.initial_firststage_sprites_list.add(block)
                    Fisrtstage_sprites_list.add(block)
                self.state = 'Failure'
        pygame.display.flip()
    
    def First_Success(self):
        self.game_over = 0
        self.missed = 0
        self.score = 0
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'Second_Stage'
            
        screen.fill(WHITE)
        success_image = large_font.render('SUCCESS!!', True, RED)
        Ready = large_font.render('Are you ready for next stage?', True, RED)
        Click = large_font.render('Click it!', True, RED)
        screen.blit(success_image, success_image.get_rect(centerx=window_width // 2, centery=window_height // 2 - 50))
        screen.blit(Ready, Ready.get_rect(centerx=window_width // 2, centery=window_height // 2 - 0))
        screen.blit(Click, Click.get_rect(centerx=window_width // 2, centery=window_height // 2 + 50))
        pygame.display.flip()
    
    def Failure(self):
        self.game_over = 0
        self.missed = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.initialize_stage()
                self.state = 'First_Stage'
            
        screen.fill(WHITE)
        success_image = large_font.render('Failure..UU', True, RED)
        Ready = large_font.render('Do you want to try it again?', True, RED)
        Click = large_font.render('Click it!', True, RED)
        screen.blit(success_image, success_image.get_rect(centerx=window_width // 2, centery=window_height // 2 - 50))
        screen.blit(Ready, Ready.get_rect(centerx=window_width // 2, centery=window_height // 2 - 0))
        screen.blit(Click, Click.get_rect(centerx=window_width // 2, centery=window_height // 2 + 50))
        pygame.display.flip()
    
    def Second_Stage(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                False
    
        # Clear the screen
        screen.fill(WHITE)
    
        Secondstage_sprites_list.update()
        hits_barck = pygame.sprite.groupcollide(bar_list, ball_list, False, False)
        if hits_barck:
            ball.vy *= -1

        hits_bamck = pygame.sprite.groupcollide(ball_list, Mbrick_list, False, True)
        if hits_bamck:
            ball.vy *= -1
            self.score += 1

        if ball.rect.top >= window_height:
            self.missed += 1
            ball.vy *= -1
            ball.rect.centerx = window_width/2
            ball.rect.centery = window_height * 2 / 3

        #Secondstage_sprites_list_copy.draw(screen)
        Secondstage_sprites_list.draw(screen)

        if len(Mbrick_list) == 0:
            self.game_over = self.success
        
        if self.missed >= 3:
            self.game_over = self.failure
        
        score_image = small_font.render('Point {}'.format(self.score), True, BLUE)
        screen.blit(score_image, (10, 10))

        missed_image = small_font.render('Missed {}'.format(self.missed), True, BLUE)
        screen.blit(missed_image, missed_image.get_rect(right=window_width - 10, top=10))
        
        if self.game_over > 0:
            if self.game_over == self.success:
                self.state = 'End'

            elif self.game_over == self.failure:
                self.state = 'Failure'
        pygame.display.flip()
    
    def End(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.initialize_stage()
                self.state = 'First_Stage'

        self.game_over = 0
        self.missed = 0
        screen.fill(WHITE)
        success_image = large_font.render('YOU ARE BEST CONTROLLER.', True, RED)
        Ready = large_font.render('Do you want to try it again?', True, RED)
        Click = large_font.render('Click it!', True, RED)
        screen.blit(success_image, success_image.get_rect(centerx=window_width // 2, centery=window_height // 2 - 50))
        screen.blit(Ready, Ready.get_rect(centerx=window_width // 2, centery=window_height // 2 - 0))
        screen.blit(Click, Click.get_rect(centerx=window_width // 2, centery=window_height // 2 + 50))
        pygame.display.flip()
        
    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        elif self.state == 'First_Stage':
            self.First_stage()
        elif self.state == 'First_Success':
            self.First_Success()
        elif self.state == 'Failure':
            pygame.init()
            self.Failure()
        elif self.state == 'Second_Stage':
            self.Second_Stage()
        elif self.state == 'End':
            pygame.init()
            self.End()

game_state = GameState()

done = False
while not done:
    game_state.state_manager()
    # Limit to 60 frames per second
    clock.tick(60)