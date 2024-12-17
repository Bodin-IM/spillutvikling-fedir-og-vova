import pygame as pg
import sys
from level1 import *

class Cutscene:
    def __init__(self):
        pg.init()
        self.screen_width, self.screen_height = 1920, 1080
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Вова Гуфи")

        self.clock = pg.time.Clock()

        
        self.logo = pg.image.load('img_cutscene1/game_name.png')  # Логотип
        self.building = pg.image.load('img_cutscene1/voenkomat_sprite.png')  # Здание
        self.character = pg.image.load('img_cutscene1/main_char.png')  # Персонаж

        
        self.logo = pg.transform.scale(self.logo, (600, 300))
        self.building = pg.transform.scale(self.building, (1333, 1000))
        self.character = pg.transform.scale(self.character, (100, 200))

        
        self.building_x = 200  
        self.character_x = self.building_x + 1000
        self.character_y = self.screen_height - 200

        self.run_cutscene()

    def draw_logo(self):
        
        alpha = 0
        logo_surface = self.logo.copy()
        while alpha < 255:
            self.screen.fill((0, 0, 0))  
            logo_surface.set_alpha(alpha)
            self.screen.blit(logo_surface, ((self.screen_width - self.logo.get_width()) // 2, 
                                            (self.screen_height - self.logo.get_height()) // 2))
            alpha += 5
            pg.display.update()
            self.clock.tick(30)

        
        while alpha > 0:
            self.screen.fill((0, 0, 0))  
            logo_surface.set_alpha(alpha)
            self.screen.blit(logo_surface, ((self.screen_width - self.logo.get_width()) // 2, 
                                            (self.screen_height - self.logo.get_height()) // 2))
            alpha -= 5
            pg.display.update()
            self.clock.tick(30)

    def draw_image(self, image_path, width, height, display_time=1000):
        """
        Отображает изображение по центру экрана с эффектом появления и исчезновения.
        
        :param image_path: Путь к изображению
        :param width: Ширина изображения
        :param height: Высота изображения
        :param display_time: Время (в мс), в течение которого изображение остаётся на экране
        """
       
        image = pg.image.load(image_path)
        image = pg.transform.scale(image, (width, height))
        
        
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2
        
        
        alpha = 0
        temp_surface = image.copy()
        while alpha < 255:
             
            temp_surface.set_alpha(alpha)  
            self.screen.blit(temp_surface, (x, y))
            alpha += 5
            pg.display.update()
            self.clock.tick(30)
        
        
        pg.time.wait(display_time)
        
        
        while alpha > 0:
            
            temp_surface.set_alpha(alpha)  
            self.screen.blit(temp_surface, (x, y))
            alpha -= 5
            pg.display.update()
            self.clock.tick(30)



    def type_story(self, text, font, color, x, y, char_delay=100, line_delay=500):
        
        lines = text.split('\n')
        surface = self.screen.copy()
        self.screen.fill((0, 0, 0))  

        
        current_y = y
        for line in lines:
            rendered_text = ""
            for char in line:
                rendered_text += char
                text_surface = font.render(rendered_text, True, color)
                self.screen.blit(surface, (0, 0))  
                self.screen.blit(text_surface, (x, current_y))
                pg.display.update()
                pg.time.wait(char_delay)  
            current_y += font.get_linesize()  
            pg.time.wait(line_delay)  




    def animate_building_and_character(self):
        while self.character_x < 1800:
            self.screen.fill((0, 0, 0))  

            
            self.screen.blit(self.building, (self.building_x, self.screen_height - self.building.get_height()))

            
            self.building_x -= 1

            
            if self.building_x < 800:
                self.character_moving = True

            
            if self.character_moving and self.character_x < self.screen_width:
                self.screen.blit(self.character, (self.character_x, self.character_y))
                self.character_x += 2

            pg.display.update()
            self.clock.tick(60)

    def run_cutscene(self):
        
        
        self.screen.fill((0, 0, 0))
        pg.display.update()
        pg.time.wait(1000)
        

        font = pg.font.Font(None, 48) 
        story_text = 'Made by Vova "Zhostkiy" development'
        self.type_story(story_text, font, (255, 0, 0), 600, 400, char_delay=50, line_delay=300)
        self.draw_image('img_cutscene1/gufi.png', 200, 200, display_time=500)
        pg.time.wait(1000)
        self.screen.fill((0,0,0))

        story_text = "When back from army...\nI want to drink vodka\n SUKA BLYAT"
        self.type_story(story_text, font, (255, 255, 255), 100, 600, char_delay=50, line_delay=3000)
        self.draw_image('img_cutscene1/vodka.png', 200, 800, display_time=500)


        pg.time.wait(1000)

        
        self.draw_logo()

        
        self.animate_building_and_character()

        pg.time.wait(2000)

        level123 = Level_one()




cutscene = Cutscene()
cutscene.run_cutscene()






        

    