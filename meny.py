import pygame as pg
from random import randint
from time import sleep
from level1 import *
from shop import Shop





class Button(pg.sprite.Sprite):
    def __init__(self, image, x, y, hitbox=None):

        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        if hitbox:
            x_offset, y_offset, width, height = hitbox
            self.hitbox = pg.Rect(
                self.rect.x + x_offset, 
                self.rect.y + y_offset, 
                width, 
                height
            )
        else:

            self.hitbox = self.rect

    def draw_hitbox(self, screen):
        """
        Рисует хитбокс для визуализации (например, для отладки).
        """
        pg.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

        




class Meny():
    def __init__(self):
        pg.init()
        pg.mixer.init()
        

        screen_width, screen_height = 1920, 1080
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption("Вова гуфи")

        self.new()

    def new(self):

        self.play = True

        self.clock = pg.time.Clock()

        self.button_new_game = pg.transform.scale(pg.image.load('img_meny/new_game.png'),(500, 300))
        self.button_continue = pg.transform.scale(pg.image.load('img_meny/continue.png'),(500, 300))
        self.button_shop = pg.transform.scale(pg.image.load('img_meny/shop.png'),(500, 300))
        self.button_settings = pg.transform.scale(pg.image.load('img_meny/settings.png'),(500, 300))
        self.button_exit = pg.transform.scale(pg.image.load('img_meny/exit.png'),(500, 300))

        self.background1 = pg.transform.scale(pg.image.load("img_meny/meny1.png"),(1920, 1080))
        self.background2 = pg.transform.scale(pg.image.load("img_meny/meny2.png"),(1920, 1080))
        self.background3 = pg.transform.scale(pg.image.load("img_meny/meny3.png"),(1920, 1080))

        self.buttons = pg.sprite.Group(
        Button(self.button_new_game, 700, 200, hitbox=(30, 0, 430, 80)),
        Button(self.button_continue, 700, 300, hitbox=(30, 0, 430, 80)),
        Button(self.button_shop, 700, 400, hitbox=(30, 0, 430, 80)),
        Button(self.button_settings, 700, 500, hitbox=(30, 0, 430, 80)),
        Button(self.button_exit, 700, 600, hitbox=(30, 0, 430, 80))
        )




        self.run()


    def run(self):

        def draw_cursor_coordinates(screen):
            """
            Отображает координаты курсора в верхнем левом углу экрана.

            :param screen: поверхность pygame, на которой рисуется текст
            """
            font = pg.font.Font(None, 36)  # Используем шрифт по умолчанию, размером 36
            mouse_x, mouse_y = pg.mouse.get_pos()
            text_surface = font.render(f"X: {mouse_x}, Y: {mouse_y}", True, (255, 255, 255))
            screen.blit(text_surface, (10, 10))  # Рисуем текст в левом верхнем углу

        running = True
        timer = 0
        while running:
            
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.hitbox.collidepoint(event.pos):
                            if button.image == self.button_new_game:
                                print("Новая игра")
                                a = Level_one()
                            elif button.image == self.button_continue:
                                print("Продолжить")
                            elif button.image == self.button_shop:
                                print("Магазин")
                                b = Shop()
                            elif button.image == self.button_settings:
                                print("Настройки")
                            elif button.image == self.button_exit:
                                print("Выход")
                                running = False
            self.buttons.draw(self.screen)

            for button in self.buttons:
                button.draw_hitbox(self.screen)


            timer += 1
            if timer == 60:
                self.screen.blit(self.background1, (0,0))
                draw_cursor_coordinates(self.screen)
            if timer == 120:
                self.screen.blit(self.background2, (0,0))
                draw_cursor_coordinates(self.screen)
            if timer == 180:
                self.screen.blit(self.background3, (0,0))
                draw_cursor_coordinates(self.screen)
            if timer > 180:
                timer = 0
            
            
            pg.display.update()


g = Meny()