import pygame 
import math
import time
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ходьба, бег и стрельба")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Настройки персонажа
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 50
player_color = GREEN
walk_speed = 4
run_speed = 8

# Настройки выносливости
max_stamina = 100
stamina = max_stamina
stamina_recovery_rate = 0.5
stamina_drain_rate = 1.5
stamina_run_threshold = 25
can_run = True

# Настройки оружия
bullet_color = BLACK
bullet_speed = 10
bullets = []
shooting_mode = 1  # Режим стрельбы по умолчанию
explosions = []
# Боезапас
ammo = 30  # Патроны в обойме
max_ammo = 30
reserve_ammo = 120  # Запасные патроны
reload_time = 2.5  # Время перезарядки в секундах
reloading = False
reload_start_time = 0

# Время обновления
clock = pygame.time.Clock()
FPS = 60

# Флаг состояния игры
running = True

# Загрузка спрайтов для взрыва с номерами от 1 до 15
explosion_images = [pygame.image.load(f"explosion_{i}.png") for i in range(1, 16)]  # Загрузите ваши спрайты с именами explosion_1.png до explosion_15.png

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image_index = 0  # Индекс текущего кадра анимации
        self.max_frames = len(explosion_images)  # Количество кадров в анимации
        self.timer = 0  # Таймер для смены кадров анимации

    def update(self):
        self.timer += 1
        if self.timer > 5:  # Пауза между кадрами
            self.timer = 0
            self.image_index += 1
            if self.image_index >= self.max_frames:  # После последнего кадра взрыв исчезает
                return False
        return True

    def draw(self, screen):
        screen.blit(explosion_images[self.image_index], (self.x, self.y))

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
            if ammo > 0 and not reloading:
                # Рассчитать направление выстрела
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - (player_pos[0] + player_size // 2)
                dy = mouse_y - (player_pos[1] + player_size // 2)
                angle = math.atan2(dy, dx)

                # В зависимости от режима стрельбы
                if shooting_mode == 1:  # Обычная стрельба
                    bullets.append({
                        "pos": [player_pos[0] + player_size // 2, player_pos[1] + player_size // 2],
                        "vel": [math.cos(angle) * bullet_speed, math.sin(angle) * bullet_speed]
                    })
                    ammo -= 1
                elif shooting_mode == 2:  # Стрельба с калаша
                    for i in range(3):  # Стрельба тремя пулями
                        spread_angle = angle + (random.random() * 0.2 - 0.1)  # Немного отклонений
                        bullets.append({
                            "pos": [player_pos[0] + player_size // 2, player_pos[1] + player_size // 2],
                            "vel": [math.cos(spread_angle) * bullet_speed, math.sin(spread_angle) * bullet_speed]
                        })
                    ammo -= 3  # Тратим 3 патрона
                elif shooting_mode == 3:  # Стрельба с RPG
                    # Создаем снаряд RPG
                    bullets.append({
                        "pos": [player_pos[0] + player_size // 2, player_pos[1] + player_size // 2],
                        "vel": [math.cos(angle) * 5, math.sin(angle) * 5],  # Меньшая скорость для RPG
                        "type": "explosive"
                    })
                    ammo -= 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                shooting_mode = 1  # Обычная стрельба
            elif event.key == pygame.K_2:
                shooting_mode = 2  # Стрельба с калаша
            elif event.key == pygame.K_3:
                shooting_mode = 3  # Стрельба с RPG


        # Проверка на столкновение с целью (если пуля выходит за экран, удаляем)
        new_bullets = []
        for bullet in bullets:
            if 0 <= bullet["pos"][0] <= WIDTH and 0 <= bullet["pos"][1] <= HEIGHT:
                new_bullets.append(bullet)
            else:
                if bullet["type"] == "explosive":
                    # Добавляем взрыв в место, где пуля исчезла
                    explosions.append(Explosion(bullet["pos"][0], bullet["pos"][1]))
        bullets = new_bullets


    # Обновление состояния перезарядки
    if reloading:
        elapsed_time = (pygame.time.get_ticks() - reload_start_time) / 1000
        if elapsed_time >= reload_time:
            reload_amount = min(max_ammo - ammo, reserve_ammo)
            ammo += reload_amount
            reserve_ammo -= reload_amount
            reloading = False

    # Получение нажатий клавиш
    keys = pygame.key.get_pressed()

    # Движение персонажа
    move_x, move_y = 0, 0
    current_speed = walk_speed

    if keys[pygame.K_LSHIFT] and can_run and stamina > 0:
        current_speed = run_speed
        stamina -= stamina_drain_rate
        if stamina <= 0:
            stamina = 0
            can_run = False
    else:
        stamina += stamina_recovery_rate
        if stamina > max_stamina:
            stamina = max_stamina
        if stamina >= stamina_run_threshold:
            can_run = True

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        move_y -= current_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        move_y += current_speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        move_x -= current_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        move_x += current_speed

    player_pos[0] += move_x
    player_pos[1] += move_y

    # Ограничение движения в пределах экрана
    player_pos[0] = max(0, min(WIDTH - player_size, player_pos[0]))
    player_pos[1] = max(0, min(HEIGHT - player_size, player_pos[1]))

    # Обновление пуль
    for bullet in bullets:
        bullet["pos"][0] += bullet["vel"][0]
        bullet["pos"][1] += bullet["vel"][1]

    # Удаление пуль, выходящих за экран
    bullets = [bullet for bullet in bullets if 0 <= bullet["pos"][0] <= WIDTH and 0 <= bullet["pos"][1] <= HEIGHT]


    # Рендеринг
    screen.fill(WHITE)

    # Рисуем персонажа
    pygame.draw.rect(screen, player_color, (*player_pos, player_size, player_size))

    # Рисуем оружие
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - (player_pos[0] + player_size // 2)
    dy = mouse_y - (player_pos[1] + player_size // 2)
    angle = math.atan2(dy, dx)
    gun_length = 40
    gun_width = 10
    gun_x = player_pos[0] + player_size // 2 + math.cos(angle) * gun_length
    gun_y = player_pos[1] + player_size // 2 + math.sin(angle) * gun_length
    pygame.draw.line(screen, BLACK, (player_pos[0] + player_size // 2, player_pos[1] + player_size // 2), (gun_x, gun_y), gun_width)

    # Рисуем пули
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, (*bullet["pos"], 10, 5))

    # Обновление и рисование взрывов
    explosions = [explosion for explosion in explosions if explosion.update()]

    # Рисуем взрывы
    for explosion in explosions:
        explosion.draw(screen)

    # Рисуем шкалу выносливости
    stamina_bar_width = 200
    stamina_bar_height = 20
    stamina_bar_x = 10
    stamina_bar_y = 10
    pygame.draw.rect(screen, RED, (stamina_bar_x, stamina_bar_y, stamina_bar_width, stamina_bar_height))
    pygame.draw.rect(screen, GREEN, (stamina_bar_x, stamina_bar_y, stamina_bar_width * (stamina / max_stamina), stamina_bar_height))

    # Рисуем боезапас
    font = pygame.font.SysFont(None, 36)
    ammo_text = font.render(f"Ammo: {ammo}/{reserve_ammo}", True, BLACK)
    screen.blit(ammo_text, (10, 40))

    # Отображение статуса перезарядки
    if reloading:
        reload_text = font.render("Reloading...", True, RED)
        screen.blit(reload_text, (10, 70))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
