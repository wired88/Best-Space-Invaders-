import math
import random
import pygame
from pygame import mixer

from MotherClasses import Window, Spaceships, PowerUp, Buttons, StaticObjects, Bullet, Explosion


class GameWindow(Window):
    def __init__(self, caption, image):
        window_open = False
        super().__init__(caption, image, window_open)

        self.score = 0

        self.player_spaceship = PlayerSpaceship(400, 515)
        self.name_field = Name()
        self.pause = Pause()

        self.group_names = ['enemy_group', 'heart_group', 'powerup_group', 'explosion_group', 'player_bullet_group',
                            'enemy_bullet_group',
                            'player_group']

        for name in self.group_names:
            setattr(self, name, pygame.sprite.Group())

        self.volume = 100

        self.button_group = pygame.sprite.Group(self.pause)
        self.name_group = pygame.sprite.Group(self.name_field)

        self.last_powerup = pygame.time.get_ticks()
        self.change_y_screen_image = 0

        self.index = 1
        self.more_enemies = True
        self.more_enemies_at_score_points = 50

        # pause Attributes
        self.back_to_meu_button = BackToMenu()
        self.continue_button = Continue()
        self.back_group = pygame.sprite.Group(self.back_to_meu_button)
        self.pause_button_group = pygame.sprite.Group(self.back_to_meu_button,
                                                      self.continue_button)

        # lists
        self.bullet_group_list = [self.player_bullet_group,
                                  self.enemy_bullet_group]

        self.button_group_list = [self.button_group,
                                  self.name_group]

        self.group_list = [self.enemy_group,
                           self.heart_group,
                           self.powerup_group,
                           self.explosion_group,
                           self.player_bullet_group,
                           self.enemy_bullet_group,
                           self.player_group]

        with (open('high_score', 'r')) as file:
            self.high_score = int(file.readline(4))

    def update(self, m_pos, current_time, lvl_window, hs_window, menu_window, game_window, level_three_window,
               setting_window):

        self.spaceship_params = [self.screen,
                                 setting_window.volume_button.volume,
                                 current_time,
                                 self.empty_all_groups,
                                 self.heart_group,
                                 self.score,
                                 self.explosion_group,
                                 self.enemy_group]

        if not self.name_field.action:
            for group in self.button_group_list:  # update name-field before start game
                for sprite in group:
                    sprite.update(m_pos, menu_window, self, level_three_window, self.empty_all_groups, self.group_list,
                                  self.explosion_group)
        elif self.pause.action:
            self.pause_button_group.update(m_pos, menu_window, game_window, level_three_window, self.empty_all_groups,
                                           self.group_list,
                                           self.explosion_group)

        else:
            if not self.player_spaceship.dead:
                self.pause.update(m_pos, menu_window, self, level_three_window)
            else:
                self.back_group.update(m_pos, menu_window, game_window, level_three_window, self.empty_all_groups,
                                       self.group_list,
                                       self.explosion_group)

            for sprite in self.enemy_group.sprites():
                self.score = sprite.update(*self.spaceship_params,
                                           self.enemy_bullet_group,
                                           self.player_bullet_group,
                                           self.player_spaceship)


            self.player_spaceship.update(*self.spaceship_params,
                                         self.player_bullet_group,
                                         self.enemy_bullet_group,
                                         self.enemy_group)

            for bullet_group in self.bullet_group_list:
                bullet_group.update()

            if len(self.explosion_group) > 0:
                self.explosion_group.update()

            if len(self.powerup_group) > 0:
                self.powerup_group.update(self.player_spaceship,
                                      self.heart_group,
                                      current_time,
                                      self.powerup_group)
            if self.player_spaceship.lives <= 1:
                self.check_lives_and_enemy_position(self.score,
                                                    self.player_spaceship,
                                                    self.enemy_group,
                                                    self.group_list,
                                                    self.screen,
                                                    self.empty_all_groups,
                                                    self.print_game_over,
                                                    self.explosion_group,
                                                    self.group,
                                                    self.back_group,
                                                    m_pos)

            self.initialize_powerup(current_time,
                                    self.heart_group,
                                    self.powerup_group)

        #    if self.score >= self.more_enemies_at_score_points:
        #        self.add_enemies(self.enemy_group)
        #        self.more_enemies_at_score_points += 50

    def draw(self, m_pos):
        super().draw(m_pos)

        self.change_y_screen_image = self.seamless_background(self.change_y_screen_image,
                                                              self.image,
                                                              self.height,
                                                              self.screen)
        if not self.name_field.action:
            self.name_group.draw(self.screen)
            self.name_field.draw(m_pos, self.screen)

        elif self.pause.action:
            self.pause_button_group.draw(self.screen)

            for sprite in self.pause_button_group.sprites():
                sprite.draw(m_pos, self.screen)
        else:
            for group in self.group_list:
                group.draw(self.screen)

            if not self.player_spaceship.dead:
                self.pause.draw(m_pos, self.screen)
                self.button_group.draw(self.screen)
            else:
                self.back_group.draw(self.screen)
                for sprite in self.back_group.sprites():
                    sprite.draw(m_pos, self.screen)

            for sprite in self.enemy_group.sprites():
                sprite.draw(self.screen,
                            self.print_newhs_score_counter)

            for bullet_group in self.bullet_group_list:
                bullet_group.draw(self.screen)

            self.player_group.draw(self.screen)

            self.player_spaceship.draw(self.screen,
                                       self.print_newhs_score_counter)

            self.print_newhs_score_counter(
                "freesansbold.ttf",
                16,
                f"Punkte: {str(self.score)}",
                (155, 200, 255),
                (8, 8),
                self.screen,
            )

            if self.score > int(self.high_score):
                self.print_newhs_score_counter('Starjedi.ttf',
                                               10,
                                               'New Record!',
                                               (255, 134, 31),
                                               (8, 20),
                                               self.screen)

    def empty_all_groups(self, group_l, explosion_group):
        for group in group_l:
            if group != explosion_group:
                group.empty()

    def seamless_background(self, change_screen, image, screen_height, surface):
        change_screen += 1
        surface.blit(image, (0, change_screen))
        if change_screen >= screen_height:
            return 0
        if change_screen > 0:
            surface.blit(image, (0, 0 - screen_height + change_screen))
            return change_screen

    def initialize_powerup(self, current_time, heart_g, powerup_group):
        power_up_counter = 3000
        if current_time - self.last_powerup > power_up_counter and len(heart_g) <= 2:
            powerup = random.choice(PowerUp.__subclasses__())
            powerup_group.add(powerup(random.randint(0, 736), random.randint(-130, -60)))
            self.last_powerup = current_time

    def add_enemies(self, group):
        if len(group) == 2 and self.more_enemies:
            # add more enemies
            self.index += 1
            for _ in range(9 + self.index):
                group.add(NormalEnemy(random.randint(0, 736), random.randint(-130, -60)))
            for _ in range(0 + self.index):
                group.add(SpeedEnemy(random.randint(0, 736), random.randint(-130, -60)))

    # print methods
    def print_newhs_score_counter(self, font, font_size, text, color, pos, surface):
        score_font = pygame.font.Font(font, font_size)
        score_text = score_font.render(text, True, color)
        surface.blit(score_text, pos)

    def check_lives_and_enemy_position(self, game_score, player, enemies_g, group_l,
                                       surface, empty_groups, print_game_over, explosion_group, my_group, back_group,
                                       m_pos):

        if player.lives == 0:
            empty_groups(group_l, explosion_group)
            print_game_over(game_score, surface)
            player.dead = True
            back_group.draw(surface)

        elif len(enemies_g) == 0 and len(my_group) == 0:
            self.print_mission_complete(surface)
            empty_groups(group_l, explosion_group)
            back_group.draw(surface)
            for sprite in back_group.sprites():
                sprite.draw(m_pos, surface)

    def print_mission_complete(self, surface):
        win_font = pygame.font.Font("freesansbold.ttf", 64)
        win_font2 = pygame.font.Font("freesansbold.ttf", 48)
        win_text = win_font.render("Mission Complete", True, (153, 204, 0))
        win_text2 = win_font2.render("Möchtest du noch eine Runde spielen?", True, (204, 204, 255))
        surface.blit(win_text, (350, 250))
        surface.blit(win_text2, (350, 350))

    def print_game_over(self, game_score, surface):
        go_font = pygame.font.Font("freesansbold.ttf", 64)
        go_text = go_font.render("GAME OVER", True, (255, 255, 255))
        score_font1 = pygame.font.Font("freesansbold.ttf", 16)
        go_text_score = score_font1.render(
            f"Dein Punktestand: {str(game_score)}", True, (100, 200, 10)
        )
        surface.blit(go_text, (200, 150))
        surface.blit(go_text_score, (325, 250))

    def save_high_score_data(self, score, name_field, high_score):
        if score > high_score:
            with open('high_score', 'r+') as file:
                lines = file.readlines()
                lines.append(f"{score}\n")
                lines.sort(key=int, reverse=True)
                lines = lines[:3]
            with open('high_score', 'w') as f:
                f.writelines(lines)

            with open('names', 'r+') as file:
                hs_names = file.readlines()
                index = lines.index(f"{score}\n")
                hs_names.insert(index, name_field.name + '\n')
                hs_names = hs_names[:3]
            with open('names', 'w') as f:
                f.writelines(hs_names)


class ShieldSymbol(StaticObjects):
    def __init__(self):
        x = 20
        y = 65
        image = "shield_pu.png"
        super().__init__(image, x, y)

    def draw(self, current_time, player, print_counter, surface):
        pass


class PowerUpShieldSpaceship(StaticObjects):
    def __init__(self, x, y):
        image = "shield.png"
        super().__init__(image, x, y)

    def update(self, player):
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y


class Hearts(StaticObjects):
    def __init__(self, x, y):
        image = "heart.png"
        super().__init__(image, x, y)


class HealthPowerUp(PowerUp):
    def __init__(self, x, y):
        image = "passion.png"
        super().__init__(image, x, y)

    def apply(self, player, heart_gr):
        if player.lives < 3:
            player.lives += 1
            heart = Hearts(16 * len(heart_gr) + 16, 45)
            heart_gr.add(heart)


class ShieldPowerUp(PowerUp):
    def __init__(self, x, y):
        image = "shield_pu.png"
        super().__init__(image, x, y)

    def apply(self, player, heart_gr):
        player.add_shield()


class DoubleShootPowerUp(PowerUp):
    def __init__(self, x, y):
        image = "fire.png"
        super().__init__(image, x, y)

    def apply(self, player, heart_gr):
        player.add_shoot_bar()


class NormalEnemy(Spaceships):
    def __init__(self, x, y):
        image = "ufo.png"
        speed = 5
        lives = 1
        shoot_count = 0
        cooldown = 0
        speed_y = 60
        sound = None
        super().__init__(image, speed, lives, shoot_count, x, y, cooldown, 2, sound, speed_y)

    def shoot(self, current_time, group, bullet_group, volume):
        pass


class SpeedEnemy(Spaceships):
    def __init__(self, x, y):
        image = "aircraft.png"
        speed = 10
        lives = 2
        shoot_count = 1000
        cooldown = 0
        speed_y = 60
        sound = 'tie_shoot_better.mp3'
        super().__init__(image, speed, lives, shoot_count, x, y, cooldown, 2, sound, speed_y)


class BossSpaceship(Spaceships):
    def __init__(self, x, y):
        image = "death-star.png"
        speed = 1
        lives = 3
        shoot_count = 600
        cooldown = 2000
        speed_y = 100
        sound = 'death-star_shoot_sound.mp3'
        super().__init__(image, speed, lives, shoot_count, x, y, cooldown, 2, sound, speed_y)


class PlayerSpaceship(Spaceships):
    def __init__(self, x, y):
        image = "battleship.png"
        speed = 0
        lives = 3
        shoot_count = 200
        cooldown = 200
        sound = 'player-shoot-sound_ogg.ogg'
        super().__init__(image, speed, lives, shoot_count, x, y, cooldown, 3, sound, speed_y=None)
        self.amo = 0
        self.double_shoot = False
        self.shield_bool = False
        self.dead = False
        self.z = True
        self.move_choice = random.choice([-5, 5])
        self.angle = 0
        self.shield_group = pygame.sprite.Group()
        self.total_seconds = 7
        self.last_up = pygame.time.get_ticks()

    def draw(self, surface, print_counter):
        super().draw(surface, print_counter)
        self.shield_group.draw(surface)
        if self.double_shoot:
            self.draw_double_shoot_bar(surface)
        if self.shield_bool:
            self.draw_shield_timer(surface, print_counter)

    def draw_shield_timer(self, surface, print_counter):
        shield_symbol = ShieldSymbol()
        surface.blit(shield_symbol.image, (20, 40))
        print_counter("mainmenufont.ttf", 27, str(self.total_seconds), (255, 165, 0),
                      (30, 40), surface)

    def update(self, surface, volume, current_time, func, h_group, game_score, explosion_group, group, bullet_group,
               enemy_bullet_group, spaceship):

        super().update(surface, volume, current_time, func, h_group, game_score, explosion_group, group, bullet_group,
                       enemy_bullet_group, spaceship)

        if self.shield_bool:
            self.shield_counter_update(current_time)

    def shield_counter_update(self, current_time):
        if current_time - self.last_up > 1000:
            self.total_seconds -= 1
            self.last_up = current_time
        if self.total_seconds <= 0:
            self.shield_bool = False
            self.shield_group.empty()
            self.total_seconds = 7

    def shoot(self, current_time, heart_g, bullet_group, volume):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and current_time - self.last_shot > self.shoot_count and len(heart_g) > 0:

            shooting_sound = mixer.Sound(f'sounds/{self.sound}')
            shooting_sound.play()
            shooting_sound.set_volume(volume)

            if not self.double_shoot:
                bullet = Bullet(self.rect.centerx,
                                self.rect.top,
                                "laser.png",
                                math.pi / 2,
                                -10,
                                0)
                bullet_group.add(bullet)
            else:
                bullet_double_shoot = Bullet(self.rect.left,
                                             self.rect.top,
                                             "laser.png",
                                             math.pi / 2,
                                             -10,
                                             0)
                bullet_double_shoot2 = Bullet(self.rect.right,
                                              self.rect.top,
                                              "laser.png",
                                              math.pi / 2,
                                              -10,
                                              0)

                bullet_group.add(bullet_double_shoot)
                bullet_group.add(bullet_double_shoot2)

                self.amo -= 2

            self.last_shot = current_time

    def check_collision(self, h_group, game_score, spaceship, explosion_group, enemy_bullet_group, group):
        if pygame.sprite.spritecollide(self, enemy_bullet_group, True) and \
                not self.shield_bool and \
                len(h_group) > 0:
            h_group.sprites()[-1].kill()
            self.lives -= 1
            explosion_group.add(Explosion(self.rect.x, self.rect.y, 1))

    def add_shield(self):
        powerup_shield = PowerUpShieldSpaceship(self.rect.centerx, self.rect.centery)
        self.shield_group.add(powerup_shield)
        self.shield_bool = True
        self.total_seconds = 7

    def move(self, func, spaceship, surface, explosion_group, group=None):
        if not self.dead:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                self.move_x(-10)
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                self.move_x(10)
            if key[pygame.K_UP] or key[pygame.K_w]:
                self.move_y(-10)
            if key[pygame.K_DOWN] or key[pygame.K_s]:
                self.move_y(10)
        else:
            self.shield_bool = False
            self.double_shoot = False
            self.create_rotate_img(explosion_group, surface)

    def create_rotate_img(self, explosion_group, surface):
        self.angle += 4
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
        huge_explosion = Explosion(400, 250, 3)
        if 736 >= self.rect.x > 10 and 10 < self.rect.y < 536:
            self.kill()
            surface.blit(self.rotated_image, (self.rect.x, self.rect.y))
            self.move_x(self.move_choice)
            self.move_y(self.move_choice)
        elif len(explosion_group) == 0 and self.z:
            explosion_group.add(explosion)
            explosion_group.add(huge_explosion)
            self.z = False

    def add_shoot_bar(self):
        self.amo = 200
        self.double_shoot = True

    def draw_double_shoot_bar(self, surface):
        if self.double_shoot:
            blue = (0, 0, 255)
            orange = (255, 165, 0)
            pygame.draw.rect(surface, orange, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 10))
            pygame.draw.rect(surface, blue,
                             (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.amo / 200)), 10))
            if self.amo <= 0:
                self.double_shoot = False


class Pause(Buttons):
    def __init__(self):
        x = 740
        y = 40
        image = "pause.png"
        extra_image_sizex = 32
        extra_image_sizey = 32
        bg_image = "pause-button.png"
        bgimage_sizex = 32
        bgimage_sizey = 32
        text = ''
        plus_vecx = 0
        plus_vecy = 0
        super().__init__(x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey,
                         text, plus_vecx, plus_vecy)


class Name(Buttons):
    def __init__(self):
        x = 680
        y = 500
        image = "check.png"
        extra_image_sizex = 42
        extra_image_sizey = 42
        bg_image = "check_green.png"
        bgimage_sizex = 42
        bgimage_sizey = 42
        text = ''
        plus_vecx = 0
        plus_vecy = 0
        super().__init__(x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey,
                         text, plus_vecx, plus_vecy)
        self.name = ''

        self.yoda_img = pygame.image.load('yoda.png')
        self.yoda_img = pygame.transform.scale(self.yoda_img, (100, 200))

        self.field = pygame.image.load('frame.png')
        self.field = pygame.transform.scale(self.field, (600, 500))

        self.bubble = pygame.image.load('speech-bubble.png')
        self.bubble = pygame.transform.scale(self.bubble, (400, 200))

        self.text_field = pygame.image.load('cell.png')
        self.text_field = pygame.transform.scale(self.text_field, (300, 200))

    def update(self, m_pos, menu_window, game_window, level_three_window, empty_groups, group_l, explosion_group):
        super().update(m_pos, menu_window, game_window, level_three_window, empty_groups, group_l, explosion_group)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and len(self.name) <= 13:
                if event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    self.name += event.unicode

    def draw(self, m_pos, surface):
        super().draw(m_pos, surface)
        surface.blit(self.field, (100, 50))
        surface.blit(self.bubble, (200, 150))
        surface.blit(self.yoda_img, (125, 270))
        self.draw_text(surface, 16, 224, 210, 'Deinen Namen eingeben, du solltest')
        surface.blit(self.text_field, (280, 240))
        self.draw_text(surface, 18, 340, 325, self.name)
        return self.name


class BackMainMenu(Buttons):
    def __init__(self):
        x = 680
        y = 460
        image = "rounded-recktangle.png"
        extra_image_sizex = 64
        extra_image_sizey = 64
        bg_image = "check_green.png"
        bgimage_sizex = 64
        bgimage_sizey = 64
        text = ''
        plus_vecx = 0
        plus_vecy = 0
        super().__init__(x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey,
                         text, plus_vecx, plus_vecy)


class BackToMenu(Buttons):
    def __init__(self):
        x = 400
        y = 350
        image = "rounded-rectangle.png"
        extra_image_sizex = 250
        extra_image_sizey = 128
        bg_image = "ray_shield.png"
        bgimage_sizex = 250
        bgimage_sizey = 70
        text = 'Back to Menu'
        plus_vecx = 3
        plus_vecy = 30
        super().__init__(x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey,
                         text, plus_vecx, plus_vecy)

    def update(self, m_pos, menu_window, game_window, level_three_window, empty_groups, group_l, explosion_group):
        super().update(m_pos, menu_window, game_window, level_three_window, empty_groups, group_l, explosion_group)
        if self.action:
            empty_groups(group_l, explosion_group)
            # Save the game states
            game_window.save_high_score_data(game_window.score, game_window.name_field, game_window.high_score)
            level_three_window.save_high_score_data(level_three_window.score, level_three_window.name_field,
                                                    level_three_window.high_score)
            # Reset the scores
            game_window.score = 0
            level_three_window.score = 0
            # Reset the player spaceship's shield and double shoot abilities
            game_window.player_spaceship.shield_bool = False
            game_window.player_spaceship.double_shoot = False
            # Set the window booleans
            menu_window.window_open = True
            game_window.window_open = False
            level_three_window.window_open = False
            # Empty the enemy group in level three window
            level_three_window.enemy_group.empty()
            # Set the action to False
            self.action = False

    def draw(self, m_pos, surface):
        super().draw(m_pos, surface)
        self.draw_text(surface, 27, self.rect.x + 10, self.rect.y + 40, str(self.text))


class Continue(Buttons):
    def __init__(self):
        x = 400
        y = 250
        image = "rounded-rectangle.png"
        extra_image_sizex = 160
        extra_image_sizey = 128
        bg_image = "ray_shield.png"
        bgimage_sizex = 160
        bgimage_sizey = 70
        text = 'Continue'
        plus_vecx = 3
        plus_vecy = 30
        super().__init__(x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey,
                         text, plus_vecx, plus_vecy)

    def update(self, m_pos, menu_window, game_window, level_three_window, empty_groups, group_l, explosion_group):
        super().update(m_pos, menu_window, game_window, level_three_window, empty_groups, group_l, explosion_group)
        if self.action:
            self.action = False
            game_window.pause.action = False
            level_three_window.pause.action = False

    def draw(self, m_pos, surface):
        super().draw(m_pos, surface)
        self.draw_text(surface, 27, self.rect.x + 10, self.rect.y + 40, str(self.text))


class Settings(Buttons):
    def __init__(self):
        x = 400
        y = 250
        image = "rounded-rectangle.png"
        extra_image_sizex = 160
        extra_image_sizey = 128
        bg_image = "ray_shield.png"
        bgimage_sizex = 160
        bgimage_sizey = 70
        text = 'Continue'
        plus_vecx = 3
        plus_vecy = 30
        super().__init__(x, y, image, extra_image_sizex, extra_image_sizey, bg_image, bgimage_sizex, bgimage_sizey,
                         text, plus_vecx, plus_vecy)
