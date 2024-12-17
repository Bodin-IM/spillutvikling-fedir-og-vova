import pygame as pg
from random import randint
 
burgerImg = pg.image.load("C:/Users/Bruker/Desktop/game v2/img/15_burger.png")
playerImg = pg.image.load("C:/Users/Bruker/Desktop/game v2/img/player.PNG")
enemyImg = pg.image.load("C:/Users/Bruker/Desktop/game v2/img/enemy.png")
projectileImg = pg.image.load("C:/Users/Bruker/Desktop/game v2/img/Terraria-Emblem.png")
 
class Player(pg.sprite.Sprite):
    def __init__(self, game): # kjører når vi lager/oppretter 1 kopi av burger klassen
        pg.sprite.Sprite.__init__(self)
        self.image = playerImg
        self.rect = self.image.get_rect()
 
        self.game = game
 
        self.rect.x = 100
        self.rect.y = 100
 
        self.speed = 3
 
        self.gravity = 10
        self.jump_time = 0
        self.jumping = False
        self.onGround = False
 
        self.size = 100
        self.image = pg.transform.scale(playerImg,(self.size, self.size))
 
    def changeSize(self):
        self.oldRect = self.rect
        self.image = pg.transform.scale(playerImg,(self.size, self.size))
        self.rect = self.image.get_rect()
 
        self.rect.x = self.oldRect.x
        self.rect.y = self.oldRect.y
 
    def shoot(self):
        proj = Projectile(self.game)
        self.game.allSprites.add(proj)
        self.game.playerProjectiles.add(proj)
 
    def update(self):
        keys = pg.key.get_pressed() # henter hvilke knapper som er trykket
        self.rect.y += self.gravity
 
        if keys[pg.K_UP]:
            self.shoot()
 
        if keys[pg.K_SPACE] and self.onGround: 
            self.jumping = True
            self.onGround = False
 
        if keys[pg.K_w]:
            self.rect.y -=  self.speed
        if keys[pg.K_d]:
            self.rect.x +=  self.speed
        #Legg inn for keys a og s
        if keys[pg.K_a]:
            self.rect.x -= self.speed
        if keys[pg.K_s]:
            self.rect.y += self.speed
 
        #Gjør at boksen ikke forlater vinduet
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.x > 720-50:     #Width på vindu - størrelse på boks
            self.rect.x = 720-50
        if self.rect.y > 420-50:     #Height på vindu - størrelse på boks
            self.rect.y = 420-50
            self.onGround = True        
 
        if self.jumping:
            self.rect.y -= 20
            self.jump_time += 1
            if self.jump_time == 25:
                self.jumping = False
                self.jump_time = 0
 
class Burger(pg.sprite.Sprite):
    def __init__(self): # kjører når vi lager/oppretter 1 kopi av burger klassen
        pg.sprite.Sprite.__init__(self)
 
        self.image = burgerImg
        self.rect = self.image.get_rect()
 
        self.rect.x = 800
        self.rect.y = randint(0, 400)
 
        self.speed = 1
    
    def update(self):
        self.rect.x -= self.speed
 
        if self.rect.x < -30:
            self.kill()
 
class Enemy(pg.sprite.Sprite):
    def __init__(self, hero): # kjører når vi lager/oppretter 1 kopi av burger klassen
        pg.sprite.Sprite.__init__(self)
 
        self.image = enemyImg
        self.rect = self.image.get_rect()
 
        self.rect.x = randint(0,700) # spawn position x
        self.rect.y = -50 # spawn position y
 
        self.target = hero
 
        self.speedY = 3
        self.speedX = 1
 
        
    
    def update(self):
        self.rect.y += self.speedY # hvilken vei flytter den seg
 
        if self.rect.x > self.target.rect.x: # hvis til høyre for player
            self.rect.x -= self.speedX
        else:
            self.rect.x += self.speedX # beveg til høyre
 
        if self.rect.y > 500:
            self.kill()
 
class Projectile(pg.sprite.Sprite):
    def __init__(self, game): # kjører når vi lager/oppretter 1 kopi av burger klassen
        pg.sprite.Sprite.__init__(self)
        self.image = projectileImg
        self.rect = self.image.get_rect()
 
        self.game = game
        #self.player = self.game.hero
 
        self.rect.x = self.game.hero.rect.x # spawn position x
        self.rect.y = self.game.hero.rect.y # spawn position y
 
        self.speedY = -4
        self.speedX = 0
 
    def update(self):
        self.rect.y += self.speedY
 
        hit = pg.sprite.spritecollide(self, self.game.enemyGroup, True)