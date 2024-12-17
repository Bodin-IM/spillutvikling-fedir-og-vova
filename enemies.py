import pygame as pg
from random import randint


class Enemy(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pg.image.load("C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/img/enemy.png")
        self.image = pg.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

          
        if randint(0, 1) == 0:
            self.side = "left" 
        else:
            self.side = "right"


        if self.side == "left":
            self.rect.center = (0 -50, randint(200, 800))  
            self.speed_x = randint(3, 5)
        else:
            self.rect.center = (1920 + 50, randint(200, 800))  
            self.speed_x = -randint(3, 5)

        self.speed_y = 0
        self.stop_distance = randint(200, 500)  
        self.moving = True
        self.shoot_timer = pg.time.get_ticks()
        self.shoot_cooldown = 1000  

        
    def shoot(self):
        
        current_time = pg.time.get_ticks()
        if current_time - self.shoot_timer >= self.shoot_cooldown:
            projectile = EnemyProjectile(self.game, self.side)
            projectile.rect.center = self.rect.center
            self.game.allSprites.add(projectile)
            self.game.enemyGroup.add(projectile)
            self.shoot_timer = current_time

    def update(self):
        # Если враг двигается
        if self.moving:
            self.rect.x += self.speed_x
            # Проверяем, достиг ли враг своей остановки
            if (self.side == "left" and self.rect.x >= self.stop_distance) or \
               (self.side == "right" and self.rect.x <= 1920 - self.stop_distance):
                self.moving = False  # Останавливаем движение
        else:
            self.shoot()  # Враг начинает стрелять

        # Удаляем врага, если он вышел за пределы экрана
        if self.rect.right < 0 or self.rect.left > 1920:
            self.kill()


class EnemyProjectile(pg.sprite.Sprite):
    def __init__(self, game, side):
        super().__init__()
        self.game = game
        self.image = pg.image.load("C:/Users/Fedir/Desktop/goofy ahh pygame/game v2/img/Terraria-Emblem.png")
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.speed_x = 0
        self.speed_y = 5  # Снаряды летят вниз по вертикали

    def update(self):
        self.rect.y += self.speed_y
        # Удаляем снаряд, если он выходит за пределы экрана
        if self.rect.top > self.game.screen.get_height():
            self.kill()
