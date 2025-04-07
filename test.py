import pygame
import random
from enemies import HeroBullet, EnemyBullet, HomingSausage, StraightBullet, SpreadBullet
from enemies import Enemy1  # Импорт нужных врагов

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



# Группы врагов
enemy_group = pygame.sprite.Group()

enemy_bullet_group = pygame.sprite.Group()


# Группа всех пуль героя
hero_bullet_group = pygame.sprite.Group()

# Создание врагов
gufi1 = Enemy1(0, 0)
enemy_group.add(gufi1)

# Основной игровой цикл
clock = pygame.time.Clock()
running = True

direction = 1


while running:
    SCREEN.fill(WHITE)

    keys = pygame.key.get_pressed()
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Выстрел вперёд
                bullet = HeroBullet(hero_x, hero_y, direction*5, 1)
                hero_bullet_group.add(bullet)

    # Управление героем
    
    if keys[pygame.K_LEFT]:
        direction = -1
        hero_x -= hero_speed
    if keys[pygame.K_RIGHT]:
        direction = 1
        hero_x += hero_speed
    if keys[pygame.K_UP]:
        hero_y -= hero_speed
    if keys[pygame.K_DOWN]:
        hero_y += hero_speed

    # Ограничение перемещения в пределах экрана
    hero_x = max(0, min(WIDTH - hero_size, hero_x))
    hero_y = max(0, min(HEIGHT - hero_size, hero_y))

    # Обновление врагов (с учётом разных методов)
    for enemy in enemy_group:
        enemy.update(hero_x, hero_y, hero_bullet_group, enemy_bullet_group, SCREEN)
        #enemy.draw(SCREEN)



    # Обновление пуль
    hero_bullet_group.update()
    hero_bullet_group.draw(SCREEN)
    
    enemy_bullet_group.update()
    enemy_bullet_group.draw(SCREEN)


    # Отрисовка героя
    pygame.draw.rect(SCREEN, BLUE, (hero_x, hero_y, hero_size, hero_size))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

# Завершение работы Pygame
pygame.quit()
