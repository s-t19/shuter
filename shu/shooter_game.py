#Создай собственный Шутер!

from pygame import *
from random import randint 



class GameSprite(sprite.Sprite):
    def __init__(self, speed_sprite, x_sprite, y_sprite, image_sprite, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(image_sprite), (size_x, size_y))
        self.speed = speed_sprite
        self.rect = self.image.get_rect()
        self.rect.x = x_sprite
        self.rect.y = y_sprite

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_w - 70:
            self.rect.x += self.speed
        

    def fire(self):
        bullet = Bullet(15, self.rect.x - 8, self.rect.top, 'bullet.png', 16, 20)
        bullets.add(bullet)

lost = 0
score = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
         
        if self.rect.y >= win_h:
            global lost
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(5, win_w - 70)
            self.speed = randint(2, 5)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
         
        if self.rect.y >= win_h:
            self.rect.y = 0
            self.rect.x = randint(5, win_w - 70)
            self.speed = randint(2, 5)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()



win_w = 700
win_h = 500
window = display.set_mode((win_w, win_h))

display.set_caption('Шутер')

background = transform.scale(
    image.load('galaxy.jpg'), 
    (win_w, win_h)
)
player = Player(5, win_w/ - 65/2, win_h - 65, 'rocket.png', 65, 65)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(randint(2, 4), randint(5, win_w - 70), 0,'ufo.png', 65, 40)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid(randint(2, 3),  randint(5, win_w - 70) , 0, 'asteroid.png', 65, 40)
    asteroids.add(asteroid)
bullets = sprite.Group()


font.init()
font1 = font.SysFont('Arial', 36)
font_title = font.SysFont('Arial', 72)
win_text = font_title.render('YOU WIN!', True, (27, 242, 242))
lose_text = font_title.render('YOU LOSE!', True, (245, 207, 39))


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

shoot_sound = mixer.Sound('fire.ogg')

run = True
clock = time.Clock()
FPS = 60
finish = False
result_text = lose_text
start_time = time.get_ticks()
num_fire = 0
is_reolad = False
reload_timer = time.get_ticks()


life_player = 3
while run:
    

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not is_reolad:
                player.fire()
                shoot_sound.play()
                num_fire += 1
                if num_fire >= 7:
                    is_reolad = True
                    reload_timer = time.get_ticks()
    if finish == False:

        

        window.blit(background, (0, 0))

        enemies_collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in enemies_collides:
            score += 1
            monster = Enemy(randint(2, 4), randint(5, win_w - 70), 0,'ufo.png', 65, 40)
            monsters.add(monster)

        asteroids_collides = sprite.spritecollide(player, asteroids, False)
        for i in asteroids_collides:
            life_player -= 1
            i.kill()

        text_lose = font1.render('пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (5, 35))

        text_score = font1.render('счёт:' + str(score), 1, (255, 255, 255))
        window.blit(text_score, (5, 5))

        


        enemy_collides = sprite.spritecollide(player, monsters, False)

        for i in enemy_collides:
            life_player -= 1
            i.kill()
        text_life = font1.render('жизни:' + str(life_player), 1, (255, 255, 255))
        window.blit(text_life, (5, 65))
        if lost >= 3 or life_player <= 0:
            finish = True
            result_text = lose_text
            start_time = time.get_ticks()

        if score >= 10:
            finish = True
            result_text = win_text
            start_time = time.get_ticks()
        


        monsters.update()
        monsters.draw(window)
        player.update()
        player.reset()
        asteroids.update()
        asteroids.draw(window)

        bullets.update()
        bullets.draw(window)

        #window.blit(win_text, (170, 210))
        #window.blit(lose_text, (180, 210))

        if is_reolad:
            text_reolad = font1.render('Перезарядка...', True, (255, 20, 20))
            window.blit(text_reolad, (60, win_h - 70))
            current_timer = time.get_ticks()
            if current_timer - reload_timer >= 2000:
                is_reolad = False
                num_fire = 0


    else:
        if result_text == win_text:
            window.blit(result_text, (230, 230))
        
        else:
            window.blit(result_text, (220, 230))
    
        end_time = time.get_ticks()
        if end_time - start_time > 3000:
            
            
            finish = False
            score = 0
            lost = 0
            is_reolad = False
            num_fire = 0
            current_timer = 0
            life_player = 3

            for bullet in bullets:
                bullet.kill()
            for enemy in monsters:
                enemy.kill()
            for asteroid in asteroids:
                asteroid.kill()
            for i in range(5):
                monster = Enemy(randint(2, 4), randint(5, win_w - 70), 0,'ufo.png', 65, 40)
                monsters.add(monster)
            for i in range(3):
                asteroid = Asteroid(randint(2, 3), randint(5, win_w - 70), 0, 'asteroid.png', 65, 40)
                asteroids.add(asteroid)
    

        
    
    clock.tick(FPS)
    display.update()