import pygame
import random
from enemies_fixed import Enemy6, Enemy7, Enemy8, Boss1, Boss2, Boss3  # Импорт нужных врагов

# Инициализация Pygame
pygame.init()

# Основные параметры окна
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Уровень с разными врагами")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Параметры героя
hero_size = 50
hero_x = WIDTH // 2
hero_y = HEIGHT // 2
hero_speed = 5
hero_bullets = []

# Класс пули героя
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > WIDTH:
            self.kill()

# Группы врагов
enemy6_group = pygame.sprite.Group()
enemy7_group = pygame.sprite.Group()
enemy8_group = pygame.sprite.Group()
boss1_group = pygame.sprite.Group()
boss2_group = pygame.sprite.Group()
boss3_group = pygame.sprite.Group()

# Группа всех пуль героя
hero_bullet_group = pygame.sprite.Group()

# Создание врагов
for _ in range(2):
    enemy6_group.add(Enemy6(random.randint(600, 750), random.randint(50, 550)))
    enemy7_group.add(Enemy7(random.randint(600, 750), random.randint(50, 550)))
    enemy8_group.add(Enemy8(random.randint(600, 750), random.randint(50, 550)))

boss1_group.add(Boss1(650, 200))
boss2_group.add(Boss2(650, 300))
boss3_group.add(Boss3(650, 400))

# Основной игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    SCREEN.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Выстрел вперёд
                bullet = Bullet(hero_x + hero_size, hero_y + hero_size // 2, 7)
                hero_bullet_group.add(bullet)

    # Управление героем
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

    # Обновление врагов (с учётом разных методов)
    for enemy in enemy6_group:
        enemy.move_towards_hero(hero_x, hero_y)
        enemy.shoot(hero_x, hero_y)
        enemy.draw(SCREEN)

    for enemy in enemy7_group:
        enemy.move_towards_hero(hero_x, hero_y)
        enemy.shoot(hero_x, hero_y)
        enemy.draw(SCREEN)

    for enemy in enemy8_group:
        enemy.move_towards_hero(hero_x, hero_y)
        enemy.shoot(hero_x, hero_y)
        enemy.draw(SCREEN)

    for boss in boss1_group:
        boss.move_towards_hero(hero_x, hero_y)
        boss.shoot()
        boss.draw(SCREEN)

    for boss in boss2_group:
        boss.move_towards_hero(hero_x, hero_y)
        boss.draw(SCREEN)

    for boss in boss3_group:
        boss.update_position(hero_y)
        boss.attack()
        boss.draw(SCREEN)

    # Обновление пуль
    hero_bullet_group.update()
    hero_bullet_group.draw(SCREEN)

    # Отрисовка героя
    pygame.draw.rect(SCREEN, BLUE, (hero_x, hero_y, hero_size, hero_size))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

# Завершение работы Pygame
pygame.quit()
