import pygame
import sys
import random
import time

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Главный герой и враг")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Загрузка изображений врага
enemy_frames = [
    pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_W1.png"),
    pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_W2.png"),
    pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_W3.png"),
    pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_W4.png")
]

death_frames = [
    pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_D1.png"),
    pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_D2.png"),
    pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_D3.png"),
    pygame.image.load("C:/Users/Bruker/Documents/GitHub/spillutvikling-fedir-og-vova/enemyframes/en9_D4.png")
]

# Параметры героя
hero_size = 50
hero_x = WIDTH // 2
hero_y = HEIGHT // 2
hero_speed = 5
hero_bullets = []

# Класс пули
class Bullet:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.active = True

    def move(self):
        self.x += self.speed
        if self.x < 0 or self.x > WIDTH:
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 10, 5))

# Класс врага
class Enemy:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.state = "moving"  # Состояния: "moving", "idle" или "dying"
        self.last_state_change = time.time()
        self.state_change_interval = random.uniform(1, 3)  # Интервал 1-3 секунды
        self.bullets = []
        self.last_shot_time = time.time()
        self.animation_index = 0
        self.last_animation_time = time.time()
        self.facing_left = True
        self.death_animation_index = 0
        self.is_dead = False

    def move_towards_hero(self, hero_x, hero_y):
        if self.state == "moving":
            if self.x < hero_x:
                self.x += self.speed * 0.8  # Уменьшена скорость
                self.facing_left = False
            elif self.x > hero_x:
                self.x -= self.speed * 0.8  # Уменьшена скорость
                self.facing_left = True

            if self.y < hero_y:
                self.y += self.speed * 0.8  # Уменьшена скорость
            elif self.y > hero_y:
                self.y -= self.speed * 0.8  # Уменьшена скорость

            # Анимация движения
            current_time = time.time()
            if current_time - self.last_animation_time > 0.2:  # Каждые 200 мс
                self.animation_index = (self.animation_index + 1) % len(enemy_frames)
                self.last_animation_time = current_time

    def shoot(self, hero_x):
        current_time = time.time()
        if current_time - self.last_shot_time > 1:  # Враг стреляет раз в секунду
            direction = -5 if self.x > hero_x else 5  # Определяем направление стрельбы
            bullet = Bullet(self.x, self.y + self.size // 2, direction)
            self.bullets.append(bullet)
            self.last_shot_time = current_time

    def update_state(self):
        if self.is_dead:
            return

        current_time = time.time()
        if current_time - self.last_state_change > self.state_change_interval:
            self.state = "idle" if self.state == "moving" else "moving"
            self.last_state_change = current_time
            self.state_change_interval = random.uniform(1, 3)  # Новый интервал 1-3 секунды

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
                self.state = "dying"
                self.is_dead = True
                self.death_animation_index = 0
                self.last_animation_time = time.time()
                return True
        return False

    def draw(self, screen):
        if self.state == "dying":
            if self.death_animation_index < len(death_frames):
                current_time = time.time()
                if current_time - self.last_animation_time > 0.2:  # Каждые 200 мс
                    self.death_animation_index += 1
                    self.last_animation_time = current_time
                if self.death_animation_index < len(death_frames):
                    screen.blit(death_frames[self.death_animation_index], (self.x, self.y))
            return

        current_frame = enemy_frames[self.animation_index] if self.state == "moving" else enemy_frames[0]
        if self.facing_left:
            screen.blit(current_frame, (self.x, self.y))
        else:
            flipped_frame = pygame.transform.flip(current_frame, True, False)
            screen.blit(flipped_frame, (self.x, self.y))

        for bullet in self.bullets:
            bullet.draw(screen)

# Создание врага
enemy = Enemy(WIDTH + 50, random.randint(0, HEIGHT - 50), 50, 2)

# Основной цикл игры
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Выстрел вперёд
                hero_bullets.append(Bullet(hero_x + hero_size, hero_y + hero_size // 2, 7))
            elif event.key == pygame.K_LSHIFT:  # Выстрел назад
                hero_bullets.append(Bullet(hero_x, hero_y + hero_size // 2, -7))

    # Управление с помощью клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        hero_x -= hero_speed
    if keys[pygame.K_RIGHT]:
        hero_x += hero_speed
    if keys[pygame.K_UP]:
        hero_y -= hero_speed
    if keys[pygame.K_DOWN]:
        hero_y += hero_speed

    # Ограничение перемещения в пределах экрана
    hero_x = max(0, min(WIDTH - hero_size, hero_x))
    hero_y = max(0, min(HEIGHT - hero_size, hero_y))

    # Логика врага
    enemy.update_state()
    if enemy.state == "moving":
        enemy.move_towards_hero(hero_x, hero_y)
    elif enemy.state == "idle":
        enemy.shoot(hero_x)
    enemy.update_bullets()

    # Проверка попаданий
    if enemy.check_collision(hero_bullets):
        pass  # Враг в состоянии смерти, ничего не делаем

    for bullet in hero_bullets:
        bullet.move()

    hero_bullets = [bullet for bullet in hero_bullets if bullet.active]

    # Отрисовка
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, BLUE, (hero_x, hero_y, hero_size, hero_size))
    for bullet in hero_bullets:
        bullet.draw(SCREEN)
    enemy.draw(SCREEN)
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)

# Завершение работы Pygame
pygame.quit()
sys.exit()
