import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Shop:
    def __init__(self):
        pg.init()
        pg.mixer.init()

        screen_width, screen_height = 1920, 1080
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption("Вова Гуфи")

        self.new()

    def new(self):
        self.play = True
        self.clock = pg.time.Clock()


        self.button_arrow_right = pg.transform.scale(pg.image.load('img_shop/arrow_right.png'), (300, 300))
        self.button_arrow_left = pg.transform.scale(pg.image.load('img_shop/arrow_left.png'), (300, 300))
        self.button_buy = pg.transform.scale(pg.image.load('img_shop/buy.png'), (600, 600))
        self.button_back = pg.transform.scale(pg.image.load('img_shop/back.png'), (600, 600))

        self.ak_sprite = pg.transform.scale(pg.image.load('img_shop/AK.png'), (500, 300))
        self.pm_sprite = pg.transform.scale(pg.image.load('img_shop/PM.png'), (500, 300))
        self.rpg7_sprite = pg.transform.scale(pg.image.load('img_shop/RPG7.png'), (500, 300))
        self.items = [self.ak_sprite, self.pm_sprite, self.rpg7_sprite]  
        self.current_item_index = 0  

        self.background = pg.transform.scale(pg.image.load("img_shop/phon.png"), (1920, 1080))


        self.button_left = Button(self.button_arrow_left, 30, 330)
        self.button_right = Button(self.button_arrow_right, 1530, 330)
        self.button_buy = Button(self.button_buy, 650, 500)
        self.button_back = Button(self.button_back, 20, 700)

        self.buttons = pg.sprite.Group(self.button_left, self.button_right, self.button_buy, self.button_back)

        self.run()

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            if button == self.button_left:

                                self.current_item_index -= 1
                                if self.current_item_index < 0:
                                    self.current_item_index = len(self.items) - 1
                            elif button == self.button_right:

                                self.current_item_index += 1
                                if self.current_item_index >= len(self.items):
                                    self.current_item_index = 0
                            elif button == self.button_buy:

                                print(f"Item {self.current_item_index + 1} purchased!")
                            elif button == self.button_back:
                                running = False


            self.screen.blit(self.background, (0, 0))  
            self.buttons.draw(self.screen)


            current_item = self.items[self.current_item_index]
            self.screen.blit(current_item, (680, 300))

            pg.display.update()



gufio = Shop()