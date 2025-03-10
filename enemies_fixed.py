import pygame
import random
import time
import math
import sys

# Класс пули игрока
class HeroBullet:
    def __init__(self, x, y, speed, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.active = True
        self.damage = damage

    def move(self):
        self.x += self.speed
        if self.x < 0 or self.x > 800:  # Ширина экрана фиксирована для примера
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, 10, 5))

# Класс пули врага
class EnemyBullet:
    def __init__(self, x, y, speed, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.active = True
        self.damage = damage

    def move(self):
        self.x += self.speed
        if self.x < 0 or self.x > 800:
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 10, 5))

# Класс особой пули для enemy6
class HomingSausage:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 3
        self.active = True

    def move(self, hero_x, hero_y):
        dx = hero_x - self.x
        dy = hero_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance

    def check_collision(self, hero_x, hero_y, hero_size):
        if self.x < hero_x + hero_size and self.x + 20 > hero_x and self.y < hero_y + hero_size and self.y + 20 > hero_y:
            self.active = False
            return True
        return False

    def draw(self, screen):
        screen.blit(sausage_image, (self.x, self.y))

# Класс особой пули для enemy7
class StraightBullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 5
        self.dx = target_x - x
        self.dy = target_y - y
        distance = (self.dx ** 2 + self.dy ** 2) ** 0.5
        if distance != 0:
            self.dx = self.dx / distance * self.speed
            self.dy = self.dy / distance * self.speed
        self.active = True

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, 10, 10))

# Класс особой пули для enemy8
class SpreadBullet:
    def __init__(self, x, y, angle, facing_left):
        self.x = x
        self.y = y
        self.speed = 5
        self.angle = angle if not facing_left else 180 - angle
        self.dx = math.cos(math.radians(self.angle)) * self.speed
        self.dy = math.sin(math.radians(self.angle)) * self.speed
        self.active = True

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, 10, 10))

# Класс врага Enemy1
class Enemy1:
    def __init__(self, x, y, size, speed, health):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.health = health
        self.state = "moving"  # Состояния: "moving", "shooting" или "dying"
        self.last_state_change = time.time()
        self.state_change_interval = random.uniform(1, 3)  # Интервал 1-3 секунды
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.facing_left = True
        self.death_animation_index = 0
        self.is_dead = False
        self.shoot_animation_time = time.time()
        self.walk_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en1_W1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en1_W2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en1_W3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en1_W4.png")
        ]
        self.death_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en1_D1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en1_D2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en1_D3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en1_D4.png")
        ]

    def move_towards_hero(self, hero_x, hero_y):
        if self.state == "moving":
            if self.x < hero_x:
                self.x += self.speed * 0.8
                self.facing_left = False
            elif self.x > hero_x:
                self.x -= self.speed * 0.8
                self.facing_left = True

            if self.y < hero_y:
                self.y += self.speed * 0.4
            elif self.y > hero_y:
                self.y -= self.speed * 0.4

            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:
                self.animation_index = (self.animation_index + 1) % len(self.walk_frames)
                self.last_animation_time = current_time

    def shoot(self, bullets):
        if self.state == "shooting":
            current_time = time.time()
            if current_time - self.shoot_animation_time > 0.15:
                self.shoot_animation_time = current_time
                bullet_x = self.x if self.facing_left else self.x + self.size
                bullet_y = self.y + self.size // 2
                bullet_speed = -10 if self.facing_left else 10
                bullets.append(EnemyBullet(bullet_x, bullet_y, bullet_speed, damage=10))

    def update_state(self):
        if self.is_dead:
            return

        current_time = time.time()
        if current_time - self.last_state_change > self.state_change_interval:
            self.state = "shooting" if self.state == "moving" else "moving"
            self.last_state_change = current_time
            self.state_change_interval = random.uniform(2, 5)

    def check_collision(self, bullets):
        if self.is_dead:
            return False

        for bullet in bullets:
            if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
                self.health -= bullet.damage
                bullets.remove(bullet)
                if self.health <= 0:
                    self.state = "dying"
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        if self.state == "dying":
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        current_frame = self.walk_frames[self.animation_index] if self.state == "moving" else self.walk_frames[0]

        if self.facing_left:
            screen.blit(current_frame, (self.x, self.y))
        else:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

# Класс врага Enemy2
class Enemy2:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.state = "moving"  # Состояния: "moving" или "dying"
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.facing_left = True
        self.death_animation_index = 0
        self.is_dead = False
        self.health = 3  # Умирает с 3 попаданий

        # Загрузка фреймов
        self.walk_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en2_W1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en2_W2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en2_W3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en2_W4.png")
        ]

        self.death_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en2_D1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en2_D2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en2_D3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en2_D4.png")
        ]

    def move_towards_hero(self, hero_x, hero_y):
        if self.state == "moving":
            if self.x < hero_x:
                self.x += self.speed
                self.facing_left = False
            elif self.x > hero_x:
                self.x -= self.speed
                self.facing_left = True

            if self.y < hero_y:
                self.y += self.speed
            elif self.y > hero_y:
                self.y -= self.speed

            # Анимация движения
            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:
                self.animation_index = (self.animation_index + 1) % len(self.walk_frames)
                self.last_animation_time = current_time

    def check_collision_with_hero(self, hero_x, hero_y, hero_size):
        if self.is_dead:
            return False

        if (
            self.x < hero_x + hero_size
            and self.x + self.size > hero_x
            and self.y < hero_y + hero_size
            and self.y + self.size > hero_y
        ):
            # Здесь можно вставить снижение здоровья героя
            return True
        return False

    def check_collision(self, bullets):
        if self.is_dead:
            return False

        for bullet in bullets:
            if (
                self.x < bullet.x < self.x + self.size
                and self.y < bullet.y < self.y + self.size
            ):
                bullets.remove(bullet)
                self.health -= 1
                if self.health <= 0:
                    self.state = "dying"
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        if self.state == "dying":
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        current_frame = self.walk_frames[self.animation_index]

        if self.facing_left:
            screen.blit(current_frame, (self.x, self.y))
        else:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

# Класс врага Enemy3
class Enemy3:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.state = "moving"  # Состояния: "moving", "idle", "shooting" или "dying"
        self.last_state_change = time.time()
        self.state_change_interval = random.uniform(1, 3)  # Интервал 1-3 секунды
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.facing_left = True
        self.death_animation_index = 0
        self.is_dead = False
        self.shoot_animation_index = 0
        self.shoot_animation_time = time.time()
        self.health = 6  # Умирает с 6 попаданий

        # Загрузка фреймов
        self.walk_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_W1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_W2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_W3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_W4.png")
        ]

        self.death_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_D1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_D2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_D3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_D4.png")
        ]

        self.shoot_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_S1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_S2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_S3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en3_S4.png")
        ]

    def move_towards_hero(self, hero_x, hero_y):
        if self.state == "moving":
            if self.x < hero_x:
                self.x += self.speed * 0.8
                self.facing_left = False
            elif self.x > hero_x:
                self.x -= self.speed * 0.8
                self.facing_left = True

            if self.y < hero_y:
                self.y += self.speed * 0.8
            elif self.y > hero_y:
                self.y -= self.speed * 0.8

            # Анимация движения
            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:
                self.animation_index = (self.animation_index + 1) % len(self.walk_frames)
                self.last_animation_time = current_time

    def shoot(self, hero_x, hero_y):
        if self.state == "shooting":
            current_time = time.time()
            if current_time - self.shoot_animation_time > 0.2:
                self.shoot_animation_index += 1
                self.shoot_animation_time = current_time

                # На 3-м кадре запускаем атаку
                if self.shoot_animation_index == 2:
                    # Здесь можно добавить урон герою
                    pass

                if self.shoot_animation_index >= len(self.shoot_frames):
                    self.state = "moving"
                    self.shoot_animation_index = 0

    def update_state(self):
        if self.is_dead:
            return

        current_time = time.time()
        if current_time - self.last_state_change > self.state_change_interval:
            self.state = "shooting" if self.shoot_frames else "moving"
            self.last_state_change = current_time
            self.state_change_interval = random.uniform(1, 3)

    def check_collision(self, bullets):
        if self.is_dead:
            return False

        for bullet in bullets:
            if (
                self.x < bullet.x < self.x + self.size
                and self.y < bullet.y < self.y + self.size
            ):
                bullets.remove(bullet)
                self.health -= 1
                if self.health <= 0:
                    self.state = "dying"
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        if self.state == "dying":
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        if self.state == "shooting" and self.shoot_frames:
            current_frame = self.shoot_frames[self.shoot_animation_index]
        else:
            current_frame = self.walk_frames[self.animation_index]

        if self.facing_left:
            screen.blit(current_frame, (self.x, self.y))
        else:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

# Класс врага Enemy4
class Enemy4:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.state = "moving"
        self.last_state_change = time.time()
        self.state_change_interval = random.uniform(1, 3)
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.facing_left = True
        self.death_animation_index = 0
        self.is_dead = False
        self.shoot_animation_time = time.time()
        self.burst_count = 0
        self.health = 2  # Умирает с двух попаданий

        # Загрузка фреймов
        self.walk_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en4_W1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en4_W2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en4_W3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en4_W4.png")
        ]

        self.death_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en4_D1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en4_D2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en4_D3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en4_D4.png")
        ]

    def move_towards_hero(self, hero_x, hero_y):
        if self.state == "moving":
            if self.x < hero_x:
                self.x += self.speed * 0.7
                self.facing_left = False
            elif self.x > hero_x:
                self.x -= self.speed * 0.7
                self.facing_left = True

            if self.y < hero_y:
                self.y += self.speed * 0.5
            elif self.y > hero_y:
                self.y -= self.speed * 0.5

            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:
                self.animation_index = (self.animation_index + 1) % len(self.walk_frames)
                self.last_animation_time = current_time

    def shoot(self):
        if self.state == "shooting":
            current_time = time.time()
            if current_time - self.shoot_animation_time > 0.2:
                self.shoot_animation_time = current_time
                self.burst_count += 1
                if self.burst_count >= 3:
                    self.burst_count = 0
                    self.state = "moving"

    def update_state(self):
        if self.is_dead:
            return

        current_time = time.time()
        if current_time - self.last_state_change > self.state_change_interval:
            self.state = "shooting" if self.state == "moving" else "moving"
            self.last_state_change = current_time
            self.state_change_interval = random.uniform(1, 3)

    def check_collision(self, bullets):
        if self.is_dead:
            return False

        for bullet in bullets:
            if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
                bullets.remove(bullet)
                self.health -= 1
                if self.health <= 0:
                    self.state = "dying"
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        if self.state == "dying":
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        current_frame = self.walk_frames[self.animation_index] if self.state == "moving" else self.walk_frames[0]

        if self.facing_left:
            screen.blit(current_frame, (self.x, self.y))
        else:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

# Класс врага Enemy5
class Enemy5:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.state = "moving"
        self.last_state_change = time.time()
        self.state_change_interval = random.uniform(1, 3)
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.facing_left = True
        self.death_animation_index = 0
        self.is_dead = False
        self.shoot_animation_time = time.time()
        self.health = 7  # Умирает с 7 попаданий

        # Загрузка фреймов
        self.walk_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en5_W1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en5_W2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en5_W3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en5_W4.png")
        ]

        self.death_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en5_D1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en5_D2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en5_D3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en5_D4.png")
        ]

    def move_towards_hero(self, hero_x, hero_y):
        if self.state == "moving":
            if self.x < hero_x:
                self.x += self.speed * 0.4
                self.facing_left = False
            elif self.x > hero_x:
                self.x -= self.speed * 0.4
                self.facing_left = True

            if self.y < hero_y:
                self.y += self.speed * 0.2
            elif self.y > hero_y:
                self.y -= self.speed * 0.2

            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:
                self.animation_index = (self.animation_index + 1) % len(self.walk_frames)
                self.last_animation_time = current_time

    def shoot(self):
        if self.state == "shooting":
            current_time = time.time()
            if current_time - self.shoot_animation_time > 0.1:
                self.shoot_animation_time = current_time

    def update_state(self):
        if self.is_dead:
            return

        current_time = time.time()
        if current_time - self.last_state_change > self.state_change_interval:
            self.state = "shooting" if self.state == "moving" else "moving"
            self.last_state_change = current_time
            self.state_change_interval = random.uniform(1, 3)

    def check_collision(self, bullets):
        if self.is_dead:
            return False

        for bullet in bullets:
            if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
                bullets.remove(bullet)
                self.health -= 1
                if self.health <= 0:
                    self.state = "dying"
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        if self.state == "dying":
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        current_frame = self.walk_frames[self.animation_index] if self.state == "moving" else self.walk_frames[0]

        if self.facing_left:
            screen.blit(current_frame, (self.x, self.y))
        else:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

# Класс врага Enemy6
class Enemy6:
    def __init__(self, x, y, size=50, speed=2):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.state = "moving"
        self.last_state_change = time.time()
        self.state_change_interval = random.uniform(1, 3)
        self.bullets = []
        self.last_shot_time = time.time()
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.facing_left = True
        self.death_animation_index = 0
        self.is_dead = False
        self.shoot_animation_index = 0
        self.shoot_animation_time = time.time()
        self.health = 2

        # Прямая загрузка фреймов
        self.walk_frame_1 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_W1.png")
        self.walk_frame_2 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_W2.png")
        self.walk_frame_3 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_W3.png")
        self.walk_frame_4 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_W4.png")

        self.death_frame_1 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_D1.png")
        self.death_frame_2 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_D2.png")
        self.death_frame_3 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_D3.png")
        self.death_frame_4 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_D4.png")

        self.shoot_frame_1 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_S1.png")
        self.shoot_frame_2 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_S2.png")
        self.shoot_frame_3 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_S3.png")
        self.shoot_frame_4 = pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en6_S4.png")

        self.walk_frames = [self.walk_frame_1, self.walk_frame_2, self.walk_frame_3, self.walk_frame_4]
        self.death_frames = [self.death_frame_1, self.death_frame_2, self.death_frame_3, self.death_frame_4]
        self.shoot_frames = [self.shoot_frame_1, self.shoot_frame_2, self.shoot_frame_3, self.shoot_frame_4]
        self.homing_missiles = []

    def move_towards_hero(self, hero_x, hero_y):
        if self.state == "moving":
            if self.x < hero_x:
                self.x += self.speed * 0.8
                self.facing_left = False
            elif self.x > hero_x:
                self.x -= self.speed * 0.8
                self.facing_left = True

            if self.y < hero_y:
                self.y += self.speed * 0.8
            elif self.y > hero_y:
                self.y -= self.speed * 0.8

            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:
                self.animation_index = (self.animation_index + 1) % len(self.walk_frames)
                self.last_animation_time = current_time

    def shoot(self, hero_x, hero_y):
        if self.state == "shooting":
            current_time = time.time()
            if current_time - self.shoot_animation_time > 0.2:
                self.shoot_animation_index += 1
                self.shoot_animation_time = current_time

                if self.shoot_animation_index == 2:
                    self.homing_missiles.append(HomingSausage(self.x, self.y, hero_x, hero_y))

                if self.shoot_animation_index >= len(self.shoot_frames):
                    self.state = "moving"
                    self.shoot_animation_index = 0

    def update_state(self):
        if self.is_dead:
            return

        current_time = time.time()
        if current_time - self.last_state_change > self.state_change_interval:
            self.state = "shooting" if self.shoot_frames else "moving"
            self.last_state_change = current_time
            self.state_change_interval = random.uniform(1, 3)

    def update_bullets(self):
        for missile in self.homing_missiles:
            missile.move(self.x, self.y)
        self.homing_missiles = [missile for missile in self.homing_missiles if missile.active]

    def check_collision(self, bullets):
        if self.is_dead:
            return False

        for bullet in bullets:
            if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
                bullets.remove(bullet)
                self.health -= 1
                if self.health <= 0:
                    self.state = "dying"
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        if self.state == "dying":
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        if self.state == "shooting" and self.shoot_frames:
            current_frame = self.shoot_frames[self.shoot_animation_index]
        else:
            current_frame = self.walk_frames[self.animation_index]

        if self.facing_left:
            screen.blit(current_frame, (self.x, self.y))
        else:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

        for missile in self.homing_missiles:
            missile.draw(screen)

# Класс врага Enemy7
class Enemy7:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.state = "moving"
        self.last_state_change = time.time()
        self.state_change_interval = 2  # Интервал смены состояния
        self.bullets = []
        self.last_shot_time = time.time()
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.facing_left = True
        self.death_animation_index = 0
        self.is_dead = False
        self.shoot_animation_index = 0
        self.shoot_animation_time = time.time()
        self.hit_count = 0

        # Загрузка фреймов
        self.walk_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_W1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_W2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_W3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_W4.png")
        ]
        self.death_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_D1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_D2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_D3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_D4.png")
        ]
        self.shoot_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_S1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_S2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_S3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en7_S4.png")
        ]

    def move_towards_hero(self, hero_x, hero_y):
        if self.state == "moving":
            if self.x < hero_x:
                self.x += self.speed
                self.facing_left = False
            elif self.x > hero_x:
                self.x -= self.speed
                self.facing_left = True

            if self.y < hero_y:
                self.y += self.speed
            elif self.y > hero_y:
                self.y -= self.speed

            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:
                self.animation_index = (self.animation_index + 1) % len(self.walk_frames)
                self.last_animation_time = current_time

    def shoot(self, hero_x, hero_y):
        if self.state == "shooting":
            current_time = time.time()
            if current_time - self.shoot_animation_time > 0.2:
                self.shoot_animation_index += 1
                self.shoot_animation_time = current_time
                if self.shoot_animation_index == 2:
                    self.bullets.append(StraightBullet(self.x, self.y, hero_x, hero_y))
                if self.shoot_animation_index >= len(self.shoot_frames):
                    self.state = "moving"
                    self.shoot_animation_index = 0

    def update_state(self):
        if self.is_dead:
            return
        current_time = time.time()
        if current_time - self.last_state_change > self.state_change_interval:
            self.state = "shooting" if self.state == "moving" else "moving"
            self.last_state_change = current_time

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.move()
        self.bullets = [bullet for bullet in self.bullets if bullet.active]

    def check_collision(self, bullets):
        if self.is_dead:
            return False
        for bullet in bullets:
            if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
                bullets.remove(bullet)
                self.hit_count += 1
                if self.hit_count >= 1:
                    self.state = "dying"
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        if self.state == "dying":
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        current_frame = self.walk_frames[self.animation_index] if self.state == "moving" else self.shoot_frames[self.shoot_animation_index]

        if self.facing_left:
            screen.blit(current_frame, (self.x, self.y))
        else:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

        for bullet in self.bullets:
            bullet.draw(screen)

# Класс врага Enemy8
class Enemy8:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.health = 4
        self.state = "moving"
        self.last_state_change = time.time()
        self.state_change_interval = random.uniform(1, 3)
        self.bullets = []
        self.last_shot_time = time.time()
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.facing_left = True
        self.death_animation_index = 0
        self.is_dead = False
        self.shoot_animation_index = 0
        self.shoot_animation_time = time.time()

        # Прямая загрузка фреймов
        self.walk_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_W1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_W2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_W3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_W4.png")
        ]
        self.death_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_D1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_D2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_D3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_D4.png")
        ]
        self.shoot_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_S1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_S2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_S3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en8_S4.png")
        ]

    def move_towards_hero(self, hero_x, hero_y):
        if self.state == "moving":
            if self.x < hero_x:
                self.x += self.speed * 0.8
                self.facing_left = False
            elif self.x > hero_x:
                self.x -= self.speed * 0.8
                self.facing_left = True

            if self.y < hero_y:
                self.y += self.speed * 0.8
            elif self.y > hero_y:
                self.y -= self.speed * 0.8

            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:
                self.animation_index = (self.animation_index + 1) % len(self.walk_frames)
                self.last_animation_time = current_time

    def shoot(self, hero_x, hero_y):
        if self.state == "shooting":
            current_time = time.time()
            if current_time - self.shoot_animation_time > 0.2:
                self.shoot_animation_index += 1
                self.shoot_animation_time = current_time
                if self.shoot_animation_index == 1:
                    for angle in range(-20, 21, 10):
                        self.bullets.append(SpreadBullet(self.x, self.y, angle, self.facing_left))
                if self.shoot_animation_index >= len(self.shoot_frames):
                    self.state = "moving"
                    self.shoot_animation_index = 0

    def update_state(self):
        if self.is_dead:
            return

        current_time = time.time()
        if current_time - self.last_state_change > self.state_change_interval:
            self.state = "shooting" if self.shoot_frames else "moving"
            self.last_state_change = current_time
            self.state_change_interval = random.uniform(1, 3)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.move()
        self.bullets = [bullet for bullet in self.bullets if bullet.active]

    def check_collision(self, bullets):
        if self.is_dead:
            return False

        for bullet in bullets:
            if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
                bullets.remove(bullet)
                self.health -= 1
                if self.health <= 0:
                    self.state = "dying"
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        if self.state == "dying":
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        current_frame = self.shoot_frames[self.shoot_animation_index] if self.state == "shooting" else self.walk_frames[self.animation_index]

        if self.facing_left:
            screen.blit(current_frame, (self.x, self.y))
        else:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

        for bullet in self.bullets:
            bullet.draw(screen)

# Класс врага Enemy9
class Enemy9:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.state = "moving"  # Состояния: "moving", "idle", "dying"
        self.last_state_change = time.time()
        self.state_change_interval = random.uniform(1, 3)
        self.bullets = []
        self.last_shot_time = time.time()
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.facing_left = True
        self.death_animation_index = 0
        self.is_dead = False
        self.hit_points = 9  # Количество попаданий до смерти

        # Загрузка фреймов напрямую
        self.walk_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_W1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_W2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_W3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_W4.png"),
        ]
        self.death_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_D1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_D2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_D3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_D4.png"),
        ]

    def move_towards_hero(self, hero_x, hero_y):
        if self.state == "moving":
            if self.x < hero_x:
                self.x += self.speed * 0.8
                self.facing_left = False
            elif self.x > hero_x:
                self.x -= self.speed * 0.8
                self.facing_left = True

            if self.y < hero_y:
                self.y += self.speed * 0.8
            elif self.y > hero_y:
                self.y -= self.speed * 0.8

            # Анимация движения
            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:
                self.animation_index = (self.animation_index + 1) % len(self.walk_frames)
                self.last_animation_time = current_time

    def shoot(self, hero_x):
        current_time = time.time()
        if current_time - self.last_shot_time > 1:
            direction = -5 if self.x > hero_x else 5
            bullet = EnemyBullet(self.x, self.y + self.size // 2, direction)
            self.bullets.append(bullet)
            self.last_shot_time = current_time

    def update_state(self):
        if self.is_dead:
            return

        current_time = time.time()
        if current_time - self.last_state_change > self.state_change_interval:
            self.state = "idle" if self.state == "moving" else "moving"
            self.last_state_change = current_time
            self.state_change_interval = random.uniform(1, 3)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.move()
        self.bullets = [bullet for bullet in self.bullets if bullet.active]

    def check_collision(self, bullets):
        if self.is_dead:
            return False

        for bullet in bullets:
            if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
                bullets.remove(bullet)
                self.hit_points -= 1
                if self.hit_points <= 0:
                    self.state = "dying"
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        if self.state == "dying":
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        current_frame = self.walk_frames[self.animation_index]
        if self.facing_left:
            screen.blit(current_frame, (self.x, self.y))
        else:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

        for bullet in self.bullets:
            bullet.draw(screen)

# Класс босса boss1
class Boss1:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.state = "moving"  # Состояния: "moving", "shooting", "dying"
        self.last_state_change = time.time()
        self.state_change_interval = random.uniform(2, 5)
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.facing_left = True
        self.death_animation_index = 0
        self.is_dead = False
        self.shoot_animation_time = time.time()
        self.hit_points = 50  # Жизни босса
        self.bullets = []

        # Прямая загрузка фреймов
        self.walk_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss1_W1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss1_W2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss1_W3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss1_W4.png"),
        ]
        self.death_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss1_D1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss1_D2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss1_D3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss1_D4.png"),
        ]

    def move_towards_hero(self, hero_x, hero_y):
        if self.state == "moving":
            if self.x < hero_x:
                self.x += self.speed
                self.facing_left = False
            elif self.x > hero_x:
                self.x -= self.speed
                self.facing_left = True

            if self.y < hero_y:
                self.y += self.speed * 0.5
            elif self.y > hero_y:
                self.y -= self.speed * 0.5

            # Анимация движения
            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:
                self.animation_index = (self.animation_index + 1) % len(self.walk_frames)
                self.last_animation_time = current_time

    def shoot(self):
        if self.state == "shooting":
            current_time = time.time()
            if current_time - self.shoot_animation_time > 0.1:
                self.shoot_animation_time = current_time
                bullet_x = self.x if self.facing_left else self.x + self.size
                bullet_y = self.y + self.size // 2
                bullet_speed = -10 if self.facing_left else 10
                self.bullets.append(EnemyBullet(bullet_x, bullet_y, bullet_speed))

    def update_state(self):
        if self.is_dead:
            return

        current_time = time.time()
        if current_time - self.last_state_change > self.state_change_interval:
            self.state = "shooting" if self.state == "moving" else "moving"
            self.last_state_change = current_time
            self.state_change_interval = random.uniform(2, 5)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.move()
        self.bullets = [bullet for bullet in self.bullets if bullet.active]

    def check_collision(self, bullets):
        if self.is_dead:
            return False

        for bullet in bullets:
            if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
                bullets.remove(bullet)
                self.hit_points -= 1
                if self.hit_points <= 0:
                    self.state = "dying"
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        if self.state == "dying":
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        current_frame = self.walk_frames[self.animation_index]
        if self.facing_left:
            screen.blit(current_frame, (self.x, self.y))
        else:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

        for bullet in self.bullets:
            bullet.draw(screen)

# Класс босса boss2
class Boss2:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.is_dead = False
        self.death_animation_index = 0
        self.facing_right = True
        self.hit_points = 30  # Количество жизней босса

        # Прямая загрузка фреймов
        self.walk_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss2_W1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss2_W2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss2_W3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss2_W4.png"),
        ]
        self.death_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss2_D1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss2_D2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss2_D3.png"),
        ]

    def move_towards_hero(self, hero_x, hero_y):
        if not self.is_dead:
            if self.x < hero_x:
                self.x += self.speed
                self.facing_right = True
            elif self.x > hero_x:
                self.x -= self.speed
                self.facing_right = False

            if self.y < hero_y:
                self.y += self.speed * 0.5
            elif self.y > hero_y:
                self.y -= self.speed * 0.5

            # Анимация движения
            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:
                self.animation_index = (self.animation_index + 1) % len(self.walk_frames)
                self.last_animation_time = current_time

    def check_collision(self, bullets):
        if self.is_dead:
            return False

        for bullet in bullets:
            if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
                bullets.remove(bullet)
                self.hit_points -= 1
                if self.hit_points <= 0:
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def check_melee_attack(self, hero_x, hero_y, hero_size):
        if not self.is_dead:
            if (
                self.x < hero_x + hero_size and
                self.x + self.size > hero_x and
                self.y < hero_y + hero_size and
                self.y + self.size > hero_y
            ):
                return True  # Атака в ближнем бою, наносит урон игроку
        return False

    def draw(self, screen):
        if self.is_dead:
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        current_frame = self.walk_frames[self.animation_index]
        if not self.facing_right:
            current_frame = pygame.transform.flip(current_frame, True, False)
        screen.blit(current_frame, (self.x, self.y))

# Класс босса boss3
class Boss3:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.is_dead = False
        self.death_animation_index = 0
        self.last_shoot_time = time.time()
        self.state = 0  # 0 - статичный, 1 - атака
        self.laser_active = False
        self.hit_points = 20  # Количество попаданий для смерти

        # Прямая загрузка фреймов
        self.shoot_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss3_S1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss3_S2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss3_S3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss3_S4.png"),
        ]
        self.death_frames = [
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss3_D1.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss3_D2.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss3_D3.png"),
            pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/boss3_D4.png"),
        ]

    def update_position(self, hero_y):
        """ Босс всегда остается на одной оси Y с героем. """
        if not self.is_dead:
            self.y = hero_y

    def attack(self):
        """ Запускает атаку каждые 3 секунды. """
        current_time = time.time()
        if not self.is_dead:
            if self.state == 1:  # Анимация атаки
                if current_time - self.last_animation_time > 0.2:  # Каждые 200 мс
                    self.animation_index = (self.animation_index + 1) % len(self.shoot_frames)
                    self.last_animation_time = current_time

                if self.animation_index == 2 and not self.laser_active:  # Лазер активируется на 3-м кадре
                    self.laser_active = True

                if self.animation_index == 0:  # Завершение цикла атаки
                    self.state = 0
                    self.laser_active = False
            else:  # Ожидание перед атакой
                if current_time - self.last_shoot_time > 3:  # 3 секунды между атаками
                    self.state = 1
                    self.animation_index = 0
                    self.last_shoot_time = current_time

    def check_collision(self, bullets):
        """ Проверяет попадания в босса. """
        if self.is_dead:
            return False

        for bullet in bullets:
            if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
                bullets.remove(bullet)
                self.hit_points -= 1
                if self.hit_points <= 0:
                    self.is_dead = True
                    self.death_animation_index = 0
                    self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        """ Отрисовка босса и его лазера при атаке. """
        if self.is_dead:
            if self.death_animation_index < len(self.death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:  # Каждые 200 мс
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(self.death_frames):
                    screen.blit(self.death_frames[self.death_animation_index], (self.x, self.y))
            return

        # Отрисовка анимации атаки или покоя
        current_frame = self.shoot_frames[self.animation_index] if self.state == 1 else self.shoot_frames[0]
        screen.blit(current_frame, (self.x, self.y))

        # Отрисовка лазера
        if self.laser_active:
            pygame.draw.rect(screen, (255, 165, 0), (self.x - 800, self.y + self.size // 2 - 2, 800, 4))  # Оранжевый лазер

#вова гуфи