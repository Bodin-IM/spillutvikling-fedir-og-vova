import pygame as pg
from random import randint
from enemies import *


class Level_one():
    def __init__(self):
        pg.init()
        pg.mixer.init()

        self.soundPowerUp = pg.mixer.Sound('C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/sounds/powerup.wav')
        screenWidth, screenHeight = 1920, 1080
        self.screen = pg.display.set_mode((screenWidth, screenHeight))
        pg.display.set_caption("Improved Game")

        self.bgImg = pg.image.load('levels_img/fon1.png')
        self.bgImg = pg.transform.scale(self.bgImg, (screenWidth, screenHeight))

        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Comic Sans MS", 30)

        self.running = True
        self.paused = False  
        self.new()

    def new(self):
        self.score = 0
        self.allSprites = pg.sprite.Group()
        self.foodGroup = pg.sprite.Group()
        self.enemyGroup = pg.sprite.Group()
        self.playerProjectiles = pg.sprite.Group()
        self.carGroup = pg.sprite.Group()  

        self.hero = Player(self)
        self.allSprites.add(self.hero)

        self.burgerTimer = 0
        self.enemyTimer = 0
        self.carTimer = randint(300, 600)  
        self.run()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            if not self.paused:  
                self.update()
                self.draw()
            else:
                self.draw_paused()  

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  
                    self.paused = not self.paused
            elif event.type == pg.MOUSEBUTTONDOWN:  
                if event.button == 1 and not self.paused:  
                    self.hero.shoot()

    def update(self):
        self.allSprites.update()

        
        if self.carTimer <= 0:
            car = Car(self)  
            self.allSprites.add(car)
            self.carGroup.add(car)
            self.carTimer = randint(600, 1200)  
        self.carTimer -= 1

        
        for enemy in pg.sprite.spritecollide(self.hero, self.enemyGroup, True):
            if not enemy.hit_hero:  
                self.score -= 20
                self.hero.size = max(50, self.hero.size - 20)  

                enemy.hit_hero = True

        if pg.sprite.spritecollide(self.hero, self.foodGroup, True):
            #self.soundPowerUp.play()
            self.score += 10
            self.hero.size = min(150, self.hero.size + 10)  


        
        if self.burgerTimer <= 0:
            burger = Burger()
            self.foodGroup.add(burger)
            self.allSprites.add(burger)
            self.burgerTimer = randint(50, 100)

        
        if self.enemyTimer <= 0:
            enemy = Enemy(self.hero)
            self.enemyGroup.add(enemy)
            self.allSprites.add(enemy)
            self.enemyTimer = randint(80, 120)

        self.burgerTimer -= 1
        self.enemyTimer -= 1

    def draw(self):
        self.screen.blit(self.bgImg, (0, 0))
        self.allSprites.draw(self.screen)
        scoreText = self.font.render(f"Score: {self.score}", True, "red")
        self.screen.blit(scoreText, (10, 10))
        pg.display.flip()

    def draw_paused(self):
        self.screen.blit(self.bgImg, (0, 0))  
        pauseText = self.font.render("Paused", True, "yellow")
        text_rect = pauseText.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(pauseText, text_rect)
        pg.display.flip()

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pg.image.load("C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/img/player.PNG")
        self.size = 100
        self.image = pg.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(center=(100, 100))
        self.speed = 5
        self.direction = "right"  
        self.shoot_cooldown = 500  
        self.shoot_timer = pg.time.get_ticks()  

        frame1 = pg.transform.scale((pg.image.load("C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/img/frame1.png")),(100,100))
        frame2 = pg.transform.scale((pg.image.load("C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/img/frame2.png")),(100,100))
        frame3 = pg.transform.scale((pg.image.load("C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/img/frame3.png")),(100,100))
        self.anim1frames = [frame1, frame2, frame3]


        self.lastUpdate = 0
        self.currentFrame = 0
        self.standing = True

    def shoot(self):
        current_time = pg.time.get_ticks()  
        if current_time - self.shoot_timer >= self.shoot_cooldown:  
            projectile = Projectile(self.game, self.direction)
            self.game.allSprites.add(projectile)
            self.game.playerProjectiles.add(projectile)
            self.shoot_timer = current_time  

    def animate(self):
        ticks_now = pg.time.get_ticks()
        if self.standing:
            if ticks_now - self.lastUpdate > 60:
                self.lastUpdate = ticks_now
                self.currentFrame = (self.currentFrame + 1) % len(self.anim1frames)
                self.image = self.anim1frames[self.currentFrame]
            print("animated")


    def update(self):
        keys = pg.key.get_pressed()
        self.standing = True
        if keys[pg.K_w]:
            self.rect.y -= self.speed
            self.standing = False
        if keys[pg.K_a]:
            self.rect.x -= self.speed
            self.direction = "left"
            self.image = pg.transform.flip(pg.image.load("C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/img/player.PNG"), True, False)
            self.image = pg.transform.scale(self.image, (self.size, self.size))
            self.standing = False
        if keys[pg.K_s]:
            self.rect.y += self.speed
            self.standing = False
        if keys[pg.K_d]:
            self.rect.x += self.speed
            self.direction = "right"
            self.image = pg.image.load("C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/img/player.PNG")
            self.image = pg.transform.scale(self.image, (self.size, self.size))
            self.standing = False

        if self.rect.y < 450:
            self.rect.y = 450



        self.animate()


        self.rect.clamp_ip(self.game.screen.get_rect())


        if keys[pg.K_SPACE]:
            self.shoot()





class Burger(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/img/15_burger.png")
        self.image = pg.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(randint(740, 800), randint(0, 400)))
        self.speed = randint(2, 4)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()




class Projectile(pg.sprite.Sprite):
    def __init__(self, game, direction):
        super().__init__()
        self.game = game
        self.image = pg.image.load("C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/img/Terraria-Emblem.png")
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center=(game.hero.rect.centerx, game.hero.rect.centery))
        if direction == "right":
            self.speed_x = 10 
        else:
            self.speed_x = -10
        self.speed_y = 0  

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.right < 0 or self.rect.left > self.game.screen.get_width():
            self.kill()
        if pg.sprite.spritecollide(self, self.game.enemyGroup, True):  
            self.kill()



class Car(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pg.image.load("C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/img/car1.png")
        self.image = pg.transform.scale(self.image, (100, 50))  
        self.rect = self.image.get_rect(center=(game.screen.get_width() + 50, game.screen.get_height() // 2))
        self.speed = 5  
        self.enemySpawnTimer = 0  

    def update(self):
        
        if self.rect.right > self.game.screen.get_width() // 2 + 50:
            self.rect.x -= self.speed

        
        if self.enemySpawnTimer <= 0:
            enemy = Enemy(self)  
            self.game.enemyGroup.add(enemy)
            self.game.allSprites.add(enemy)
            self.enemySpawnTimer = randint(50, 100)
        self.enemySpawnTimer -= 1






if __name__ == "__main__":
    g = Level_one()
