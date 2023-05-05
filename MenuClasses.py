import random

import pygame
from MotherClasses import Buttons, Window
from GameClasses import SpeedEnemy, BossSpaceship, NormalEnemy, Hearts
from Level3 import Endboss
#einzelne Buttons


class LevelButton(Buttons):
    def __init__(self):
        x = 200
        y = 200
        image = "rounded-rectangle.png"
        extra_image_sizex = 128
        extra_image_sizey = 128
        bg_image = "ray_shield.png"
        bgimage_sizex = 120
        bgimage_sizey = 70
        text = 'Levels'
        plus_vecx = 3
        plus_vecy = 30
        super().__init__(x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey,
                         text, plus_vecx, plus_vecy)


class HighScoreButton(Buttons):
    def __init__(self):
        x = 600
        y = 200
        image = "rounded-rectangle.png"
        extra_image_sizex = 128
        extra_image_sizey = 128
        bg_image = "ray_shield.png"
        bgimage_sizex = 120
        bgimage_sizey = 70
        text = 'Scores'
        plus_vecx = 3
        plus_vecy = 30
        super().__init__(x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey,
                         text, plus_vecx, plus_vecy)


class FastGame(Buttons):
    def __init__(self):
        x = 400
        y = 200
        image = "rounded-rectangle.png"
        extra_image_sizex = 100
        extra_image_sizey = 134
        bg_image = "play.png"
        bgimage_sizex = 100
        bgimage_sizey = 70
        text = 'Play'
        plus_vecx = 3
        plus_vecy = 30
        super().__init__(x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey,
                         text, plus_vecx, plus_vecy)


class ChooseLevelButtons(Buttons):
    def __init__(self, x, y):
        image = "rounded-rectangle.png"
        extra_image_sizex = 128
        extra_image_sizey = 128
        bg_image = "play.png"
        bgimage_sizex = 120
        bgimage_sizey = 70
        text = 'Level'
        plus_vecx = 3
        plus_vecy = 30
        super().__init__(x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey,
                         text, plus_vecx, plus_vecy)


# Game Windows

class MenuWindow(Window):
    def __init__(self):
        caption = 'Menu'
        image = "menu_bg.png"
        window_open = True
        super().__init__(caption, image, window_open)
        self.level_button = LevelButton()
        self.high_score_button = HighScoreButton()
        self.fast_game_button = FastGame()
        pygame.mixer.init()
        self.group.add(self.level_button)
        self.group.add(self.high_score_button)
        self.group.add(self.fast_game_button)

    def draw(self, m_pos):
        super().draw(m_pos)
        self.print_headline((320, 50))
        for sprite in self.group.sprites():
            sprite.draw_text(self.screen, 27, sprite.rect.x + 6, sprite.rect.y + 40, str(sprite.text))

    def update(self, m_pos, current_time, lvl_window, hs_window, menu_window, game_window, level_three_window):
        for sprite in self.group.sprites():
            sprite.action = sprite.update(m_pos, menu_window, game_window, level_three_window)
            if self.level_button.action:
                self.w_bool = False
                lvl_window.window_open = True
                self.level_button.action = False
            if self.high_score_button.action:
                self.w_bool = False
                hs_window.window_open = True
                self.high_score_button.action = False
            if self.fast_game_button.action:
                for _ in range(7):
                    game_window.enemy_group.add(NormalEnemy(random.randint(0, 736), random.randint(-130, -60)))

                for _ in range(1):
                    game_window.enemy_group.add(SpeedEnemy(random.randint(0, 736), random.randint(-130, -60)))

                for _ in range(0):
                    game_window.enemy_group.add(BossSpaceship(random.randint(0, 736), 50))

                for heart in range(3):
                    hearts = Hearts(16 + heart * 16, 45)
                    game_window.heart_group.add(hearts)

                game_window.player_group.add(game_window.player_spaceship)
                game_window.player_spaceship.lives = 3
                game_window.player_spaceship.rect.x = 400
                game_window.player_spaceship.rect.y = 515
                game_window.player_spaceship.dead = False
                game_window.player_spaceship.z = True
                game_window.window_open = True
                menu_window.window_open = False
                game_window.pause.action = False
                game_window.name_field.action = False
                self.fast_game_button.action = False


class LevelWindow(Window):
    def __init__(self):
        caption = 'Levels'
        image = "level_bg.jpg"
        window_open = False
        super().__init__(caption, image, window_open)
        for levels in range(3):
            self.group.add(ChooseLevelButtons(200 + levels * 200, 300))
        self.group.add(self.back_button)

    def draw(self, m_pos):
        super().draw(m_pos)
        self.print_headline((290, 50))
        for sprite in self.group.sprites():
            sprite.draw(m_pos, self.screen)
            sprite.draw_text(self.screen, 24, sprite.rect.x + 10, sprite.rect.y + 39,
                             sprite.text + str(self.group.sprites().index(sprite) + 1))

    def update(self, m_pos, current_time, lvl_window, hs_window, menu_window, game_window, level_three_window):
        super().update(m_pos, current_time, lvl_window, hs_window, menu_window, game_window, level_three_window)
        for sprite in self.group.sprites():
            sprite.action = sprite.update(m_pos, menu_window, game_window, level_three_window)
        if self.group.sprites()[2].action:
            level_three_window.window_open = True
            level_three_window.enemy_group.add(Endboss(300, -400))

            for heart in range(3):
                hearts = Hearts(16 + heart * 16, 45)
                level_three_window.heart_group.add(hearts)

            level_three_window.player_group.add(level_three_window.player_spaceship)
            level_three_window.player_spaceship.lives = 3
            level_three_window.player_spaceship.rect.x = 400
            level_three_window.player_spaceship.rect.y = 515
            level_three_window.player_spaceship.dead = False
            level_three_window.player_spaceship.z = True
            self.group.sprites()[2].action = False
            self.w_bool = False


class HighScoreWindow(Window):
    def __init__(self):
        caption = 'High Score'
        image = "hs_bg.jpg"
        window_open = False
        super().__init__(caption, image, window_open)
        self.group.add(self.back_button)

    def draw(self, m_pos):
        super().draw(m_pos)
        self.print_headline((320, 50))
        high_score = HighScoreMenu()
        high_score.draw_table(self.screen)
        high_score.draw_text(self.screen)
        high_score.draw_high_score(self.screen)
        self.back_button.draw(m_pos, self.screen)

    def update(self, m_pos, current_time, lvl_window, hs_window, menu_window, game_window, level_three_window, extra_posx=0, extra_posy=0):
        super().update(m_pos, current_time, lvl_window, hs_window, menu_window, game_window, level_three_window)

###############################################


class HighScoreMenu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = (105, 105, 105)

    def draw_table(self, surface):
        pygame.draw.rect(surface, self.color, (150, 150, 500, 310), 4)
        pygame.draw.line(surface, self.color, (150, 225), (649, 225), 4)
        pygame.draw.line(surface, self.color, (150, 300), (649, 300), 4)
        pygame.draw.line(surface, self.color, (150, 375), (649, 375), 4)
        pygame.draw.line(surface, self.color, (300, 150), (300, 455), 4)

    def draw_text(self, surface):
        font = pygame.font.Font('mainmenufont.ttf', 27)
        text = font.render('Points    Name', True, (255, 165, 1))
        surface.blit(text, (160, 195))

    def draw_high_score(self, surface):
        start_point = 250
        index = 0
        name_index = 0
        yellow = (255, 165, 1)
        with open('high_score', 'r') as file:
            lines = file.readlines()
            font = pygame.font.Font('mainmenufont.ttf', 27)
            for line in range(3):
                text = font.render(str(lines[index]), True, yellow)
                surface.blit(text, (180, start_point + line * 80))
                index += 1

        with open('names', 'r') as file:
            lines = file.readlines()
            for line in range(3):
                text = font.render(str(lines[name_index]), True, yellow)
                surface.blit(text, (325, start_point + line * 82))
                name_index += 1
