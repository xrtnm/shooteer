from pygame import *
from random import randint
from time import time as get_time


SCREEN_SIZE = (1420, 780)
SPRITE_SIZE = 40

def show_label(text: str, x: int, y: int, font_name: str='Arial', color: tuple=(255, 255, 255)):
    '''
    Выводит надпись на игровую сцену window

    Аргументы:
    x, y - координаты, где будет выведена надпись
    text - текст надписи
    font_name - название шрифта
    color - цвет текста
    '''
    font.init()
    font1 = font.SysFont(font_name, 40)
    text = font1.render(text, True, color)
    window.blit(text, (x, y))

class Live:
    def __init__(self, x,y, image_name, lives):
        self.lives = lives
        self.image = transform.scale(image.load(image_name), (SPRITE_SIZE//2, SPRITE_SIZE//2))
        self.x = x
        self.y = y

    def update(self):
        for i in range(self.lives):
            window.blit(self.image, (self.x-i*40, self.y))

lives = Live(SCREEN_SIZE[0] - SPRITE_SIZE//2, 20, 'rocket.png', 5)

class GameSprite(sprite.Sprite):
    def __init__(self, image_name, speed, x, y):
        super().__init__()
        self.image_name = image_name
        self.image = image.load(image_name)
        self.image = transform.scale(self.image, (SPRITE_SIZE, SPRITE_SIZE))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < SCREEN_SIZE[0]-SPRITE_SIZE:
            self.rect.x += self.speed
        if keys_pressed[K_SPACE] and get_time() - self.last_shoot > .2:
            self.shoot()
            self.last_shoot = get_time()
    
    def shoot(self):
        new_bullet = Bullet('bullet.png', 7, self.rect.centerx-3, self.rect.y)
        new_bullet.image = transform.scale(new_bullet.image, (10, 30))
        bullets.add(new_bullet)
        if killed_counter.counter >= 10:
            new_bullet = Bullet('bullet.png', 7, self.rect.centerx-3, self.rect.y, 1)
            new_bullet.image = transform.scale(new_bullet.image, (10, 30))
            bullets.add(new_bullet)
            new_bullet = Bullet('bullet.png', 7, self.rect.centerx-3, self.rect.y, 2)
            new_bullet.image = transform.scale(new_bullet.image, (10, 30))
            bullets.add(new_bullet)
    

class Enemy(GameSprite):
    def __init__(self, image_name, speed, x, y):
        super().__init__(image_name, speed, x, y)
        self.set_hp()

    def set_hp(self):
        self.hp = randint(1, 5)
        if self.hp in (3, 4, 5):
            self.speed = 1
            x, y = self.rect.x, self.rect.y
            self.image = image.load(self.image_name)
            self.image = transform.scale(self.image, (SPRITE_SIZE, SPRITE_SIZE))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.speed = 3
            x, y = self.rect.x, self.rect.y
            self.image = image.load(self.image_name)
            self.image = transform.scale(self.image, (SPRITE_SIZE//2, SPRITE_SIZE//2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
            missed_counter.counter += 1
            missed_counter.set_text(24,(255,255,255))
        self.reset()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
        self.reset()

class Heart(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < SCREEN_SIZE[1]:
            self.reset()
        else:
            if randint(1, 100) == 1:
                self.rect.y = 0
                self.rect.x = randint(1, SCREEN_SIZE[0] - SPRITE_SIZE)
                
heart = Heart('rocket.png', 2, randint(1,SCREEN_SIZE[0] - SPRITE_SIZE), SCREEN_SIZE[1]*2)

class Bullet(GameSprite):
    def __init__(self, image_name, speed, x, y, direction=0):
        super().__init__(image_name, speed, x, y)
        self.direction = direction
    
    def update(self):
        self.rect.y -= self.speed
        if self.direction == 1:
            self.rect.x -= self.speed
        if self.direction == 2:
            self.rect.x += self.speed
        self.reset()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(2):
    asteroids.add(Asteroid('asteroid.png', randint(1,2), randint(0, 635), 0))


font.init()

class Counter:
    def __init__(self,text,x,y):
        self.counter = 0
        self.text = text 
        self.pos = (x,y)
    
    def set_text(self,font_size,text_color):
        f = font.SysFont('Arial',font_size)
        self.image = f.render(self.text + str(self.counter),True,text_color)

    def draw(self):
        window.blit(self.image, self.pos)





player = Player('rocket.png', 7, SCREEN_SIZE[0]//2, SCREEN_SIZE[1] - SPRITE_SIZE - 5)
player.last_shoot = 0

ufos = sprite.Group()
for i in range(5):
    ufos.add(Enemy('ufo.png', 1, randint(0, SCREEN_SIZE[0]-SPRITE_SIZE), 0))

window = display.set_mode(SCREEN_SIZE)
display.set_caption('Shooter')

missed_counter = Counter('Счетчик пропущенных:',10,10)
missed_counter.set_text(24,(255,255,255))

killed_counter = Counter('Счетчик уничтоженных:',10,50)
killed_counter.set_text(24,(255,255,255))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()


pic = image.load('galaxy.jpg')
pic = transform.scale(pic, SCREEN_SIZE)

clock = time.Clock()
FPS = 60
game = True
finish = False

end = get_time()+4
while True:
    clock.tick(FPS)
    window.blit(pic, (0,0))
    show_label(str(int(end - get_time())), SCREEN_SIZE[0]//2 - 20, SCREEN_SIZE[1]//2 - 20)
    
    display.update()
    if get_time() > end:
        break
    
while game:
    clock.tick(FPS)
    if finish == False:
        window.blit(pic, (0,0))
        ufos.update()
        player.reset()
        player.update()
        missed_counter.draw()
        killed_counter.draw()    
        bullets.update()
        asteroids.update()
        bullets.draw(window)
        heart.update()
        if sprite.collide_rect(player, heart):
            lives.lives += 1
            heart.rect.y = SCREEN_SIZE[1]*2
        lives.update()
        if killed_counter.counter >= 50:
            show_label('Победа', SCREEN_SIZE[0]//2-40, SCREEN_SIZE[1]//2-20)
            finish = True
        if missed_counter.counter >= 3:
            lives.lives -= 1
            missed_counter.counter = 0
            
        if sprite.spritecollide(player, ufos, False) or sprite.spritecollide(player, asteroids, False):
            for s in sprite.spritecollide(player, ufos, False) + sprite.spritecollide(player,asteroids, False):
                s.rect.y = 0
                s.rect.x = randint(1, SCREEN_SIZE[0]-SPRITE_SIZE)
                lives.lives -= 1
            
        if lives.lives <= 0:    
            show_label('Поражение...', SCREEN_SIZE[0]//2-40, SCREEN_SIZE[1]//2-20)
            finish = True
        display.update()    
        
        list_monsters = sprite.groupcollide(ufos, bullets, False, True)
        for monster in list_monsters:
            monster.hp -= 1
            if monster.hp <= 0:
                monster.set_hp()
                monster.hp = randint(1, 7)
                monster.rect.y = 0
                monster.rect.x = randint(1, SCREEN_SIZE[1]-SPRITE_SIZE)
                killed_counter.counter += 1
                killed_counter.set_text(24,(255,255,255))
                if killed_counter.counter == 20:
                    ufos.add(Enemy('ufo.png', 1, randint(0, SCREEN_SIZE[0]-SPRITE_SIZE), 0))

            
    for e in event.get():
        if e.type == QUIT:
            game = False
