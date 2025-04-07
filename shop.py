# Импорт библиотеки pygame для создания игры
import pygame as pg


# Класс Button наследуется от pg.sprite.Sprite для создания кнопок
class Button(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        # Вызов конструктора родительского класса, Установка изображения кнопки, 
        # Получение прямоугольника изображения для обработки коллизий, 
        # Установка позиции кнопки на экране
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# Класс Shop для создания магазина в игре
class Shop:
    def __init__(self):
        # Инициализация pygame и звукового модуля
        pg.init()
        pg.mixer.init()

        # Установка размеров экрана, Установка заголовка окна и Создание окна игры
        screen_width, screen_height = 1920, 1080
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption("Вова Гуфи")

        # Запуск метода для создания новой игры
        self.new()

    def new(self):
        # Установка флага для игрового цикла и объекта для контроля FPS
        self.play = True
        self.clock = pg.time.Clock()

        # Загрузка и масштабирование изображений кнопок
        self.button_arrow_right = pg.transform.scale(pg.image.load('img_shop/arrow_right.png'), (300, 300))
        self.button_arrow_left = pg.transform.scale(pg.image.load('img_shop/arrow_left.png'), (300, 300))
        self.button_buy = pg.transform.scale(pg.image.load('img_shop/buy.png'), (600, 600))
        self.button_back = pg.transform.scale(pg.image.load('img_shop/back.png'), (600, 600))

        # Загрузка и масштабирование изображений предметов
        self.ak_sprite = pg.transform.scale(pg.image.load('img_shop/AK.png'), (500, 300))
        self.pm_sprite = pg.transform.scale(pg.image.load('img_shop/PM.png'), (500, 300))
        self.rpg7_sprite = pg.transform.scale(pg.image.load('img_shop/RPG7.png'), (500, 300))
        # Создание списка предметов и индекса текущего отображаемого предмета
        self.items = [self.ak_sprite, self.pm_sprite, self.rpg7_sprite]  
        self.current_item_index = 0  

        # Загрузка и масштабирование фонового изображения
        self.background = pg.transform.scale(pg.image.load("img_shop/phon.png"), (1920, 1080))

        # Создание объектов кнопок
        self.button_left = Button(self.button_arrow_left, 30, 330)
        self.button_right = Button(self.button_arrow_right, 1530, 330)
        self.button_buy = Button(self.button_buy, 650, 500)
        self.button_back = Button(self.button_back, 20, 700)

        # Группировка кнопок для удобного отображения и обработки
        self.buttons = pg.sprite.Group(self.button_left, self.button_right, self.button_buy, self.button_back)

        # Запуск основного игрового цикла
        self.run()
    # Флаг для основного цикла
    def run(self):
        running = True
        while running:
            #60FPS
            self.clock.tick(60)
            # Обработка событий pygame
            for event in pg.event.get():
                if event.type == pg.QUIT:                   # Обработка выхода из игры
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    # Проверка нажатия на кнопки
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            if button == self.button_left:
                                # Переключение на предыдущий предмет
                                self.current_item_index -= 1
                                if self.current_item_index < 0:
                                    self.current_item_index = len(self.items) - 1
                            elif button == self.button_right:
                                # Переключение на следующий предмет
                                self.current_item_index += 1
                                if self.current_item_index >= len(self.items):
                                    self.current_item_index = 0
                            # Обработка нажатия на кнопку "купить"
                            elif button == self.button_buy:
                                print(f"Item {self.current_item_index + 1} purchased!")
                            elif button == self.button_back:
                                running = False

            # Отрисовка фона
            self.screen.blit(self.background, (0, 0))  
            self.buttons.draw(self.screen)

            # Получение текущего предмета и его отрисовка
            current_item = self.items[self.current_item_index]
            self.screen.blit(current_item, (680, 300))

            # Обновление экрана
            pg.display.update()