import pygame
import math
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
explosion_images = [pygame.image.load(f"C:\\Users\\Bruker\\Documents\\GitHub\\spillutvikling-fedir-og-vova\\img\\explosion_{i}.png") for i in range(1, 16)]

# Загрузка изображений оружия
pm_image = pygame.image.load("C:\\Users\\Bruker\\Documents\\GitHub\\spillutvikling-fedir-og-vova\\img_shop\\pm.png")
ak_image = pygame.image.load("C:\\Users\\Bruker\\Documents\\GitHub\\spillutvikling-fedir-og-vova\\img_shop\\ak.png")
rpg7_image = pygame.image.load("C:\\Users\\Bruker\\Documents\\GitHub\\spillutvikling-fedir-og-vova\\img_shop\\rpg7.png")

# Список оружия и текущий индекс
weapons = [pm_image, ak_image, rpg7_image]
current_weapon_index = 0  # Начальное оружие - pm

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

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = (255, 0, 0)
        self.speed = speed
        self.vertical_speed = speed * 2  # Увеличенная вертикальная скорость
        self.moving = False
        self.move_time = 0
        self.shoot_time = 0
        self.shots_to_fire = random.randint(1, 3)
        self.shots_fired = 0
        self.target_distance = random.uniform(30, 100)  # Случайное расстояние движения к игроку
        self.distance_moved = 0
        self.bullets = []  # Список пуль врага
        self.bullet_speed = 5  # Скорость пуль врага

    def shoot(self, player_pos):
        # Пули движутся только по горизонтали
        direction = 1 if player_pos[0] > self.x else -1
        self.bullets.append({
            "pos": [self.x + self.width // 2, self.y + self.height // 2],
            "vel": [direction * self.bullet_speed, 0]
        })

    def update(self, player_pos):
        if not self.moving:  # Остановка для стрельбы
            self.shoot_time += clock.get_time()
            if self.shoot_time >= 1000 and self.shots_fired < self.shots_to_fire:
                self.shoot(player_pos)
                self.shots_fired += 1
                self.shoot_time = 0

            if self.shots_fired >= self.shots_to_fire:
                self.moving = True
                self.shots_fired = 0
                self.distance_moved = 0
                self.target_distance = random.uniform(30, 100)
        else:  # Движение к игроку
            dx = player_pos[0] - self.x
            dy = player_pos[1] - self.y
            distance = math.hypot(dx, dy)
            if distance != 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.vertical_speed
                self.distance_moved += self.speed

            if self.distance_moved >= self.target_distance:
                self.moving = False

        # Обновление пуль
        for bullet in self.bullets:
            bullet["pos"][0] += bullet["vel"][0]
            bullet["pos"][1] += bullet["vel"][1]

        # Удаление пуль, выходящих за экран
        self.bullets = [bullet for bullet in self.bullets if 0 <= bullet["pos"][0] <= WIDTH and 0 <= bullet["pos"][1] <= HEIGHT]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Рисуем пули врага
        for bullet in self.bullets:
            pygame.draw.rect(screen, (0, 0, 255), (*bullet["pos"], 5, 5))





# Функция добавления врагов
def add_enemy():
    x = WIDTH + random.randint(20, 100)  # Враги появляются справа от экрана
    y = random.randint(0, HEIGHT - 50)
    speed = random.uniform(1, 3)  # Случайная скорость от 1 до 3
    enemies.append(Enemy(x, y, speed))

# Список врагов
enemies = [Enemy(WIDTH + random.randint(0, 100), random.randint(0, HEIGHT - 50), random.uniform(1, 3)) for _ in range(5)]


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
                current_weapon_index = 0  # Выбор pm
            elif event.key == pygame.K_2:
                shooting_mode = 2  # Стрельба с калаша
                current_weapon_index = 1  # Выбор ak
            elif event.key == pygame.K_3:
                shooting_mode = 3  # Стрельба с RPG
                current_weapon_index = 2  # Выбор rpg7
            elif event.key == pygame.K_r:  # Перезарядка
                if ammo < max_ammo and reserve_ammo > 0 and not reloading:
                    reloading = True
                    reload_start_time = pygame.time.get_ticks()

    # Проверка на столкновение с целью (если пуля выходит за экран, удаляем)
    new_bullets = []
    for bullet in bullets:
        if 0 <= bullet["pos"][0] <= WIDTH and 0 <= bullet["pos"][1] <= HEIGHT:
            new_bullets.append(bullet)
        else:
            if bullet.get("type") == "explosive":
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

    # Рисуем текущее оружие
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - (player_pos[0] + player_size // 2)
    dy = mouse_y - (player_pos[1] + player_size // 2)
    angle = math.atan2(dy, dx)
    current_weapon_image = weapons[current_weapon_index]
    rotated_weapon = pygame.transform.rotate(current_weapon_image, -math.degrees(angle))
    weapon_rect = rotated_weapon.get_rect(center=(player_pos[0] + player_size // 2, player_pos[1] + player_size // 2))
    screen.blit(rotated_weapon, weapon_rect.topleft)

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

    # Обновление врагов
    for enemy in enemies:
        enemy.update(player_pos)
        enemy.draw(screen)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
