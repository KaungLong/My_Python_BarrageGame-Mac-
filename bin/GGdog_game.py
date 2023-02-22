# sprite

#from email.mime import image
#from gc import garbage

#還需要更新:多彗星互動&分裂、激光炮


from random import random
#from re import S, X
from tkinter import N, X, font
# tokenize import _all_string_prefixes

# from unittest import runner
from numpy import power
# import pygame
import pygame
import random
import os

# print(random.random())
FPS = 60
WIDTH = 500
HEIGHT = 600

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# 係數調整區
Num_rocks = 10
damage_coeff = 1.5
drop_rate = 0.94
rock_live_rate = 10
crazy_mode_sec = 20
# 遊戲初始化＆創建視窗

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("測試用遊戲")

clock = pygame.time.Clock()
tato_img = pygame.image.load(os.path.join("images/tato.ico")).convert()
pygame.display.set_icon(tato_img)


# 載入圖片
background_img = pygame.image.load(os.path.join("images", "background.png")).convert()
player_img = pygame.image.load(os.path.join("images", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(os.path.join("images", "bullet.png")).convert()
missile_img = pygame.image.load(os.path.join("images", "missile.png")).convert()
missile_img.set_colorkey(BLACK)
missile_mini_img = pygame.transform.scale(missile_img, (30, 20))
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("images", f"rock{i}.png")).convert())
expl_anim = {}
expl_anim["lg"] = []
expl_anim["sm"] = []
expl_anim["player"] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("images", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim["lg"].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim["sm"].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("images", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim["player"].append(player_expl_img)
power_imgs = {}
power_imgs["HPup"] = pygame.image.load(os.path.join("images", "shield.png")).convert()
power_imgs["gun"] = pygame.image.load(os.path.join("images", "gun.png")).convert()

barrierIco_img = pygame.image.load(os.path.join("images", "barrier_icon.png")).convert()
power_imgs["barrier"] = pygame.transform.scale(barrierIco_img, (45, 50))
barrier_img = pygame.image.load(os.path.join("images", "barrier.png")).convert()
barrier_img.set_colorkey(WHITE)

# comet_img = pygame.image.load(os.path.join("img", "Big_Comet.png")).convert()
# comet_img.set_colorkey(WHITE)


# 載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
HPup_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
barrier_on_sound = pygame.mixer.Sound(os.path.join("sound", "barrier_on.wav"))
barrier_break_sound = pygame.mixer.Sound(os.path.join("sound", "barrier_break.wav"))
get_hurt_sound = pygame.mixer.Sound(os.path.join("sound", "get_hurt.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.wav"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]

def music_play(song,volume):
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join("sound", song))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

# 載入字體
font_name = os.path.join("tttf/font.ttf")   


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
def new_bullet(x,y):
    direction_mode = [(2,2,-135),(-2,-2,45),(2,-2,-45),(-2,2,135),(0,4,-180),(0,-4,0),(-4,0,-90),(4,0,90)]
    for i in range(8):
        bullet = Bullet(x, y)
        all_sprites.add(bullet)
        bullets.add(bullet)
        bullet.scatter = True
        bullet_way = random.choice(direction_mode)
        bullet.speedx = bullet_way[0]
        bullet.speedy = bullet_way[1]
        bullet.degree = bullet_way[2]
        direction_mode.remove(bullet_way)
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)
def new_pow_from_rocks():
    pow = Power(hit.rect.center)
    all_sprites.add(pow)
    powers.add(pow)
def new_pow_from_god(center):
    pow = Power(center)
    all_sprites.add(pow)
    powers.add(pow)

def draw_background(img,x,y):
    first_BG = screen.blit(img, (x, y))
    #print(first_BG.top)
    if first_BG.top > 0:
        sec_BG = screen.blit(img, (x, y-600))

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 12
    fill = (hp / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_num_missile(surf, num_missile, img, x, y):
    for i in range(num_missile):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "曾嘎曾嘎", 64, WIDTH / 2, HEIGHT / 4 -50)
    draw_text(screen, "← → 移動飛船，使用空白鍵發射子彈", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "按方向鍵下 來開始遊戲", 18, WIDTH / 2, HEIGHT * 3 / 4)
    if game_frist == False:
        draw_text(screen,"本次得分:"+ str(int(score)), 36, WIDTH / 2, HEIGHT / 4+50)
    pygame.display.update()
    watting = True
    while watting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    watting = False
                    return False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun_level = 1 
        self.gun_time = 0
        self.num_missile = 3
        self.missle_reloading_time = 0
    def update(self):
        now = pygame.time.get_ticks()
        if self.gun_level > 1 and now - self.gun_time > 8000:
            self.gun_level -= 1
            self.gun_time = now
        if self.num_missile < 3 and pygame.time.get_ticks()-self.missle_reloading_time >8000:
            self.num_missile += 1
            self.missle_reloading_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hidden_time > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            barrier.protect_on()
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:  
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


    def shoot(self):
        if not (self.hidden):
            if self.gun_level == 1:
                
                bullet1 =Bullet(self.rect.centerx,self.rect.top)
                bullet2 = Bullet(self.rect.centerx, self.rect.bottom)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.gun_level == 2:
                bullet1 = Bullet(self.rect.left, self.rect.top-2)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.gun_level >= 3:
                

                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                bullet3 = Bullet(self.rect.midtop[0],self.rect.midtop[1])
                bullet4 = Bullet(self.rect.midtop[0],self.rect.midtop[1]-10)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3) 
                all_sprites.add(bullet4) 
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
                shoot_sound.play()
    def missile_attack(self):

        if self.num_missile > 0 :
            self.num_missile -= 1

            if not (self.hidden):
                missile = Missile(self.rect.left, self.rect.top+20)
                all_sprites.add(missile)
                missiles.add(missile)

    def hide(self):
        self.hidden = True
        self.hidden_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 500)

    def gunup(self):
        self.gun_level += 1
        self.gun_time = pygame.time.get_ticks()


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-300, -150)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = 1
        self.live = int(self.radius/rock_live_rate)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 0
        self.speedy = -10
        self.scatter = False
        self.num_scatter = 0
        self.degree = 0
    def scattering(self):
        self.image = pygame.transform.rotate(self.image, self.degree)

    def update(self):
        if self.scatter == True:
            self.scattering()
            self.scatter = False
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.bottom < 0) or (self.rect.top>HEIGHT) or (self.rect.left>WIDTH) or (self.rect.right<0)   :
            self.kill()
      
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_img
        self.image = pygame.transform.scale(missile_img, (50, 40))
        self.image = pygame.transform.rotate(self.image, -95)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = -10

    def update(self):
        
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        # 更新到第幾張圖
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        # 動畫的螢幕更新率
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
        
                self.image = expl_anim[self.size][self.frame]
           
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["HPup", "gun","barrier"])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Barrier_(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(barrier_img, (110, 95))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT+300
        self.speedx = 8
        self.radius = 35
        self.protect = False
    def update(self):
        if self.protect == True:
            key_pressed = pygame.key.get_pressed()
            if player.rect.right == WIDTH:#or( self.rect.left <= 0) ):
                self.rect.centerx = player.rect.centerx-3
                self.rect.bottom = player.rect.bottom+28
            if player.rect.left == 0:
                self.rect.centerx = player.rect.centerx-3
                self.rect.bottom = player.rect.bottom+28
            if key_pressed[pygame.K_RIGHT]:
                self.rect.x += self.speedx
            if key_pressed[pygame.K_LEFT]:
                self.rect.x -= self.speedx
    def protect_done(self):
       #print("self.protect")
        self.protect = False
        barrier_break_sound.play()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT+300
    def protect_on(self):
        self.protect = True
        barrier_on_sound.play()
        self.rect.centerx = player.rect.centerx-3
        self.rect.bottom = player.rect.bottom+28

show_init = True
running = True
game_frist = True

# 遊戲迴圈
while running == True:
    if show_init:
        music_play("background.wav",0.4)
        #內含有while迴圈
        close = draw_init()

        if close:
            print("close")
            break
        show_init = False
        # 1秒鐘內最多只能被執行10次
        wave_time_FPS = crazy_mode_sec*62
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()

        powers = pygame.sprite.Group()

        comets = pygame.sprite.Group()
        missiles = pygame.sprite.Group()

        player = Player()

        all_sprites.add(player)
        barrier = Barrier_()
        all_sprites.add(barrier)
        barrier.protect_on()
        bullets = pygame.sprite.Group()
        crazy_mode = True
        grand_battle_now = True
        game_frist = False
        bg_y = 0
        for i in range(Num_rocks):
            new_rock()
        #new_comet()
        score = 0
        

    clock.tick(FPS)
    wave_time_FPS -= 1
    crazy_mode_time = int(wave_time_FPS/60)
    if crazy_mode_time <= 0:
        crazy_mode = False 
    if wave_time_FPS < 0:
        wave_time_FPS = 0

    # 取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_UP :
                player.missile_attack()

    # 更新遊戲
    all_sprites.update()

    #隕石光盾互撞
    hits = pygame.sprite.spritecollide(barrier,rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        #hit.kill()
        expl = Explosion(hit.rect.center, "sm")
        print(hit.rect.center)
        all_sprites.add(expl)
        barrier.protect_done()
        #print("5050")
        new_rock()
        


    # 隕石子彈相撞
    hits = pygame.sprite.groupcollide(rocks, bullets, False, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        hit.live -= 1
        if hit.live <= 0 :
            
            #random.choice(expl_sounds).play()
            score += int((hit.radius+(hit.radius)**0.5*10)/8)
            expl = Explosion(hit.rect.center, "lg") 
            all_sprites.add(expl)
            if random.random() > drop_rate:
                new_pow_from_rocks()
            hit.kill()
            new_rock()
        else:
            score += 1
            expl = Explosion(hit.rect.center,"sm")
            all_sprites.add(expl)
    #飛彈隕石相撞
    hits = pygame.sprite.groupcollide(rocks,missiles, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()

            #random.choice(expl_sounds).play()
        score += int((hit.radius+(hit.radius)**0.5*10)/8)
        expl = Explosion(hit.rect.center, "lg") 
        all_sprites.add(expl)
        
        new_bullet(hit.rect.center[0],hit.rect.center[1])
        if random.random() > drop_rate:
            new_pow_from_rocks()
        #hit.kill()
        new_rock()

    

    # 玩家道具相撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == "HPup":
            player.health += 20
            if player.health > 100:
                score += (player.health-100)
                player.health = 100
            HPup_sound.play()
        elif hit.type == "gun":
            player.gunup()
            gun_sound.play()
        elif hit.type == "barrier":
            if barrier.protect:
                score += 100
            if not barrier.protect:
                barrier.protect = True
                barrier.protect_on()

    # 玩家隕石相撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        expl = Explosion(hit.rect.center, "sm")
        all_sprites.add(expl)
        get_hurt_sound.play()
        new_rock()
        player.health -= hit.radius * damage_coeff
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, "player")
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()
         
    if player.lives < 0 and not (death_expl.alive()):
        show_init = True
        # running = False

    # 畫面顯示
    


    screen.fill(BLACK)
    bg_y += 0.5
    if bg_y == 600:
        bg_y = 0
    draw_background(background_img,0,bg_y)
    #screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen,"score",18,WIDTH/2,0)
    draw_text(screen, str(int(score)), 18, WIDTH / 2, 18)
    draw_health(screen, player.health, 5, 15)
    draw_text(screen,"HP "+str(int(player.health))+"%",18,40,40)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    draw_num_missile(screen, player.num_missile, missile_mini_img, WIDTH - 100, 50)
    if crazy_mode :
        draw_text(screen,"Crazy Mode 倒數："+str(crazy_mode_time)+"s",15,WIDTH/2,40)
    if not crazy_mode:
        draw_text(screen,"Grand Battle Time",25,WIDTH/2,40)
        score_K = int(score/500)
        if grand_battle_now:
            god_center = (random.randrange(50, (WIDTH -50) ),random.randrange(-250,  -50) )
            new_pow_from_god(god_center)
            for i in range(5):
                new_rock()
            music_play("BATTLE.mp3",0.5)
            grand_battle_now = False
            Level = 1
        if score_K >Level:
            print(rocks)
            new_pow_from_god(god_center)
            new_rock()
            new_rock()
            Level += 1
            


    score += (0.001*len(rocks)+(len(rocks)-10)*(0.001)*3)

    pygame.display.update()

pygame.quit()
