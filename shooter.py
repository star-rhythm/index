from pygame import *
from random import *

font.init()

window = display.set_mode((850, 500))
display.set_caption('Shooter')
back = transform.scale(image.load('background.png'), (850, 500))


class Card(sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__()
        self.rect = Rect(x, y, w, h)
        self.fill = color

    def draw(self):
        draw.rect(window, self.fill, self.rect)

class Pic(sprite.Sprite):
    def __init__(self, pic, x, y, w, h):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pic), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self): #Отрисовка изображений на экране
        window.blit(self.image, (self.rect.x, self.rect.y))

class Ship(Pic):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 760 and not finish:
            self.rect.x += 15
        elif keys[K_a] and self.rect.x > 0 and not finish:
            self.rect.x -= 15
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx-6, self.rect.centery,  12,50)
        bullets.add(bullet)

bullets = sprite.Group()

class Bullet(Pic): #пули
    def update(self):
        self.rect.y -= 17
        if self.rect.y <= 0:
            self.kill()

class Enemy(Pic):
    def update(self):
        self.rect.y += randint(2, 8)
        global miss
        if self.rect.y >= 460:
            self.rect.y = 0
            self.rect.x = randint(0, 750)
            miss += 1


        
carda = Card(0, 0, 270, 110, (20,20,20))
ship = Ship('ship.png', 325, 400, 90, 100)

enemies = sprite.Group()
for i in range(6):
    ship_enemy = Enemy('ship_enemy2.png', randint(0, 750), -7, 60,70)
    enemies.add(ship_enemy)
miss = 0
kill = 0


run = True
finish = False
while run:
    display.update()
    time.delay(40)
    if not finish:
        window.blit(back, (0,0))
        bullets.draw(window)
        bullets.update()
        ship.reset()
        enemies.draw(window)
        enemies.update()
        ship.update()
        carda.draw()
        carda.update()

        miss_text = font.SysFont('Verdana', 30).render("Пропущено: " + str(miss),1,(255,255,255))
        window.blit(miss_text, (20, 10))

        kill_text = font.SysFont('Verdana', 30).render("Убито: " + str(kill),1,(255,255,255))
        window.blit(kill_text, (20, 50))

        if sprite.groupcollide(bullets, enemies, True, True):
            ship_enemy = Enemy('ship_enemy2.png', randint(0, 750), -7, 60,70)
            enemies.add(ship_enemy)
            enemies.draw(window)
            enemies.update()
            kill += 1

        if sprite.spritecollide(ship, enemies, True) or miss == 8:
            lose_text = font.SysFont('Verdana', 48).render('Вы проиграли!', 1, (255,255,255))
            carda = Card(250, 190, 410, 90, (20,20,20))
            carda.draw()
            carda.update()

            window.blit(lose_text, (270, 200))
            finish = True
        
        if kill == 6:
            win_text = font.SysFont('Verdana', 48).render("Вы победили!",1,(255,255,255))
            carda = Card(250, 190, 410, 90, (20,20,20))
            carda.draw()
            carda.update()
            window.blit(win_text, (270, 200))
            finish = True

        
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE: #стрельба
                ship.fire()
    


